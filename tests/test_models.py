"""
Unit tests for database models
"""

import unittest
import sqlite3
import os
import tempfile
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Attack, init_db, get_recent_attacks, get_attack_stats

class TestModels(unittest.TestCase):
    """Test cases for database models"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        
        # Override DB_PATH for testing
        import models
        models.DB_PATH = self.test_db.name
        
        # Initialize test database
        init_db()
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.test_db.name)
    
    def test_attack_creation(self):
        """Test creating an attack record"""
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
        
        self.assertIsNotNone(attack.id)
        self.assertEqual(attack.ip_address, "192.168.1.1")
        self.assertEqual(attack.port, 22)
        self.assertEqual(attack.protocol, "SSH")
    
    def test_attack_retrieval(self):
        """Test retrieving attack by ID"""
        attack = Attack(
            ip_address="10.0.0.1",
            port=80,
            protocol="HTTP",
            country="Test Country",
            city="Test City",
            latitude=0.0,
            longitude=0.0,
            timestamp=datetime.now()
        )
        attack.save()
        
        retrieved_attack = Attack.get_by_id(attack.id)
        
        self.assertIsNotNone(retrieved_attack)
        self.assertEqual(retrieved_attack.ip_address, "10.0.0.1")
        self.assertEqual(retrieved_attack.port, 80)
        self.assertEqual(retrieved_attack.protocol, "HTTP")
    
    def test_get_recent_attacks(self):
        """Test getting recent attacks"""
        # Create test attacks
        for i in range(5):
            attack = Attack(
                ip_address=f"192.168.1.{i+1}",
                port=22 + i,
                protocol="SSH",
                country="Test Country",
                city="Test City",
                latitude=40.7128,
                longitude=-74.0060,
                timestamp=datetime.now()
            )
            attack.save()
        
        recent_attacks = get_recent_attacks(limit=3)
        
        self.assertEqual(len(recent_attacks), 3)
        self.assertEqual(recent_attacks[0].ip_address, "192.168.1.5")  # Most recent
    
    def test_get_recent_attacks_with_filters(self):
        """Test getting recent attacks with filters"""
        # Create attacks with different countries
        countries = ["USA", "China", "USA", "Russia"]
        for i, country in enumerate(countries):
            attack = Attack(
                ip_address=f"192.168.1.{i+1}",
                port=22,
                protocol="SSH",
                country=country,
                city="Test City",
                latitude=40.7128,
                longitude=-74.0060,
                timestamp=datetime.now()
            )
            attack.save()
        
        # Filter by country
        usa_attacks = get_recent_attacks(country="USA")
        self.assertEqual(len(usa_attacks), 2)
        
        # Filter by protocol
        ssh_attacks = get_recent_attacks(protocol="SSH")
        self.assertEqual(len(ssh_attacks), 4)
    
    def test_get_attack_stats(self):
        """Test getting attack statistics"""
        # Create test attacks
        attacks_data = [
            ("192.168.1.1", 22, "SSH", "USA"),
            ("192.168.1.2", 80, "HTTP", "China"),
            ("192.168.1.3", 22, "SSH", "USA"),
            ("192.168.1.4", 443, "HTTPS", "Russia"),
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
        
        stats = get_attack_stats()
        
        self.assertEqual(stats['total_attacks'], 4)
        self.assertEqual(len(stats['top_countries']), 3)  # USA, China, Russia
        self.assertEqual(len(stats['protocol_stats']), 3)  # SSH, HTTP, HTTPS
        
        # Check that USA has 2 attacks
        usa_count = next((c['count'] for c in stats['top_countries'] if c['country'] == 'USA'), 0)
        self.assertEqual(usa_count, 2)

if __name__ == '__main__':
    unittest.main()
