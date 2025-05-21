# Bank Account Setup Instructions

## Environment Variables Setup

To securely store your bank account information, this application uses environment variables. Follow these steps to set up your banking information:

1. Locate the `.env` file in the root directory
2. Replace the placeholder values with your actual bank account information:
   ```
   CITI_ACCOUNT_NUMBER=your_actual_citi_account_number
   CITI_ROUTING_NUMBER=your_actual_citi_routing_number
   JPMORGAN_ACCOUNT_NUMBER=your_actual_jpmorgan_account_number
   JPMORGAN_ROUTING_NUMBER=your_actual_jpmorgan_routing_number
   ```

## Security Notes

- The `.env` file is automatically ignored by git (via .gitignore) to prevent sensitive data from being committed
- Never commit your actual bank account numbers to the repository
- Keep your `.env` file secure and do not share it
- For development/testing, you can use the mock values from `.env.example`

## Required Python Packages

Make sure you have the required package for environment variable handling:
```bash
pip install python-dotenv
```

## Verification

To verify your bank account setup:
1. Start the API server: `python run_api_server.py`
2. Test the banking endpoints with your API key:
   ```bash
   curl -H "X-API-KEY: secret-api-key" http://localhost:5001/api/banks/citi-private-bank/account
   curl -H "X-API-KEY: secret-api-key" http://localhost:5001/api/banks/jpmorgan-chase/account
   ```

Your actual bank account numbers will be used when the environment variables are set, otherwise, the system will fall back to mock values for testing.
