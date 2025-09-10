#!/usr/bin/env python3
"""
Test runner for all honeypot tests
"""

import unittest
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def run_tests():
    """Run all tests"""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
