@echo off
REM ============================================================
REM  PrintForge + 3D Business Brain — Integrated Startup
REM  Windows Batch Script
REM  Starts backend and optional AI server
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║  🧠 PrintForge + 3D Business Brain — Integrated       ║
echo ║  Starting Full Stack...                              ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Create/activate virtual environment if needed
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -q -r requirements_integrated.txt
    echo ✓ Environment ready
) else (
    call venv\Scripts\activate.bat
)
echo.

REM Start Ollama/AI Server (optional, in background)
echo 🤖 Would you like to start the AI server? (requires Ollama installed)
choice /C YN /M "Start AI server?"
if %errorlevel%==1 (
    echo Starting AI server...
    timeout /t 2 >nul
    start "AI Server" cmd /k "python local_ai_server.py"
    timeout /t 3
)

echo.
echo 🚀 Starting Backend API...
echo    📡 API will run at: http://localhost:8000
echo    📖 Docs at: http://localhost:8000/docs
echo.
echo 📝 Default Admin:
echo    Email: admin@printforge.com
echo    Password: admin123
echo.
echo 💡 Frontend: Open frontend_integrated.html in your browser
echo    or run: python -m http.server 3000
echo.
echo ────────────────────────────────────────────────────────
echo.

python -m uvicorn main_integrated:app --reload --host 127.0.0.1 --port 8000

pause
