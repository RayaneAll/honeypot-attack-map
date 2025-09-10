"""
Honeypot Attack Map - Backend Flask Application
Main application file for the honeypot server and API
"""

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
import json
import threading
import socket
import time
from datetime import datetime
import requests
import os
from models import init_db, Attack, get_recent_attacks, get_attack_stats
from geolocation import get_ip_location

app = Flask(__name__)
app.config['SECRET_KEY'] = 'honeypot_secret_key_2024'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
HONEYPOT_PORTS = [22, 23, 80, 443, 3389, 5432, 3306]  # Common attack ports
DB_PATH = 'attacks.db'

class HoneypotServer:
    """Simple TCP honeypot server that logs connection attempts"""
    
    def __init__(self, port):
        self.port = port
        self.running = False
        self.socket = None
        
    def start(self):
        """Start the honeypot server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"🔥 Honeypot listening on port {self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    # Log the attack
                    self.log_attack(address[0], self.port, 'TCP')
                    client_socket.close()
                except Exception as e:
                    if self.running:
                        print(f"Error accepting connection: {e}")
                        
        except Exception as e:
            print(f"Error starting honeypot on port {self.port}: {e}")
    
    def stop(self):
        """Stop the honeypot server"""
        self.running = False
        if self.socket:
            self.socket.close()
    
    def log_attack(self, ip_address, port, protocol):
        """Log an attack attempt and emit to frontend"""
        try:
            # Get geolocation
            location = get_ip_location(ip_address)
            
            # Create attack record
            attack = Attack(
                ip_address=ip_address,
                port=port,
                protocol=protocol,
                country=location.get('country', 'Unknown'),
                city=location.get('city', 'Unknown'),
                latitude=location.get('latitude', 0),
                longitude=location.get('longitude', 0),
                timestamp=datetime.now()
            )
            
            # Save to database
            attack.save()
            
            # Emit to frontend via WebSocket
            attack_data = {
                'id': attack.id,
                'ip_address': attack.ip_address,
                'port': attack.port,
                'protocol': attack.protocol,
                'country': attack.country,
                'city': attack.city,
                'latitude': attack.latitude,
                'longitude': attack.longitude,
                'timestamp': attack.timestamp.isoformat()
            }
            
            socketio.emit('new_attack', attack_data)
            print(f"🚨 Attack detected: {ip_address} on port {port} from {location.get('country', 'Unknown')}")
            
        except Exception as e:
            print(f"Error logging attack: {e}")

# Global honeypot instances
honeypots = {}

def start_honeypots():
    """Start all honeypot servers"""
    for port in HONEYPOT_PORTS:
        honeypot = HoneypotServer(port)
        honeypots[port] = honeypot
        thread = threading.Thread(target=honeypot.start, daemon=True)
        thread.start()

# API Routes
@app.route('/api/attacks', methods=['GET'])
def get_attacks():
    """Get recent attacks with optional filtering"""
    limit = request.args.get('limit', 100, type=int)
    country = request.args.get('country')
    protocol = request.args.get('protocol')
    
    attacks = get_recent_attacks(limit=limit, country=country, protocol=protocol)
    
    return jsonify([{
        'id': attack.id,
        'ip_address': attack.ip_address,
        'port': attack.port,
        'protocol': attack.protocol,
        'country': attack.country,
        'city': attack.city,
        'latitude': attack.latitude,
        'longitude': attack.longitude,
        'timestamp': attack.timestamp.isoformat()
    } for attack in attacks])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get attack statistics"""
    stats = get_attack_stats()
    return jsonify(stats)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'honeypots': len(honeypots)})

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected to WebSocket')
    emit('connected', {'message': 'Connected to honeypot feed'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected from WebSocket')

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start honeypot servers
    start_honeypots()
    
    # Start Flask app
    print("🚀 Starting Honeypot Attack Map Backend...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
