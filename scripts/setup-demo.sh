#!/bin/bash

# Honeypot Attack Map - Demo Setup Script
# This script sets up demo data for the honeypot

echo "🎭 Setting up Honeypot Attack Map Demo Data..."
echo "============================================="

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found. Please run this script from the project root."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt

# Generate demo data
echo "🎭 Generating demo attack data..."
python3 demo_data.py

echo "✅ Demo data generated successfully!"
echo ""
echo "🚀 You can now start the application with:"
echo "   ./scripts/start.sh"
echo ""
echo "📊 Or run locally with:"
echo "   cd backend && python3 app.py"
echo "   cd frontend && npm start"
