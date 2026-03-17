# 4sight

AI-powered desktop overlay for spreadsheet financial modeling. Chat with Claude to read, modify, and review changes to your Excel workbooks — with a diff system that lets you accept or reject every change before it's applied.

## Quick Start

```bash
cd financial-modeling && ./start.sh
```

That's it. Installs everything on first run, then launches the desktop overlay. The Python backend starts automatically in the background.

On first launch, 4sight will prompt you for your Anthropic API key right in the app. You can get one from [console.anthropic.com](https://console.anthropic.com/). Your key is saved locally and can be changed anytime in the Settings tab.

## Prerequisites

- **macOS**
- **Python 3.11+**
- **Node.js 18+**
- **Rust** (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`)
- **Microsoft Excel**

## How It Works

1. Open an Excel workbook on your Mac
2. Launch 4sight — it floats as an always-on-top overlay next to Excel
3. Enter your API key on first launch (Settings tab to change later)
4. Chat with Claude in the Chat tab — ask it to read or modify your spreadsheet
5. Review tracked changes in the Diffs tab
6. Accept or reject changes individually or as a batch

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Desktop | Tauri 2 (native macOS overlay) |
| Frontend | React, TypeScript, Vite, Tailwind CSS, Zustand |
| Backend | Python, FastAPI, SQLAlchemy (async), SQLite |
| AI | Anthropic Claude API |
| Excel | xlwings (macOS) |

## Project Structure

```
financial-modeling/
├── start.sh               # Installs dependencies + runs in browser mode
├── backend/
│   └── foresight/
│       ├── server.py      # FastAPI entry point (port 8742)
│       ├── config.py      # Configuration + API key storage (~/.4sight/)
│       ├── agents/        # Claude agent + tool definitions
│       ├── api/           # WebSocket (chat), REST (diff, settings)
│       ├── db/            # SQLAlchemy models and session
│       ├── diff/          # Diff tracker, changeset, rollback
│       └── spreadsheet/   # Excel interface (xlwings)
└── frontend/
    ├── src/
    │   ├── App.tsx        # Main component (Chat / Diffs / Settings)
    │   ├── components/    # Chat, diff, settings, and overlay UI
    │   ├── hooks/         # WebSocket connection hook
    │   ├── lib/           # WebSocket and REST API clients
    │   └── stores/        # Zustand state (chat, diffs, settings)
    └── src-tauri/         # Tauri desktop shell (Rust, auto-launches backend)
```
