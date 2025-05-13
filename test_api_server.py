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
        # Check for sector keys instead of old keys
        self.assertIn('Financial Services', data)
        self.assertIn('Technology', data)
        self.assertIn('Real Estate', data)
        self.assertIn('Communication Services', data)

if __name__ == '__main__':
    unittest.main()
