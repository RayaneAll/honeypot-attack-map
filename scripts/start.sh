#!/bin/bash

# Honeypot Attack Map - Start Script
# This script starts the honeypot attack map application

echo "🛡️  Starting Honeypot Attack Map..."
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p backend/data

# Start the application
echo "🚀 Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services started successfully!"
    echo ""
    echo "🌐 Access the application:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:5000"
    echo "   Health Check: http://localhost:5000/api/health"
    echo ""
    echo "📊 To view logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 To stop the application:"
    echo "   docker-compose down"
else
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi
