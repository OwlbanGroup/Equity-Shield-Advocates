import unittest
import json
from api_server import app

class ApiServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_corporate_structure(self):
        response = self.app.get('/api/corporate-structure')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    def test_get_companies_by_sector_valid(self):
        response = self.app.get('/api/companies/Technology')
        # 200 or 404 depending on data presence
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_get_companies_by_sector_invalid(self):
        response = self.app.get('/api/companies/NonExistentSector')
        self.assertEqual(response.status_code, 404)

    def test_get_company_by_ticker_valid(self):
        # Assuming 'MSFT' is a valid ticker in data
        response = self.app.get('/api/company/MSFT')
        # 200 or 404 depending on data presence
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, dict)

    def test_get_company_by_ticker_invalid(self):
        response = self.app.get('/api/company/INVALIDTICKER')
        self.assertEqual(response.status_code, 404)

    def test_get_real_assets(self):
        response = self.app.get('/api/real-assets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_companies_by_sector_empty_string(self):
        response = self.app.get('/api/companies/')
        self.assertIn(response.status_code, [404, 405])

    def test_get_company_by_ticker_empty_string(self):
        response = self.app.get('/api/company/')
        self.assertIn(response.status_code, [404, 405])

    def test_get_company_by_ticker_case_insensitive(self):
        # Assuming 'msft' lowercase ticker should work same as 'MSFT'
        response_upper = self.app.get('/api/company/MSFT')
        response_lower = self.app.get('/api/company/msft')
        self.assertEqual(response_upper.status_code, response_lower.status_code)
        if response_upper.status_code == 200:
            self.assertEqual(json.loads(response_upper.data), json.loads(response_lower.data))

if __name__ == '__main__':
    unittest.main()
