import requests
import json
import os
import shutil
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = "demo"  # Using demo key for initial testing

def fetch_company_financials(ticker):
    """
    Fetch financial data for a company given its ticker symbol using Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    try:
        logger.info(f"Fetching data for {ticker}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "Note" in data:  # API rate limit hit
            logger.warning(f"API rate limit reached: {data['Note']}")
            return None
            
        market_cap = int(data.get('MarketCapitalization')) if data.get('MarketCapitalization') else None
        revenue = int(data.get('RevenueTTM')) if data.get('RevenueTTM') else None
        
        logger.info(f"Successfully fetched data for {ticker}")
        return {
            'ticker': ticker,
            'market_cap': market_cap,
            'revenue': revenue,
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching data for {ticker}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Data parsing error for {ticker}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching data for {ticker}: {e}")
        return None

def backup_file(file_path):
    """
    Create a backup of the specified file with timestamp.
    """
    if os.path.exists(file_path):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = f"{file_path}.{timestamp}.bak"
        try:
            shutil.copyfile(file_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    return False

def update_corporate_data_file(results, file_path):
    """
    Update the corporate data file with new financial data while preserving existing data.
    """
    try:
        # Load existing data
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # Create backup before modifying
        if not backup_file(file_path):
            logger.error("Failed to create backup, aborting update")
            return False

        # Update only the financial data, preserving other fields
        for item in results:
            if item and 'ticker' in item:
                ticker = item['ticker']
                if ticker in data:
                    # Update only financial fields
                    data[ticker].update({
                        'market_cap': item['market_cap'],
                        'revenue': item['revenue'],
                        'last_updated': item['last_updated']
                    })
                else:
                    # Add new ticker data
                    data[ticker] = {
                        'market_cap': item['market_cap'],
                        'revenue': item['revenue'],
                        'last_updated': item['last_updated']
                    }

        # Write updated data back to file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully updated corporate data file: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error updating corporate data file: {e}")
        return False

def validate_response(data):
    """
    Validate the API response data.
    """
    required_fields = ['MarketCapitalization', 'RevenueTTM']
    return all(field in data for field in required_fields)

if __name__ == "__main__":
    # Test tickers (including some that might fail)
    tickers = ["MSFT", "GOOG", "JPM", "BAC", "C", "PLD", "AMT", "SPG", "EQH", "OAS", "OASPQ", "JSEOAS"]
    results = []
    success_count = 0
    failure_count = 0
    
    logger.info("Starting financial data fetch process")
    
    for ticker in tickers:
        try:
            data = fetch_company_financials(ticker)
            if data:
                results.append(data)
                success_count += 1
                logger.info(f"Successfully processed {ticker}")
            else:
                failure_count += 1
                logger.warning(f"Failed to fetch data for {ticker}")
            
            # Respect API rate limits (5 calls per minute for free tier)
            time.sleep(12)  # 12 second delay between calls
            
        except Exception as e:
            failure_count += 1
            logger.error(f"Error processing {ticker}: {e}")
    
    logger.info(f"Fetch process completed. Successes: {success_count}, Failures: {failure_count}")
    
    # Update the corporate_data.json file with live data
    corporate_data_file = os.path.join(os.path.dirname(__file__), '../data/corporate_data.json')
    if update_corporate_data_file(results, corporate_data_file):
        logger.info("Corporate data file updated successfully")
    else:
        logger.error("Failed to update corporate data file")
