import unittest
from unittest.mock import patch, mock_open
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import extract_corporate_data as ecd

class TestExtractCorporateData(unittest.TestCase):

    def setUp(self):
        self.sample_md = """
## Executive Summary
This is the executive summary.

## Fund Overview
Overview of the fund.

## Investment Strategy
Strategy details.

## Team Structure
Team details.

## Total Assets Under Management (AUM)
| Company | Value |
|---------|-------|
| A       | 100   |
| B       | 200   |

## Risk Assessment
Risk details.
"""

    def test_parse_markdown(self):
        data = ecd.parse_markdown(self.sample_md)
        self.assertIn('Executive Summary', data)
        self.assertIn('Fund Overview', data)
        self.assertIn('Investment Strategy', data)
        self.assertIn('Team Structure', data)
        self.assertIn('AUM', data)
        self.assertIn('Risk Assessment', data)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_json(self, mock_file):
        data = {"key": "value"}
        ecd.save_json(data, "test.json")
        mock_file.assert_called_with("test.json", "w")

    @patch('builtins.open', new_callable=mock_open)
    @patch('re.search')
    def test_save_csv_from_table(self, mock_search, mock_file):
        # Mock the regex search to simulate a table match
        mock_match = mock_search.return_value
        mock_match.group.return_value = """| Header1 | Header2 |
|---------|---------|
| val1    | val2    |
| val3    | val4    |
"""
        md_text = "dummy markdown text"
        ecd.save_csv_from_table(md_text, "test.csv")
        # The open call should be triggered due to mocked regex match
        self.assertTrue(mock_file.called)

if __name__ == '__main__':
    unittest.main()
