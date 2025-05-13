import re
from ai_component import CorporateStructureAI

class NaturalLanguageQuery:
    def __init__(self):
        self.ai = CorporateStructureAI()

    def parse_query(self, query):
        """
        Basic parsing of natural language query to extract intent and parameters.
        """
        query = query.lower()
        if "sector" in query:
            match = re.search(r'sector\s+(\w+)', query)
            if match:
                return ("sector", match.group(1))
            else:
                return ("list_sectors", None)
        elif "company" in query:
            match = re.search(r'company\s+(\w+)', query)
            if match:
                return ("company", match.group(1))
        return ("unknown", None)

    def execute_query(self, query):
        intent, param = self.parse_query(query)
        if intent == "sector":
            return self.ai.get_companies_by_sector(param)
        elif intent == "list_sectors":
            return self.ai.get_sectors()
        elif intent == "company":
            # For simplicity, return company info by ticker if implemented
            return f"Company info for {param} not implemented."
        else:
            return "Sorry, I did not understand the query."

if __name__ == "__main__":
    nlq = NaturalLanguageQuery()
    print(nlq.execute_query("List sectors"))
    print(nlq.execute_query("Show companies in sector Technology"))
    print(nlq.execute_query("Get company ABC"))
