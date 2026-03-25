@echo off
setlocal

set DIR=%~dp0

:: --- Install dependencies if needed ---

:: Backend
if not exist "%DIR%backend\.venv" (
    echo Setting up Python backend...
    python -m venv "%DIR%backend\.venv" || exit /b 1
)
call "%DIR%backend\.venv\Scripts\activate.bat" || exit /b 1
python -c "import foresight" 2>nul || (
    echo Installing backend dependencies...
    pip install -e "%DIR%backend" --quiet || exit /b 1
)

:: Frontend
if not exist "%DIR%frontend\node_modules" (
    echo Installing frontend dependencies...
    cd /d "%DIR%frontend" && npm install --silent || exit /b 1
)

:: --- Launch Tauri (starts frontend + backend automatically) ---
cd /d "%DIR%frontend"
npm run tauri dev
