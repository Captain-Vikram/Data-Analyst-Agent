#!/bin/bash

echo "🤖 AI Data Analyst Agent - Quick Start"
echo "====================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org/"
    exit 1
fi

echo "✅ Python found"
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

echo "🔧 Activating virtual environment..."
source .venv/bin/activate

echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo
echo "🤖 Setup complete!"
echo
echo "Next steps:"
echo "1. Make sure LM Studio is running with a model loaded (for local backend)"
echo "2. Or set TOGETHER_API_KEY environment variable (for cloud backend)"
echo
read -p "Press Enter to start the application..."

python3 main.py
