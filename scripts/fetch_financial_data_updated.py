import requests
import json
import os
import shutil
import time

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

def backup_file(file_path):
    if os.path.exists(file_path):
        backup_path = file_path + ".bak"
        shutil.copyfile(file_path, backup_path)
        print(f"Backup created: {backup_path}")

def update_corporate_data_file(results, file_path):
    # Load existing data
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    # Update data with fetched financials keyed by ticker
    for item in results:
        ticker = item['ticker']
        data[ticker] = {
            'market_cap': item['market_cap'],
            'revenue': item['revenue']
        }

    # Backup existing file
    backup_file(file_path)

    # Write updated data back to file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Updated corporate data file: {file_path}")

if __name__ == "__main__":
    # Example tickers to fetch
    tickers = ["MSFT", "GOOG", "JPM", "BAC", "C", "PLD", "AMT", "SPG", "EQH", "OAS", "OASPQ", "JSEOAS"]
    results = []
    for ticker in tickers:
        data = fetch_company_financials(ticker)
        if data:
            results.append(data)
        time.sleep(2)  # Delay to avoid hitting API rate limits
    print(results)

    # Update the corporate_data.json file with live data
    corporate_data_file = os.path.join(os.path.dirname(__file__), '../data/corporate_data.json')
    update_corporate_data_file(results, corporate_data_file)
