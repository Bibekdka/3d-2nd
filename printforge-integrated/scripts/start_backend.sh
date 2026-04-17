#!/bin/bash
# PrintForge + 3D Business Brain - Development Startup (Linux/Mac)

echo ""
echo "========================================"
echo "  PrintForge - Backend Server Startup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Navigate to backend
cd backend

# Start the server
echo ""
echo "✅ Starting backend server..."
echo "📖 API Docs available at: http://localhost:8000/api/docs"
echo ""
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
