#!/bin/bash

# Honeypot Attack Map - Stop Script
# This script stops the honeypot attack map application

echo "🛑 Stopping Honeypot Attack Map..."
echo "================================="

# Stop and remove containers
docker-compose down

echo "✅ Application stopped successfully!"
echo ""
echo "🗑️  To remove all data and volumes:"
echo "   docker-compose down -v"
echo ""
echo "🧹 To clean up everything:"
echo "   docker-compose down -v --rmi all"
