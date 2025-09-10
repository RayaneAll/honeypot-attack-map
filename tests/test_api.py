"""
Unit tests for API endpoints
"""

import unittest
import json
import tempfile
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app
from models import init_db, Attack
from datetime import datetime

class TestAPI(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        # Create temporary database
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        
        # Override DB_PATH for testing
        import models
        models.DB_PATH = self.test_db.name
        
        # Initialize test database
        init_db()
        
        # Create test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.test_db.name)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('honeypots', data)
    
    def test_attacks_endpoint(self):
        """Test attacks endpoint"""
        # Create test attack
        attack = Attack(
            ip_address="192.168.1.1",
            port=22,
            protocol="SSH",
            country="Test Country",
            city="Test City",
            latitude=40.7128,
            longitude=-74.0060,
            timestamp=datetime.now()
        )
        attack.save()
        
        response = self.client.get('/api/attacks')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['ip_address'], "192.168.1.1")
    
    def test_attacks_endpoint_with_filters(self):
        """Test attacks endpoint with filters"""
        # Create test attacks
        attacks_data = [
            ("192.168.1.1", 22, "SSH", "USA"),
            ("192.168.1.2", 80, "HTTP", "China"),
        ]
        
        for ip, port, protocol, country in attacks_data:
            attack = Attack(
                ip_address=ip,
                port=port,
                protocol=protocol,
                country=country,
                city="Test City",
                latitude=40.7128,
                longitude=-74.0060,
                timestamp=datetime.now()
            )
            attack.save()
        
        # Test country filter
        response = self.client.get('/api/attacks?country=USA')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['country'], 'USA')
        
        # Test protocol filter
        response = self.client.get('/api/attacks?protocol=SSH')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['protocol'], 'SSH')
    
    def test_stats_endpoint(self):
        """Test stats endpoint"""
        # Create test attacks
        attack = Attack(
            ip_address="192.168.1.1",
            port=22,
            protocol="SSH",
            country="Test Country",
            city="Test City",
            latitude=40.7128,
            longitude=-74.0060,
            timestamp=datetime.now()
        )
        attack.save()
        
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('total_attacks', data)
        self.assertIn('recent_attacks_24h', data)
        self.assertIn('top_countries', data)
        self.assertIn('protocol_stats', data)
        
        self.assertEqual(data['total_attacks'], 1)

if __name__ == '__main__':
    unittest.main()
