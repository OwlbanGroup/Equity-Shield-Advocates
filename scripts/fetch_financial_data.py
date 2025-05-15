import requests

def fetch_company_financials(ticker):
    """
    Fetch financial data for a company given its ticker symbol.
    This example uses the Yahoo Finance unofficial API.
    """
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=financialData"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        financial_data = data['quoteSummary']['result'][0]['financialData']
        market_cap = financial_data['marketCap']['raw'] if financial_data.get('marketCap') else None
        revenue = financial_data['totalRevenue']['raw'] if financial_data.get('totalRevenue') else None
        return {
            'ticker': ticker,
            'market_cap': market_cap,
            'revenue': revenue
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

if __name__ == "__main__":
    # Example tickers to fetch
    tickers = ["MSFT", "GOOG", "JPM", "BAC", "C", "PLD", "AMT", "SPG", "EQH", "OAS", "OASPQ", "JSEOAS"]
    results = []
    for ticker in tickers:
        data = fetch_company_financials(ticker)
        if data:
            results.append(data)
    print(results)
