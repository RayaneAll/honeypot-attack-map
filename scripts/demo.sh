#!/bin/bash

# Demo Script for Honeypot Attack Map
# ===================================
# This script provides a complete demonstration of the Honeypot Attack Map project
# It starts all services, generates fake data, and opens the dashboard

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Honeypot Attack Map - Demo${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_info "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            print_success "$service_name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start after $max_attempts attempts"
    return 1
}

# Function to open URL in browser
open_browser() {
    local url=$1
    local service_name=$2
    
    print_info "Opening $service_name in browser..."
    
    if command_exists open; then
        # macOS
        open "$url"
    elif command_exists xdg-open; then
        # Linux
        xdg-open "$url"
    elif command_exists start; then
        # Windows
        start "$url"
    else
        print_warning "Cannot open browser automatically. Please open: $url"
    fi
}

# Function to generate fake attacks
generate_fake_attacks() {
    local count=${1:-50}
    local use_websocket=${2:-true}
    local delay=${3:-2}
    
    print_step "Generating $count fake attacks..."
    
    if [ "$use_websocket" = "true" ]; then
        docker-compose exec -T backend python populate_fake_attacks.py --count "$count" --websocket --delay "$delay" &
    else
        docker-compose exec -T backend python populate_fake_attacks.py --count "$count" &
    fi
    
    local pid=$!
    print_info "Fake attack generator started (PID: $pid)"
    
    # Wait a bit for attacks to start appearing
    sleep 5
    
    return $pid
}

# Function to show project information
show_project_info() {
    print_header
    echo -e "${PURPLE}Project: Honeypot Attack Map${NC}"
    echo -e "${PURPLE}Description: Real-time cybersecurity visualization dashboard${NC}"
    echo -e "${PURPLE}Technologies: React, FastAPI, Docker, Leaflet.js${NC}"
    echo -e "${PURPLE}GitHub: https://github.com/your-username/honeypot-attack-map${NC}"
    echo ""
}

# Function to show demo steps
show_demo_steps() {
    echo -e "${CYAN}Demo Steps:${NC}"
    echo "1. 🚀 Starting Docker services"
    echo "2. 📊 Generating fake attack data"
    echo "3. 🌐 Opening dashboard in browser"
    echo "4. 🗺️ Demonstrating attack map"
    echo "5. 📱 Showing responsive design"
    echo "6. 🔧 Exploring API documentation"
    echo ""
}

# Function to show keyboard shortcuts
show_keyboard_shortcuts() {
    echo -e "${YELLOW}Keyboard Shortcuts:${NC}"
    echo "  Ctrl+C  - Stop the demo"
    echo "  Enter   - Continue to next step"
    echo "  'q'     - Quit demo"
    echo "  's'     - Show statistics"
    echo "  'l'     - Show logs"
    echo "  'r'     - Restart services"
    echo ""
}

# Function to show statistics
show_statistics() {
    print_step "Current Statistics"
    
    # Get attack count
    local total_attacks=$(docker-compose exec -T backend python -c "
from database import SessionLocal
from models import Attack
db = SessionLocal()
count = db.query(Attack).count()
print(count)
db.close()
" 2>/dev/null || echo "0")
    
    # Get recent attacks
    local recent_attacks=$(docker-compose exec -T backend python -c "
from database import SessionLocal
from models import Attack
from datetime import datetime, timedelta
db = SessionLocal()
recent = db.query(Attack).filter(Attack.timestamp >= datetime.utcnow() - timedelta(hours=24)).count()
print(recent)
db.close()
" 2>/dev/null || echo "0")
    
    echo "  📊 Total attacks: $total_attacks"
    echo "  🕐 Recent attacks (24h): $recent_attacks"
    echo "  🌍 Countries: $(docker-compose exec -T backend python -c "
from database import SessionLocal
from models import Attack
db = SessionLocal()
countries = db.query(Attack.country).distinct().count()
print(countries)
db.close()
" 2>/dev/null || echo "0")"
    echo ""
}

# Function to show logs
show_logs() {
    print_step "Recent Logs"
    docker-compose logs --tail=20
    echo ""
}

# Function to handle user input
handle_user_input() {
    while true; do
        read -p "Demo> " input
        case $input in
            "q"|"quit"|"exit")
                print_info "Exiting demo..."
                exit 0
                ;;
            "s"|"stats"|"statistics")
                show_statistics
                ;;
            "l"|"logs")
                show_logs
                ;;
            "r"|"restart")
                print_step "Restarting services..."
                docker-compose restart
                wait_for_service "http://localhost:8000/health" "Backend"
                wait_for_service "http://localhost:3000" "Frontend"
                print_success "Services restarted!"
                ;;
            "h"|"help")
                show_keyboard_shortcuts
                ;;
            "")
                break
                ;;
            *)
                print_warning "Unknown command: $input (type 'h' for help)"
                ;;
        esac
    done
}

# Main demo function
main() {
    # Check prerequisites
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Show project information
    show_project_info
    show_demo_steps
    show_keyboard_shortcuts
    
    # Start services
    print_step "Starting Docker services..."
    docker-compose up -d
    
    # Wait for services to be ready
    wait_for_service "http://localhost:8000/health" "Backend"
    wait_for_service "http://localhost:3000" "Frontend"
    
    print_success "All services are running!"
    
    # Generate fake attacks
    print_step "Generating fake attack data..."
    generate_fake_attacks 50 true 2
    
    # Open dashboard
    print_step "Opening dashboard..."
    open_browser "http://localhost:3000" "Honeypot Attack Map Dashboard"
    
    # Show statistics
    show_statistics
    
    # Show demo information
    echo -e "${GREEN}🎉 Demo is now running!${NC}"
    echo -e "${CYAN}Dashboard: http://localhost:3000${NC}"
    echo -e "${CYAN}API Docs: http://localhost:8000/docs${NC}"
    echo -e "${CYAN}Health Check: http://localhost:8000/health${NC}"
    echo ""
    
    # Interactive mode
    print_info "Interactive mode started. Type 'h' for help or 'q' to quit."
    handle_user_input
}

# Handle Ctrl+C
trap 'print_info "Demo interrupted by user. Stopping services..."; docker-compose down; exit 0' INT

# Run main function
main "$@"
