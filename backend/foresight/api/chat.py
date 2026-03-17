from __future__ import annotations

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import foresight.db.session as db
from foresight.diff.tracker import DiffTracker
from foresight.spreadsheet.excel_mac import ExcelMacInterface
from foresight.agents.base import SpreadsheetAgent

router = APIRouter()

# Shared spreadsheet connection (one per backend process)
_spreadsheet: ExcelMacInterface | None = None


async def get_spreadsheet() -> ExcelMacInterface:
    global _spreadsheet
    if _spreadsheet is None:
        _spreadsheet = ExcelMacInterface()
        await _spreadsheet.connect()
    return _spreadsheet


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    # Try to connect to Excel, but don't block chat if it's not available
    spreadsheet = None
    excel_error = None
    try:
        spreadsheet = await get_spreadsheet()
    except Exception as e:
        excel_error = str(e)

    async with db.SessionLocal() as session:
        tracker = DiffTracker(spreadsheet, session) if spreadsheet else None
        agent = SpreadsheetAgent(tracker)

        if excel_error:
            await websocket.send_json({
                "type": "error",
                "message": f"Excel not connected: {excel_error}. Chat still works, but spreadsheet tools are unavailable.",
            })

        try:
            while True:
                data = await websocket.receive_json()

                if data.get("type") == "chat":
                    message = data.get("message", "")
                    attachments = data.get("attachments", [])
                    if not message and not attachments:
                        continue

                    try:
                        async for event in agent.chat(message, attachments=attachments):
                            await websocket.send_json(event)
                        await websocket.send_json({"type": "done"})
                    except Exception as e:
                        await websocket.send_json({"type": "error", "message": str(e)})
                        await websocket.send_json({"type": "done"})

        except WebSocketDisconnect:
            pass
