from __future__ import annotations

import base64
import json
from typing import AsyncIterator

import anthropic

from foresight.config import get_api_key, CLAUDE_MODEL
from foresight.agents.tools.cell_tools import CELL_TOOLS
from foresight.diff.tracker import DiffTracker
from foresight.diff.changeset import cell_change_to_dict


SYSTEM_PROMPT = """\
You are a financial modeling assistant embedded in a spreadsheet application. \
You help users build, modify, and analyze financial models in Excel.

When the user asks you to make changes to the spreadsheet:
1. First read the relevant cells to understand the current state.
2. Make changes using write_cell, set_formula, or write_range.
3. Explain what you changed and why.

All your writes are tracked - the user can accept or reject each change individually. \
Be precise with cell references. Prefer formulas over hardcoded values when appropriate.

If the user shares images or files, analyze them carefully and use the information \
to help with their spreadsheet tasks.\
"""


class SpreadsheetAgent:
    def __init__(self, diff_tracker: DiffTracker | None):
        self.diff_tracker = diff_tracker
        self.messages: list[dict] = []

    def _get_client(self) -> anthropic.AsyncAnthropic:
        return anthropic.AsyncAnthropic(api_key=get_api_key())

    async def handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool call and return the result as a string."""
        if not self.diff_tracker or not self.diff_tracker.spreadsheet:
            return json.dumps({"error": "Excel is not connected. Please open a workbook and restart."})

        spreadsheet = self.diff_tracker.spreadsheet

        if tool_name == "read_cell":
            value = await spreadsheet.read_cell(tool_input["sheet"], tool_input["cell_ref"])
            formula = await spreadsheet.get_formula(tool_input["sheet"], tool_input["cell_ref"])
            return json.dumps({"value": value, "formula": formula})

        elif tool_name == "read_range":
            data = await spreadsheet.read_range(tool_input["sheet"], tool_input["range_ref"])
            return json.dumps({"data": data})

        elif tool_name == "write_cell":
            change = await self.diff_tracker.track_write(
                tool_input["sheet"], tool_input["cell_ref"], tool_input["value"]
            )
            return json.dumps({"status": "tracked", "change": cell_change_to_dict(change)})

        elif tool_name == "set_formula":
            change = await self.diff_tracker.track_write(
                tool_input["sheet"],
                tool_input["cell_ref"],
                None,
                new_formula=tool_input["formula"],
            )
            return json.dumps({"status": "tracked", "change": cell_change_to_dict(change)})

        elif tool_name == "write_range":
            changes = await self.diff_tracker.track_range_write(
                tool_input["sheet"], tool_input["start_cell"], tool_input["values"]
            )
            return json.dumps({
                "status": "tracked",
                "changes": [cell_change_to_dict(c) for c in changes],
            })

        elif tool_name == "get_workbook_structure":
            structure = await spreadsheet.get_workbook_structure()
            return json.dumps(structure)

        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def _build_content(self, message: str, attachments: list[dict] | None = None) -> list[dict] | str:
        """Build a content array with text and any image/file attachments."""
        if not attachments:
            return message

        content: list[dict] = []

        for att in attachments:
            media_type = att.get("media_type", "")
            data = att.get("data", "")

            if media_type.startswith("image/"):
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": data,
                    },
                })
            else:
                # For non-image files, include as text
                try:
                    text_data = base64.b64decode(data).decode("utf-8")
                    content.append({
                        "type": "text",
                        "text": f"[File: {att.get('name', 'unknown')}]\n{text_data}",
                    })
                except Exception:
                    content.append({
                        "type": "text",
                        "text": f"[File: {att.get('name', 'unknown')}] (binary file, cannot display)",
                    })

        if message:
            content.append({"type": "text", "text": message})

        return content

    async def chat(self, user_message: str, attachments: list[dict] | None = None) -> AsyncIterator[dict]:
        """Process a user message and yield streaming events."""
        content = self._build_content(user_message, attachments)
        self.messages.append({"role": "user", "content": content})

        # Start a changeset for any writes this turn
        if self.diff_tracker:
            await self.diff_tracker.begin_changeset()

        # Only include tools if Excel is connected
        tools = CELL_TOOLS if self.diff_tracker else []

        while True:
            # Stream response from Claude
            collected_text = ""
            tool_uses = []

            stream_kwargs = dict(
                model=CLAUDE_MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=self.messages,
            )
            if tools:
                stream_kwargs["tools"] = tools

            async with self._get_client().messages.stream(**stream_kwargs) as stream:
                async for event in stream:
                    if event.type == "content_block_start":
                        if event.content_block.type == "text":
                            pass
                        elif event.content_block.type == "tool_use":
                            tool_uses.append({
                                "id": event.content_block.id,
                                "name": event.content_block.name,
                                "input_json": "",
                            })
                    elif event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            collected_text += event.delta.text
                            yield {"type": "text_delta", "text": event.delta.text}
                        elif event.delta.type == "input_json_delta":
                            if tool_uses:
                                tool_uses[-1]["input_json"] += event.delta.partial_json

                final_message = await stream.get_final_message()

            # Add assistant message to history
            self.messages.append({"role": "assistant", "content": final_message.content})

            # If no tool use, we're done
            if final_message.stop_reason != "tool_use":
                break

            # Execute tool calls
            tool_results = []
            for tool_use_block in final_message.content:
                if tool_use_block.type == "tool_use":
                    yield {
                        "type": "tool_call",
                        "name": tool_use_block.name,
                        "input": tool_use_block.input,
                    }
                    result = await self.handle_tool_call(tool_use_block.name, tool_use_block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": result,
                    })
                    yield {"type": "tool_result", "name": tool_use_block.name, "result": result}

            self.messages.append({"role": "user", "content": tool_results})

        # Finalize changeset
        if self.diff_tracker:
            cs = await self.diff_tracker.end_changeset()
            if cs and cs.changes:
                from foresight.diff.changeset import changeset_to_dict
                yield {"type": "changeset", "changeset": changeset_to_dict(cs)}
