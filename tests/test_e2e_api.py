import unittest
import json
from src.api_server import create_app

class EndToEndApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_corporate_structure_flow(self):
        # Get corporate structure
        response = self.app.get('/api/corporate-structure')
        self.assertEqual(response.status_code, 200)
        structure = json.loads(response.data)
        self.assertIsInstance(structure, dict)

        # For each sector, get companies and then company details
        for sector in structure.keys():
            response = self.app.get(f'/api/companies/{sector}')
            if response.status_code == 200:
                companies = json.loads(response.data)
                self.assertIsInstance(companies, list)
                for company in companies:
                    ticker = company.get('ticker')
                    if ticker:
                        response = self.app.get(f'/api/company/{ticker}')
                        self.assertIn(response.status_code, [200, 404])
                        if response.status_code == 200:
                            company_detail = json.loads(response.data)
                            self.assertIsInstance(company_detail, dict)

    def test_real_assets_endpoint(self):
        response = self.app.get('/api/real-assets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_banking_info_endpoint(self):
        response = self.app.get('/api/banking-info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('routing_number', data)
        self.assertIn('account_number', data)
        self.assertIn('ein_number', data)

    def test_invalid_endpoints(self):
        # Invalid sector
        response = self.app.get('/api/companies/InvalidSector')
        self.assertEqual(response.status_code, 404)

        # Invalid ticker
        response = self.app.get('/api/company/INVALID')
        self.assertEqual(response.status_code, 404)

        # Empty sector
        response = self.app.get('/api/companies/')
        self.assertEqual(response.status_code, 400)

        # Empty ticker
        response = self.app.get('/api/company/')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
