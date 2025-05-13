import unittest
from ai_nl_query import NaturalLanguageQuery

class TestNaturalLanguageQuery(unittest.TestCase):
    def setUp(self):
        self.nlq = NaturalLanguageQuery()

    def test_list_sectors(self):
        result = self.nlq.execute_query("List sectors")
        self.assertIsInstance(result, list)

    def test_companies_in_sector(self):
        result = self.nlq.execute_query("Show companies in sector Technology")
        self.assertIsInstance(result, list)

    def test_unknown_query(self):
        result = self.nlq.execute_query("What is the weather?")
        self.assertEqual(result, "Sorry, I did not understand the query.")

if __name__ == '__main__':
    unittest.main()
