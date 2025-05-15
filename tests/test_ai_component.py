import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_component import CorporateStructureAI

class TestCorporateStructureAI(unittest.TestCase):
    def setUp(self):
        self.ai = CorporateStructureAI()

    def test_get_sectors(self):
        sectors = self.ai.get_sectors()
        self.assertIsInstance(sectors, list)
        self.assertTrue(len(sectors) > 0)

    def test_get_companies_by_sector_valid(self):
        sectors = self.ai.get_sectors()
        if sectors:
            companies = self.ai.get_companies_by_sector(sectors[0])
            self.assertIsInstance(companies, list)

    def test_get_companies_by_sector_invalid(self):
        companies = self.ai.get_companies_by_sector("NonExistentSector")
        self.assertEqual(companies, [])

    def test_query_valid_sector(self):
        sectors = self.ai.get_sectors()
        if sectors:
            query_str = f"companies in {sectors[0]}"
            result = self.ai.query(query_str)
            if result == "Query not understood.":
                self.fail("Query method returned 'Query not understood.' for a valid sector")
            else:
                self.assertIsInstance(result, list)

    def test_query_invalid_sector(self):
        result = self.ai.query("companies in NonExistentSector")
        # The AI returns an empty list if sector not found, so adjust test accordingly
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
