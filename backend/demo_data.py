"""
Script to populate the database with demo attack data
Useful for testing and demonstration purposes
"""

import random
import time
from datetime import datetime, timedelta
from models import Attack, init_db
from geolocation import get_country_coordinates

# Demo countries with their coordinates
DEMO_COUNTRIES = [
    {'name': 'United States', 'lat': 39.8283, 'lon': -98.5795},
    {'name': 'China', 'lat': 35.8617, 'lon': 104.1954},
    {'name': 'Russia', 'lat': 61.5240, 'lon': 105.3188},
    {'name': 'Germany', 'lat': 51.1657, 'lon': 10.4515},
    {'name': 'United Kingdom', 'lat': 55.3781, 'lon': -3.4360},
    {'name': 'France', 'lat': 46.2276, 'lon': 2.2137},
    {'name': 'Japan', 'lat': 36.2048, 'lon': 138.2529},
    {'name': 'Brazil', 'lat': -14.2350, 'lon': -51.9253},
    {'name': 'India', 'lat': 20.5937, 'lon': 78.9629},
    {'name': 'Canada', 'lat': 56.1304, 'lon': -106.3468},
    {'name': 'Australia', 'lat': -25.2744, 'lon': 133.7751},
    {'name': 'South Korea', 'lat': 35.9078, 'lon': 127.7669},
    {'name': 'Italy', 'lat': 41.8719, 'lon': 12.5674},
    {'name': 'Spain', 'lat': 40.4637, 'lon': -3.7492},
    {'name': 'Netherlands', 'lat': 52.1326, 'lon': 5.2913},
    {'name': 'Poland', 'lat': 51.9194, 'lon': 19.1451},
    {'name': 'Ukraine', 'lat': 48.3794, 'lon': 31.1656},
    {'name': 'Turkey', 'lat': 38.9637, 'lon': 35.2433},
    {'name': 'Iran', 'lat': 32.4279, 'lon': 53.6880},
    {'name': 'Israel', 'lat': 31.0461, 'lon': 34.8516}
]

# Common attack ports and protocols
ATTACK_PORTS = [22, 23, 80, 443, 3389, 5432, 3306, 21, 25, 53, 110, 143, 993, 995]
PROTOCOLS = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH', 'FTP', 'SMTP']

def generate_demo_ip():
    """Generate a realistic demo IP address"""
    # Generate IPs from different ranges to simulate global attacks
    first_octet = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255])
    second_octet = random.randint(0, 255)
    third_octet = random.randint(0, 255)
    fourth_octet = random.randint(1, 254)
    
    return f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"

def create_demo_attacks(count: int = 100):
    """Create demo attack data"""
    print(f"🎭 Creating {count} demo attacks...")
    
    # Initialize database
    init_db()
    
    # Create attacks over the last 7 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    for i in range(count):
        # Random timestamp within the last 7 days
        random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
        timestamp = start_time + timedelta(seconds=random_seconds)
        
        # Random country
        country_data = random.choice(DEMO_COUNTRIES)
        
        # Add some randomness to coordinates
        lat_offset = random.uniform(-2, 2)
        lon_offset = random.uniform(-2, 2)
        
        # Create attack
        attack = Attack(
            ip_address=generate_demo_ip(),
            port=random.choice(ATTACK_PORTS),
            protocol=random.choice(PROTOCOLS),
            country=country_data['name'],
            city=f"City {random.randint(1, 100)}",
            latitude=country_data['lat'] + lat_offset,
            longitude=country_data['lon'] + lon_offset,
            timestamp=timestamp
        )
        
        attack.save()
        
        if (i + 1) % 20 == 0:
            print(f"Created {i + 1}/{count} demo attacks...")
    
    print(f"✅ Successfully created {count} demo attacks!")

def create_recent_attacks(count: int = 10):
    """Create recent attacks for real-time demo"""
    print(f"🔥 Creating {count} recent attacks...")
    
    for i in range(count):
        # Very recent timestamp (last hour)
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 60))
        
        country_data = random.choice(DEMO_COUNTRIES)
        
        attack = Attack(
            ip_address=generate_demo_ip(),
            port=random.choice(ATTACK_PORTS),
            protocol=random.choice(PROTOCOLS),
            country=country_data['name'],
            city=f"City {random.randint(1, 100)}",
            latitude=country_data['lat'] + random.uniform(-1, 1),
            longitude=country_data['lon'] + random.uniform(-1, 1),
            timestamp=timestamp
        )
        
        attack.save()
        time.sleep(0.1)  # Small delay for realistic timing
    
    print(f"✅ Successfully created {count} recent attacks!")

if __name__ == '__main__':
    print("🎭 Honeypot Demo Data Generator")
    print("=" * 40)
    
    # Create historical demo data
    create_demo_attacks(200)
    
    # Create some recent attacks
    create_recent_attacks(15)
    
    print("\n🎉 Demo data generation complete!")
    print("You can now start the honeypot server to see the data in action.")
