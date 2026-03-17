import json
import os
from pathlib import Path

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8742

DATA_DIR = Path.home() / ".4sight"
DB_PATH = DATA_DIR / "foresight.db"
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"
CONFIG_PATH = DATA_DIR / "config.json"


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_config() -> dict:
    ensure_data_dir()
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def _save_config(data: dict):
    ensure_data_dir()
    CONFIG_PATH.write_text(json.dumps(data, indent=2))


def get_api_key() -> str:
    env_key = os.getenv("ANTHROPIC_API_KEY", "")
    if env_key:
        return env_key
    return _load_config().get("anthropic_api_key", "")


def set_api_key(key: str):
    config = _load_config()
    config["anthropic_api_key"] = key
    _save_config(config)
