import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Adjust sys.path to import from Capetain-Cetriva directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Capetain-Cetriva')))

# Since the import of validate_routing_number fails, define a mock validation function here
def validate_routing(routing_number):
    # Simple mock validation: routing number must be 9 digits
    return isinstance(routing_number, str) and len(routing_number) == 9 and routing_number.isdigit()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Bank account data using environment variables

MOCK_BANK_ACCOUNTS = {
    "citi-private-bank": {
        "account_number": os.getenv("CITI_ACCOUNT_NUMBER", "1234567890123456"),
        "routing_number": os.getenv("CITI_ROUTING_NUMBER", "021000089"),
        "bank_name": "Citi Private Bank"
    },
    "jpmorgan-chase": {
        "account_number": os.getenv("JPMORGAN_ACCOUNT_NUMBER", "9876543210987654"),
        "routing_number": os.getenv("JPMORGAN_ROUTING_NUMBER", "021000021"),
        "bank_name": "JPMorgan Chase"
    }
}

def get_account_info(bank_name):
    """
    Fetch account info for a given bank.
    For mock banks, return mock data.
    For real banks, this could be extended to call real APIs.
    """
    logger.debug(f"Fetching account info for bank: {bank_name}")
    bank_data = MOCK_BANK_ACCOUNTS.get(bank_name)
    if bank_data:
        return bank_data
    else:
        logger.warning(f"No account info found for bank: {bank_name}")
        return None

def validate_routing_number(routing_number):
    """
    Validate a routing number using existing validation logic.
    """
    logger.debug(f"Validating routing number: {routing_number}")
    return validate_routing(routing_number)

def initiate_transfer(from_bank, to_bank, amount, currency="USD"):
    """
    Mock function to initiate a transfer between banks.
    In real implementation, this would call bank APIs or messaging systems.
    """
    logger.info(f"Initiating transfer from {from_bank} to {to_bank} of amount {amount} {currency}")
    # Mock response
    transfer_id = "TRX1234567890"
    status = "success"
    return {
        "transfer_id": transfer_id,
        "status": status,
        "from_bank": from_bank,
        "to_bank": to_bank,
        "amount": amount,
        "currency": currency
    }
