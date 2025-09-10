# 📸 Screenshots and Demos

This directory contains screenshots and demonstration materials for the Honeypot Attack Map project.

## 📁 Contents

- `dashboard.png` - Main dashboard view
- `attack-map.png` - Interactive attack map detail
- `dark-mode.png` - Dark mode interface
- `mobile.png` - Mobile responsive view
- `api-docs.png` - API documentation
- `docker-logs.png` - Docker container logs

## 🎬 Demo Instructions

### Quick Demo Setup

1. **Start the application**
```bash
./scripts/docker-start.sh demo
```

2. **Generate fake attacks**
```bash
# In another terminal
docker-compose exec backend python populate_fake_attacks.py --count 50 --websocket --delay 1
```

3. **Access the dashboard**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

### Demo Script

For a complete demonstration, use the provided demo script:

```bash
# Run the complete demo
./scripts/demo.sh
```

This script will:
- Start all services
- Generate fake attack data
- Open the dashboard in your browser
- Show real-time attack simulation

## 📊 Key Features to Demonstrate

### 1. Real-time Attack Map
- Interactive world map with attack markers
- Color-coded risk levels (Critical, High, Medium, Low)
- Detailed popups with attack information
- Real-time updates via WebSocket

### 2. Attack Statistics
- Total attack count
- Recent attacks (24h)
- Top attacking countries
- Port and protocol analysis

### 3. Filtering and Search
- Filter by country, protocol, port
- Time range selection
- Real-time search functionality

### 4. Responsive Design
- Mobile-friendly interface
- Dark/light mode toggle
- Smooth animations and transitions

### 5. API Documentation
- Interactive API docs at `/docs`
- WebSocket testing interface
- Health check endpoints

## 🎯 Portfolio Presentation

This project demonstrates:

- **Full-stack development** with modern technologies
- **Real-time data visualization** using WebSockets
- **Cybersecurity expertise** with honeypot implementation
- **Docker containerization** for easy deployment
- **Professional UI/UX** with responsive design
- **API design** with comprehensive documentation
- **Database design** with proper relationships and indexing

## 📝 Screenshot Guidelines

When taking screenshots for the portfolio:

1. **Use high resolution** (1920x1080 or higher)
2. **Show different views** (map, list, filters, mobile)
3. **Include real data** (use fake attack generator)
4. **Demonstrate interactivity** (hover states, animations)
5. **Show both light and dark modes**

## 🔧 Technical Details

- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: React with Vite and TailwindCSS
- **Database**: SQLite with PostgreSQL support
- **Maps**: Leaflet.js for interactive mapping
- **Real-time**: WebSocket communication
- **Containerization**: Docker and Docker Compose
