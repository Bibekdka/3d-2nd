#!/bin/bash
# Development startup script for 3D Brain on Linux/macOS
# Usage: bash start_dev.sh

set -e

echo "🧠 3D Business Brain - Development Startup"
echo "==========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    source venv/bin/activate
    echo "✓ Virtual environment activated"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✓ .env created. Please edit it with your configuration."
fi

# Install Playwright browsers
if ! command -v chromium &> /dev/null; then
    echo "🌐 Installing Playwright browsers..."
    playwright install chromium
    echo "✓ Playwright ready"
fi

# Check for Google Sheets secrets
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  .streamlit/secrets.toml not found."
    echo "💡 Please create it using the template in .streamlit/secrets.example.toml"
    echo "   Your Google Sheets credentials should go here."
fi

echo ""
echo "🚀 Starting services..."
echo ""
echo "1️⃣  Main Streamlit app will start on: http://localhost:8501"
echo "2️⃣  In another terminal, run: python local_ai_server.py"
echo "    (AI server will start on: http://localhost:8000)"
echo ""

# Start Streamlit
streamlit run app.py --logger.level=info
