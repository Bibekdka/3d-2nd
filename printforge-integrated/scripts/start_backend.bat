@echo off
REM PrintForge + 3D Business Brain - Development Startup (Windows)
REM This script starts the backend API server

echo.
echo ========================================
echo  PrintForge - Backend Server Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r backend/requirements.txt

REM Navigate to backend
cd backend

REM Start the server
echo.
echo ✅ Starting backend server...
echo 📖 API Docs available at: http://localhost:8000/api/docs
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
