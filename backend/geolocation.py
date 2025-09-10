"""
IP geolocation service using free APIs
"""

import requests
import time
from typing import Dict, Any, Optional

# Cache to avoid repeated API calls for same IP
location_cache = {}

def get_ip_location(ip_address: str) -> Dict[str, Any]:
    """
    Get geolocation data for an IP address
    Uses ip-api.com (free, no API key required)
    """
    
    # Check cache first
    if ip_address in location_cache:
        return location_cache[ip_address]
    
    # Skip private/local IPs
    if is_private_ip(ip_address):
        location = {
            'country': 'Private',
            'city': 'Local Network',
            'latitude': 0.0,
            'longitude': 0.0,
            'region': 'Private',
            'timezone': 'UTC'
        }
        location_cache[ip_address] = location
        return location
    
    try:
        # Use ip-api.com (free, 1000 requests/minute)
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                location = {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'latitude': float(data.get('lat', 0.0)),
                    'longitude': float(data.get('lon', 0.0)),
                    'region': data.get('regionName', 'Unknown'),
                    'timezone': data.get('timezone', 'UTC'),
                    'isp': data.get('isp', 'Unknown')
                }
            else:
                # Fallback for failed lookup
                location = {
                    'country': 'Unknown',
                    'city': 'Unknown',
                    'latitude': 0.0,
                    'longitude': 0.0,
                    'region': 'Unknown',
                    'timezone': 'UTC'
                }
        else:
            # Fallback for API error
            location = {
                'country': 'Unknown',
                'city': 'Unknown',
                'latitude': 0.0,
                'longitude': 0.0,
                'region': 'Unknown',
                'timezone': 'UTC'
            }
    
    except Exception as e:
        print(f"Error getting location for {ip_address}: {e}")
        # Fallback for any error
        location = {
            'country': 'Unknown',
            'city': 'Unknown',
            'latitude': 0.0,
            'longitude': 0.0,
            'region': 'Unknown',
            'timezone': 'UTC'
        }
    
    # Cache the result
    location_cache[ip_address] = location
    
    # Rate limiting (ip-api.com allows 1000 requests/minute)
    time.sleep(0.1)
    
    return location

def is_private_ip(ip_address: str) -> bool:
    """Check if IP address is private/local"""
    try:
        parts = ip_address.split('.')
        if len(parts) != 4:
            return True
        
        first_octet = int(parts[0])
        
        # Private IP ranges
        if first_octet == 10:
            return True
        elif first_octet == 172 and 16 <= int(parts[1]) <= 31:
            return True
        elif first_octet == 192 and int(parts[1]) == 168:
            return True
        elif first_octet == 127:  # localhost
            return True
        
        return False
    except:
        return True

def get_country_coordinates(country_name: str) -> tuple:
    """Get approximate coordinates for a country (fallback)"""
    country_coords = {
        'United States': (39.8283, -98.5795),
        'China': (35.8617, 104.1954),
        'Russia': (61.5240, 105.3188),
        'Germany': (51.1657, 10.4515),
        'United Kingdom': (55.3781, -3.4360),
        'France': (46.2276, 2.2137),
        'Japan': (36.2048, 138.2529),
        'Brazil': (-14.2350, -51.9253),
        'India': (20.5937, 78.9629),
        'Canada': (56.1304, -106.3468)
    }
    
    return country_coords.get(country_name, (0.0, 0.0))
