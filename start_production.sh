#!/bin/bash

# ACS Calculator Production Startup Script
echo "🚀 Starting ACS Calculator in Production Mode..."

# Create logs directory
mkdir -p logs

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install PM2 if not already installed
if ! command -v pm2 &> /dev/null; then
    echo "📦 Installing PM2..."
    npm install -g pm2
fi

# Stop any existing PM2 processes
echo "🛑 Stopping existing processes..."
pm2 stop acs-calculator 2>/dev/null || true
pm2 delete acs-calculator 2>/dev/null || true

# Start the application with PM2
echo "🚀 Starting ACS Calculator with PM2..."
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Show status
pm2 status

echo "✅ ACS Calculator is now running in production mode!"
echo "🌐 Application should be available at the production URL"
