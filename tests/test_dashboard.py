import unittest
import requests
import json
import time
from time import sleep

class TestDashboard(unittest.TestCase):
    API_BASE_URL = 'http://localhost:5001'
    ENDPOINTS = [
        '/health',
        '/api/v1/corporate-data',
        '/api/v1/corporate-structure',
        '/api/v1/real-assets'
    ]

    def test_health_endpoint(self):
        """Test health endpoint returns correct status"""
        response = requests.get(f"{self.API_BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)
        self.assertIn('timestamp', data)

    def test_corporate_data_endpoint(self):
        """Test corporate data endpoint returns valid data"""
        response = requests.get(f"{self.API_BASE_URL}/api/v1/corporate-data")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data'], list)
        self.assertTrue(len(data['data']) > 0)
        self.assertIn('name', data['data'][0])
        self.assertIn('type', data['data'][0])
        self.assertIn('status', data['data'][0])

    def test_corporate_structure_endpoint(self):
        """Test corporate structure endpoint returns valid data"""
        response = requests.get(f"{self.API_BASE_URL}/api/v1/corporate-structure")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data'], list)
        self.assertTrue(len(data['data']) > 0)
        self.assertIn('department', data['data'][0])

    def test_real_assets_endpoint(self):
        """Test real assets endpoint returns valid data"""
        response = requests.get(f"{self.API_BASE_URL}/api/v1/real-assets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data'], list)
        self.assertTrue(len(data['data']) > 0)
        self.assertIn('name', data['data'][0])
        self.assertIn('type', data['data'][0])
        self.assertIn('value', data['data'][0])

    def test_error_handling(self):
        """Test error handling for non-existent endpoint"""
        response = requests.get(f"{self.API_BASE_URL}/non-existent")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)

    def test_data_validation(self):
        """Test data validation for all endpoints"""
        for endpoint in self.ENDPOINTS:
            response = requests.get(f"{self.API_BASE_URL}{endpoint}")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('status', data)
            if endpoint != '/health':
                self.assertIn('data', data)

    def test_response_time(self):
        """Test response time for all endpoints"""
        for endpoint in self.ENDPOINTS:
            start_time = time.time()
            response = requests.get(f"{self.API_BASE_URL}{endpoint}")
            end_time = time.time()
            
            # Response time should be less than 3 seconds
            self.assertLess(end_time - start_time, 3.0)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
