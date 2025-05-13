import unittest
import json
from unittest.mock import patch
import src.api_server as api_server

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api_server.app.test_client()
        self.app.testing = True

    def test_full_corporate_structure_flow(self):
        # Get full corporate structure
        response = self.app.get('/api/corporate-structure')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

        # Pick a sector if available
        sectors = list(data.keys())
        if sectors:
            sector = sectors[0]
            # Get companies by sector
            response = self.app.get(f'/api/companies/{sector}')
            self.assertIn(response.status_code, [200, 404])
            if response.status_code == 200:
                companies = json.loads(response.data)
                self.assertIsInstance(companies, list)
                if companies:
                    ticker = companies[0].get('ticker')
                    if ticker:
                        # Get company by ticker
                        response = self.app.get(f'/api/company/{ticker}')
                        self.assertIn(response.status_code, [200, 404])
                        if response.status_code == 200:
                            company = json.loads(response.data)
                            self.assertIsInstance(company, dict)

    def test_real_assets_flow(self):
        # Get real assets
        response = self.app.get('/api/real-assets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    @patch('src.api_server.load_corporate_structure', return_value={})
    def test_edge_case_empty_corporate_structure(self, mock_load):
        # Test API response when corporate structure is empty
        response = self.app.get('/api/corporate-structure')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {})

    def test_edge_case_invalid_sector(self):
        # Test API response for invalid sector
        response = self.app.get('/api/companies/InvalidSector')
        self.assertEqual(response.status_code, 404)
        # Check if response data is JSON and contains 'error' key
        try:
            data = json.loads(response.get_data(as_text=True))
            self.assertIn('error', data)
        except Exception as e:
            print("Response data:", response.get_data(as_text=True))
            print("Exception:", e)
            self.fail("Response is not valid JSON or missing 'error' key")

    def test_edge_case_invalid_ticker(self):
        # Test API response for invalid ticker
        response = self.app.get('/api/company/INVALID')
        self.assertEqual(response.status_code, 404)
        # Check if response data is JSON and contains 'error' key
        try:
            data = json.loads(response.get_data(as_text=True))
            self.assertIn('error', data)
        except Exception as e:
            print("Response data:", response.get_data(as_text=True))
            print("Exception:", e)
            self.fail("Response is not valid JSON or missing 'error' key")

    def test_edge_case_empty_sector(self):
        # Test API response for empty sector string
        response = self.app.get('/api/companies/')
        self.assertEqual(response.status_code, 400)

    def test_edge_case_empty_ticker(self):
        # Test API response for empty ticker string
        response = self.app.get('/api/company/')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
