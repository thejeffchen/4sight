from __future__ import annotations

import anthropic
from fastapi import APIRouter
from pydantic import BaseModel

from foresight.config import get_api_key, set_api_key

router = APIRouter(prefix="/api/settings")


class ApiKeyRequest(BaseModel):
    api_key: str


@router.get("/api-key/status")
async def api_key_status():
    key = get_api_key()
    return {
        "configured": bool(key),
        "hint": f"sk-ant-...{key[-4:]}" if len(key) > 8 else "",
    }


@router.post("/api-key")
async def save_api_key(body: ApiKeyRequest):
    key = body.api_key.strip()
    if not key.startswith("sk-ant-"):
        return {"status": "error", "message": "Invalid key format. Anthropic keys start with sk-ant-"}

    # Validate by making a test API call
    try:
        client = anthropic.Anthropic(api_key=key)
        client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}],
        )
    except anthropic.AuthenticationError:
        return {"status": "error", "message": "Invalid API key. Please check and try again."}
    except anthropic.BadRequestError as e:
        if "credit balance" in str(e).lower():
            return {"status": "error", "message": "API key is valid but your account has no credits. Add credits at console.anthropic.com."}
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Could not validate key: {e}"}

    set_api_key(key)
    return {"status": "ok"}
