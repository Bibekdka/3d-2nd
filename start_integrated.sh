#!/bin/bash
# ============================================================
#  PrintForge + 3D Business Brain — Integrated Startup
#  Linux/macOS Bash Script
#  Starts backend and optional AI server
# ============================================================

clear

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🧠 PrintForge + 3D Business Brain — Integrated       ║"
echo "║  Starting Full Stack...                              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

echo "✓ Python $(python3 --version | awk '{print $2}')"
echo ""

# Create/activate virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -q -r requirements_integrated.txt
    echo "✓ Environment ready"
else
    source venv/bin/activate
    echo "✓ Virtual environment activated"
fi
echo ""

# Ask about AI server
read -p "🤖 Start AI server (optional)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting AI server..."
    sleep 2
    python local_ai_server.py &
    AI_PID=$!
    sleep 3
fi

echo ""
echo "🚀 Starting Backend API..."
echo "   📡 API will run at: http://localhost:8000"
echo "   📖 Docs at: http://localhost:8000/docs"
echo ""
echo "📝 Default Admin:"
echo "   Email: admin@printforge.com"
echo "   Password: admin123"
echo ""
echo "💡 Frontend: Open frontend_integrated.html in your browser"
echo "   or run: python -m http.server 3000"
echo ""
echo "────────────────────────────────────────────────────────"
echo ""

python -m uvicorn main_integrated:app --reload --host 127.0.0.1 --port 8000

# Cleanup
if [ ! -z "$AI_PID" ]; then
    kill $AI_PID 2>/dev/null
fi
