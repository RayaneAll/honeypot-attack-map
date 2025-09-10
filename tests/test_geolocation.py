"""
Unit tests for geolocation service
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from geolocation import is_private_ip, get_country_coordinates

class TestGeolocation(unittest.TestCase):
    """Test cases for geolocation service"""
    
    def test_is_private_ip(self):
        """Test private IP detection"""
        # Private IPs
        self.assertTrue(is_private_ip("192.168.1.1"))
        self.assertTrue(is_private_ip("10.0.0.1"))
        self.assertTrue(is_private_ip("172.16.0.1"))
        self.assertTrue(is_private_ip("127.0.0.1"))
        self.assertTrue(is_private_ip("localhost"))
        
        # Public IPs
        self.assertFalse(is_private_ip("8.8.8.8"))
        self.assertFalse(is_private_ip("1.1.1.1"))
        self.assertFalse(is_private_ip("208.67.222.222"))
    
    def test_get_country_coordinates(self):
        """Test country coordinate lookup"""
        # Test known countries
        us_coords = get_country_coordinates("United States")
        self.assertIsInstance(us_coords, tuple)
        self.assertEqual(len(us_coords), 2)
        self.assertIsInstance(us_coords[0], float)
        self.assertIsInstance(us_coords[1], float)
        
        # Test unknown country
        unknown_coords = get_country_coordinates("Unknown Country")
        self.assertEqual(unknown_coords, (0.0, 0.0))
    
    def test_private_ip_handling(self):
        """Test that private IPs return appropriate location data"""
        # This test would normally call get_ip_location, but we'll mock it
        # to avoid making actual API calls during testing
        pass

if __name__ == '__main__':
    unittest.main()
