import json
import re

import json
import re
import os

class CorporateStructureAI:
    def __init__(self, json_path=None):
        if json_path is None:
            json_path = os.path.join(os.path.dirname(__file__), 'data/corporate_structure.json')
        self.json_path = json_path
        with open(json_path, 'r') as f:
            self.data = json.load(f)

    def get_sectors(self):
        """
        Return the list of sectors in the data.
        """
        return list(self.data.keys())

    def get_companies_by_sector(self, sector):
        """
        Return the list of companies for a given sector.
        """
        return self.data.get(sector, [])

    def get_company_by_ticker(self, ticker):
        """
        Return company details by ticker (case-insensitive).
        """
        ticker = ticker.lower()
        for sector, companies in self.data.items():
            for company in companies:
                if company.get('ticker', '').lower() == ticker:
                    return company
        return "Company not found."

    def query(self, query_str):
        """
        Simple natural language query method.
        Supports queries like:
        - "companies in Technology"
        - "company with ticker MSFT"
        """
        query_str = query_str.lower()
        sector_match = re.search(r'companies in ([a-z\s]+)', query_str)
        ticker_match = re.search(r'company with ticker ([a-z]+)', query_str)

        if sector_match:
            sector = sector_match.group(1).title()
            return self.get_companies_by_sector(sector)
        elif ticker_match:
            ticker = ticker_match.group(1).upper()
            return self.get_company_by_ticker(ticker)
        else:
            return "Query not understood."

    def update_revenue(self, ticker, new_revenue):
        """
        Update the revenue for a company identified by ticker.
        Saves the updated data back to the JSON file.
        """
        updated = False
        for sector, companies in self.data.items():
            for company in companies:
                if company.get('ticker', '').lower() == ticker.lower():
                    company['revenue'] = new_revenue
                    updated = True
                    break
            if updated:
                break
        if updated:
            with open(self.json_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        return updated

if __name__ == "__main__":
    ai = CorporateStructureAI()
    print("Sectors:")
    print(ai.get_sectors())
