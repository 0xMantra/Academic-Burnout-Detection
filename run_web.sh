#!/bin/bash
# Quick Start Script for Web Interface

echo "=================================="
echo "Academic Burnout Detection System"
echo "Web Interface Setup"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python is available"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create data directory if it doesn't exist
mkdir -p data
echo "✓ Data directory ready"
echo ""

# Start the Flask app
echo "🚀 Starting Flask web server..."
echo ""
echo "════════════════════════════════════════"
echo "🌐 Web Interface Ready!"
echo "════════════════════════════════════════"
echo ""
echo "Open your browser and go to:"
echo "    👉 http://localhost:5000"
echo ""
echo "Features:"
echo "  • Home (/):       Student data input form"
echo "  • View Data (/data):     All student records"
echo "  • Dashboard (/dashboard): Statistics & charts"
echo ""
echo "Press Ctrl+C to stop the server"
echo "════════════════════════════════════════"
echo ""

python app.py
