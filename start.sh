#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Install dependencies if needed ---

# Backend
if [ ! -d "$DIR/backend/.venv" ]; then
  echo "Setting up Python backend..."
  python3 -m venv "$DIR/backend/.venv"
fi
source "$DIR/backend/.venv/bin/activate"
if ! python -c "import foresight" 2>/dev/null; then
  echo "Installing backend dependencies..."
  pip install -e "$DIR/backend" --quiet
fi

# Frontend
if [ ! -d "$DIR/frontend/node_modules" ]; then
  echo "Installing frontend dependencies..."
  (cd "$DIR/frontend" && npm install --silent)
fi

# --- Launch Tauri (starts frontend + backend automatically) ---
cd "$DIR/frontend"
npm run tauri dev
