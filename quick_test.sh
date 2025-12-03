#!/bin/bash
# Quick start script for Job Search Assistant
# This script sets up and tests the environment

set -e  # Exit on error

echo "=========================================="
echo "Job Search Assistant - Quick Setup & Test"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "Error: Python 3 is not installed"
    exit 1
}

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt --quiet || {
    echo "Warning: Some dependencies may not have installed correctly"
}

# Check .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env file"
        echo ""
        echo "⚠ IMPORTANT: Edit .env and add your RAPIDAPI_KEY"
        echo "  Open .env in a text editor and replace 'your_rapidapi_key_here'"
        echo "  with your actual RapidAPI key"
        echo ""
        read -p "Press Enter after updating .env file..."
    else
        echo "Error: .env.example not found"
        exit 1
    fi
else
    echo "✓ .env file already exists"
fi

# Run tests
echo ""
echo "Running automated tests..."
python3 test_tool.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Setup and testing complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Start the server: python3 app.py"
    echo "  2. Visit: http://localhost:5000/health"
    echo "  3. Test search: curl -X POST http://localhost:5000/search_jobs -H 'Content-Type: application/json' -d '{\"query\":\"python developer\"}'"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ Tests failed - please fix the issues above"
    echo "=========================================="
    exit 1
fi
