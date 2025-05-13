import unittest
import os
import json
from ai_component import CorporateStructureAI

class TestCorporateStructureAI(unittest.TestCase):
    def setUp(self):
        self.ai = CorporateStructureAI()
        self.test_ticker = "MSFT"
        self.original_data = None
        # Backup original data
        with open(self.ai.json_path, 'r') as f:
            self.original_data = json.load(f)

    def tearDown(self):
        # Restore original data
        with open(self.ai.json_path, 'w') as f:
            json.dump(self.original_data, f, indent=4)

    def test_update_revenue_success(self):
        new_revenue = 999999999
        updated = self.ai.update_revenue(self.test_ticker, new_revenue)
        self.assertTrue(updated)
        # Reload data to verify
        with open(self.ai.json_path, 'r') as f:
            data = json.load(f)
        found = False
        for sector, companies in data.items():
            for company in companies:
                if company.get('ticker') == self.test_ticker:
                    self.assertEqual(company.get('revenue'), new_revenue)
                    found = True
        self.assertTrue(found)

    def test_update_revenue_failure(self):
        updated = self.ai.update_revenue("INVALID", 12345)
        self.assertFalse(updated)

if __name__ == '__main__':
    unittest.main()
