@echo off
echo Starting AI Server...
echo 1. Launching Ollama...
start "Ollama" ollama serve

echo 2. Waiting 5 seconds for Ollama...
timeout /t 5

echo 3. Launching Local AI Bridge (Port 8000)...
start "AI Bridge" python local_ai_server.py

echo.
echo ✅ AI System Started!
echo You can now run the app: streamlit run app.py
pause
