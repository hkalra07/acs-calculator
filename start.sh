#!/bin/bash
# Production startup script for ACS Calculator

echo "Starting ACS Calculator in production mode..."

# Set environment variables
export PORT=3000
export PYTHONUNBUFFERED=1
export NODE_ENV=production

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting ACS Calculator server..."
python3 acs_server.py
