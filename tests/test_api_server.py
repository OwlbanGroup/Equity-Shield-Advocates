import unittest
import json
from unittest.mock import patch
from src.api_server import app

class ApiServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {'X-API-KEY': 'equity-shield-2024-secure-key'}
        self.mock_data = {
            'MSFT': {'market_cap': 1000.0, 'revenue': 500.0, 'last_updated': '2023-01-01'},
            'GOOG': {'market_cap': 2000.0, 'revenue': 800.0, 'last_updated': '2023-01-01'},
            'JPM': {'market_cap': 3000.0, 'revenue': 1200.0, 'last_updated': '2023-01-01'},
            'BAC': {'market_cap': 2500.0, 'revenue': 1000.0, 'last_updated': '2023-01-01'},
            'C': {'market_cap': 1800.0, 'revenue': 900.0, 'last_updated': '2023-01-01'},
            'PLD': {'market_cap': 1500.0, 'revenue': 600.0, 'last_updated': '2023-01-01'},
            'AMT': {'market_cap': 1700.0, 'revenue': 700.0, 'last_updated': '2023-01-01'},
            'SPG': {'market_cap': 1600.0, 'revenue': 650.0, 'last_updated': '2023-01-01'}
        }

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('version', data)

    def test_authentication(self):
        """Test API key authentication"""
        # Test without API key
        response = self.app.get('/api/corporate-structure')
        self.assertEqual(response.status_code, 401)
        
        # Test with invalid API key
        response = self.app.get('/api/corporate-structure', 
                              headers={'X-API-KEY': 'invalid-key'})
        self.assertEqual(response.status_code, 401)
        
        # Test with valid API key
        response = self.app.get('/api/corporate-structure', 
                              headers=self.headers)
        self.assertIn(response.status_code, [200, 404])

    def test_get_corporate_structure(self):
        """Test corporate structure endpoint"""
        response = self.app.get('/api/corporate-structure', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    def test_get_companies_by_sector(self):
        """Test getting companies by sector"""
        # Test valid sector
        response = self.app.get('/api/companies/Technology', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

        # Test invalid sector
        response = self.app.get('/api/companies/InvalidSector', headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_get_company_by_ticker(self):
        """Test getting company by ticker"""
        # Test valid ticker
        response = self.app.get('/api/company/MSFT', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

        # Test invalid ticker
        response = self.app.get('/api/company/INVALID', headers=self.headers)
        self.assertEqual(response.status_code, 404)

    @patch('src.api_server.load_json_file')
    def test_get_real_assets(self, mock_load):
        """Test real assets endpoint with pagination and filtering"""
        mock_load.return_value = self.mock_data

        # Test basic pagination - all on one line to avoid line continuation issues
        response = self.app.get('/api/real-assets', headers=self.headers, query_string={'page': '1', 'per_page': '10'})
        if response.status_code != 200:
            print(f"Response data: {response.data.decode('utf-8')}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('data', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total', data)

        # Test market cap filters
        response = self.app.get('/api/real-assets', headers=self.headers, query_string={'page': '1', 'per_page': '10', 'min_market_cap': '1000', 'max_market_cap': '5000'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

        # Test sorting
        response = self.app.get('/api/real-assets', headers=self.headers, query_string={'page': '1', 'per_page': '10', 'sort_by': 'market_cap', 'sort_order': 'desc'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

        # Test custom pagination
        response = self.app.get('/api/real-assets', headers=self.headers, query_string={'page': '1', 'per_page': '5'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    def test_error_handling(self):
        """Test error handling"""
        # Test 404 error
        response = self.app.get('/api/nonexistent', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
        self.assertIn('error', data)

        # Test invalid pagination parameters
        response = self.app.get('/api/real-assets', headers=self.headers, query_string={'page': 'invalid'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
