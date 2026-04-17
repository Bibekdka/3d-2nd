@echo off
REM Development startup script for 3D Brain on Windows
REM Usage: start_dev.bat

setlocal enabledelayedexpansion

echo.
echo 🧠 3D Business Brain - Development Startup
echo ===========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION%
echo.

REM Create/activate virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Upgrading pip...
    python -m pip install --upgrade pip >nul 2>&1
    echo Installing dependencies...
    pip install -q -r requirements.txt
    echo ✓ Dependencies installed
) else (
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
)
echo.

REM Check .env file
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env >nul
    echo ✓ .env created. Please edit it with your configuration.
    echo.
)

REM Check Google Sheets secrets
if not exist ".streamlit\secrets.toml" (
    echo ⚠️  .streamlit\secrets.toml not found.
    echo 💡 Please create it using the template in .streamlit\secrets.example.toml
    echo    Your Google Sheets credentials should go here.
    echo.
)

REM Install Playwright browsers
echo Checking Playwright installation...
python -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo 🌐 Installing Playwright browsers...
    playwright install chromium >nul 2>&1
    echo ✓ Playwright ready
) else (
    echo ✓ Playwright installed
)
echo.

echo 🚀 Starting services...
echo.
echo 1️⃣  Main Streamlit app will start on: http://localhost:8501
echo 2️⃣  In another terminal, run: start_ai.bat or python local_ai_server.py
echo    (AI server will start on: http://localhost:8000)
echo.
echo Press Enter to continue...
echo.

REM Start Streamlit
streamlit run app.py

pause
