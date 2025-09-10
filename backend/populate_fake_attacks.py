#!/usr/bin/env python3
"""
Fake Attack Data Generator for Honeypot Attack Map
==================================================

This script generates realistic fake attack data for demonstration purposes.
It creates various types of attacks from different countries and sends them
via WebSocket for real-time testing of the dashboard.

Usage:
    python populate_fake_attacks.py [options]

Options:
    --count N        Number of fake attacks to generate (default: 50)
    --websocket      Send attacks via WebSocket in real-time
    --delay SECONDS  Delay between WebSocket attacks (default: 2)
    --help           Show this help message

Examples:
    python populate_fake_attacks.py
    python populate_fake_attacks.py --count 100 --websocket
    python populate_fake_attacks.py --count 20 --websocket --delay 1
"""

import asyncio
import argparse
import random
import time
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import socketio
import requests

# Import database components
from database import SessionLocal, engine
from models import Attack, Base
from services.geoip import get_geolocation_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

class FakeAttackGenerator:
    """Generates realistic fake attack data for demonstration purposes."""
    
    def __init__(self):
        self.db = SessionLocal()
        self.sio = None
        self.websocket_connected = False
        
        # Realistic attack data templates
        self.countries = [
            "United States", "China", "Russia", "Germany", "France",
            "United Kingdom", "Japan", "South Korea", "India", "Brazil",
            "Canada", "Australia", "Netherlands", "Sweden", "Norway",
            "Italy", "Spain", "Poland", "Ukraine", "Turkey",
            "Iran", "North Korea", "Pakistan", "Bangladesh", "Vietnam",
            "Thailand", "Indonesia", "Malaysia", "Philippines", "Singapore"
        ]
        
        self.attack_ports = {
            # Critical ports (high risk)
            "critical": [22, 3389, 5432, 3306, 1433, 1521, 6379, 27017],
            # High risk ports
            "high": [21, 23, 25, 53, 80, 443, 993, 995, 8080, 8443],
            # Medium risk ports
            "medium": [135, 139, 445, 993, 995, 1433, 1521, 3306, 5432],
            # Low risk ports
            "low": [123, 161, 162, 389, 636, 993, 995, 1433, 1521]
        }
        
        self.protocols = ["TCP", "UDP", "HTTP", "HTTPS", "SSH", "FTP", "SMTP", "DNS"]
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "curl/7.68.0",
            "wget/1.20.3",
            "python-requests/2.25.1",
            "Go-http-client/1.1",
            "Java/1.8.0_291",
            "PostmanRuntime/7.26.8",
            "Apache-HttpClient/4.5.13"
        ]
        
        self.attack_patterns = [
            "SSH brute force attempt",
            "RDP connection attempt",
            "HTTP directory traversal",
            "SQL injection attempt",
            "XSS payload injection",
            "Port scan detected",
            "FTP anonymous login attempt",
            "SMTP relay attempt",
            "DNS amplification attack",
            "Botnet communication"
        ]

    def generate_fake_ip(self) -> str:
        """Generate a realistic fake IP address."""
        # Generate IPs from different ranges to simulate global attacks
        ip_ranges = [
            (1, 126),      # Class A
            (128, 191),    # Class B
            (192, 223),    # Class C
        ]
        
        range_type = random.choice(ip_ranges)
        if range_type == (1, 126):  # Class A
            first_octet = random.randint(1, 126)
            return f"{first_octet}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        elif range_type == (128, 191):  # Class B
            first_octet = random.randint(128, 191)
            return f"{first_octet}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        else:  # Class C
            first_octet = random.randint(192, 223)
            return f"{first_octet}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

    def get_risk_level(self, port: int) -> str:
        """Determine risk level based on port number."""
        if port in self.attack_ports["critical"]:
            return "Critical"
        elif port in self.attack_ports["high"]:
            return "High"
        elif port in self.attack_ports["medium"]:
            return "Medium"
        else:
            return "Low"

    def generate_attack_data(self) -> Dict[str, Any]:
        """Generate a single fake attack with realistic data."""
        # Generate IP and get geolocation
        ip_address = self.generate_fake_ip()
        
        # Simulate geolocation data (in real scenario, this would call the API)
        country = random.choice(self.countries)
        geolocation_data = {
            "country": country,
            "city": f"City_{random.randint(1, 100)}",
            "region": f"Region_{random.randint(1, 20)}",
            "timezone": random.choice(["UTC", "EST", "PST", "CET", "JST", "IST"]),
            "isp": random.choice([
                "Comcast Cable", "Verizon", "AT&T", "Charter Communications",
                "China Telecom", "Deutsche Telekom", "Orange", "Vodafone",
                "BT Group", "NTT Communications", "SK Broadband", "Reliance Jio"
            ]),
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6)
        }
        
        # Generate attack details
        risk_level = random.choice(["critical", "high", "medium", "low"])
        port = random.choice(self.attack_ports[risk_level])
        protocol = random.choice(self.protocols)
        
        # Generate timestamp (within last 7 days)
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        seconds_ago = random.randint(0, 59)
        
        timestamp = datetime.utcnow() - timedelta(
            days=days_ago,
            hours=hours_ago,
            minutes=minutes_ago,
            seconds=seconds_ago
        )
        
        # Generate additional attack data
        user_agent = random.choice(self.user_agents)
        attack_pattern = random.choice(self.attack_patterns)
        
        additional_data = {
            "attack_pattern": attack_pattern,
            "risk_level": self.get_risk_level(port),
            "source_port": random.randint(1024, 65535),
            "packet_size": random.randint(64, 1500),
            "duration": random.randint(1, 300),  # seconds
            "attempts": random.randint(1, 10)
        }
        
        return {
            "ip_address": ip_address,
            "port": port,
            "protocol": protocol,
            "country": geolocation_data["country"],
            "city": geolocation_data["city"],
            "latitude": geolocation_data["latitude"],
            "longitude": geolocation_data["longitude"],
            "region": geolocation_data["region"],
            "timezone": geolocation_data["timezone"],
            "isp": geolocation_data["isp"],
            "timestamp": timestamp,
            "user_agent": user_agent,
            "additional_data": json.dumps(additional_data)
        }

    async def connect_websocket(self, websocket_url: str = "ws://localhost:8000"):
        """Connect to WebSocket for real-time attack simulation."""
        try:
            self.sio = socketio.AsyncClient()
            
            @self.sio.event
            async def connect():
                logger.info("✅ Connected to WebSocket server")
                self.websocket_connected = True
            
            @self.sio.event
            async def disconnect():
                logger.info("❌ Disconnected from WebSocket server")
                self.websocket_connected = False
            
            await self.sio.connect(websocket_url)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to WebSocket: {e}")
            return False

    async def send_attack_via_websocket(self, attack_data: Dict[str, Any]):
        """Send attack data via WebSocket for real-time simulation."""
        if self.sio and self.websocket_connected:
            try:
                # Format attack data for WebSocket
                websocket_data = {
                    "id": attack_data.get("id"),
                    "ip_address": attack_data["ip_address"],
                    "port": attack_data["port"],
                    "protocol": attack_data["protocol"],
                    "country": attack_data["country"],
                    "city": attack_data["city"],
                    "latitude": attack_data["latitude"],
                    "longitude": attack_data["longitude"],
                    "timestamp": attack_data["timestamp"].isoformat(),
                    "risk_level": attack_data.get("risk_level", "Unknown")
                }
                
                await self.sio.emit("new_attack", websocket_data)
                logger.info(f"📡 Sent attack via WebSocket: {attack_data['ip_address']}:{attack_data['port']}")
            except Exception as e:
                logger.error(f"❌ Failed to send attack via WebSocket: {e}")

    def save_attack_to_database(self, attack_data: Dict[str, Any]) -> Attack:
        """Save attack data to database."""
        try:
            attack = Attack(**attack_data)
            self.db.add(attack)
            self.db.commit()
            self.db.refresh(attack)
            
            # Add ID to attack_data for WebSocket
            attack_data["id"] = attack.id
            attack_data["risk_level"] = self.get_risk_level(attack.port)
            
            logger.info(f"💾 Saved attack to database: {attack.ip_address}:{attack.port}")
            return attack
        except Exception as e:
            logger.error(f"❌ Failed to save attack to database: {e}")
            self.db.rollback()
            return None

    async def generate_attacks(self, count: int, use_websocket: bool = False, delay: float = 2.0):
        """Generate and process fake attacks."""
        logger.info(f"🚀 Starting generation of {count} fake attacks...")
        
        if use_websocket:
            websocket_connected = await self.connect_websocket()
            if not websocket_connected:
                logger.warning("⚠️ WebSocket connection failed, continuing without real-time updates")
        
        generated_count = 0
        failed_count = 0
        
        for i in range(count):
            try:
                # Generate attack data
                attack_data = self.generate_attack_data()
                
                # Save to database
                attack = self.save_attack_to_database(attack_data)
                if attack:
                    generated_count += 1
                    
                    # Send via WebSocket if enabled
                    if use_websocket and self.websocket_connected:
                        await self.send_attack_via_websocket(attack_data)
                        
                        # Add delay between WebSocket sends for realistic simulation
                        if delay > 0:
                            await asyncio.sleep(delay)
                else:
                    failed_count += 1
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    logger.info(f"📊 Progress: {i + 1}/{count} attacks processed")
                    
            except Exception as e:
                logger.error(f"❌ Error generating attack {i + 1}: {e}")
                failed_count += 1
        
        # Summary
        logger.info(f"✅ Attack generation completed!")
        logger.info(f"📊 Generated: {generated_count} attacks")
        logger.info(f"❌ Failed: {failed_count} attacks")
        
        if use_websocket and self.sio:
            await self.sio.disconnect()

    def get_database_stats(self):
        """Get current database statistics."""
        try:
            total_attacks = self.db.query(Attack).count()
            recent_attacks = self.db.query(Attack).filter(
                Attack.timestamp >= datetime.utcnow() - timedelta(hours=24)
            ).count()
            
            countries = self.db.query(Attack.country).distinct().count()
            
            logger.info(f"📊 Database Statistics:")
            logger.info(f"   Total attacks: {total_attacks}")
            logger.info(f"   Recent attacks (24h): {recent_attacks}")
            logger.info(f"   Countries: {countries}")
            
        except Exception as e:
            logger.error(f"❌ Failed to get database stats: {e}")

    def __del__(self):
        """Cleanup database connection."""
        if hasattr(self, 'db'):
            self.db.close()

async def main():
    """Main function to run the fake attack generator."""
    parser = argparse.ArgumentParser(description="Generate fake attack data for Honeypot Attack Map")
    parser.add_argument("--count", type=int, default=50, help="Number of fake attacks to generate")
    parser.add_argument("--websocket", action="store_true", help="Send attacks via WebSocket in real-time")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between WebSocket attacks (seconds)")
    parser.add_argument("--cleanup", action="store_true", help="Clean up old attacks before generating new ones")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")
    
    args = parser.parse_args()
    
    # Create generator instance
    generator = FakeAttackGenerator()
    
    try:
        # Show current stats
        generator.get_database_stats()
        
        # Generate attacks
        await generator.generate_attacks(
            count=args.count,
            use_websocket=args.websocket,
            delay=args.delay
        )
        
        # Show final stats
        generator.get_database_stats()
        
    except KeyboardInterrupt:
        logger.info("⏹️ Attack generation interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        # Cleanup
        if hasattr(generator, 'db'):
            generator.db.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())