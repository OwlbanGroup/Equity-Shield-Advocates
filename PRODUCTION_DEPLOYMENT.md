# Production Deployment Guide

## Overview
This guide explains how to deploy the application in a production environment using the Waitress WSGI server.

## Prerequisites
- Python 3.x
- Required packages:
  ```bash
  pip install waitress python-dotenv flask
  ```

## Configuration
1. Create a `.env` file in the root directory with your production settings:
   ```
   # Bank Account Information (Required)
   CITI_ACCOUNT_NUMBER=your_actual_citi_account_number
   CITI_ROUTING_NUMBER=your_actual_citi_routing_number
   JPMORGAN_ACCOUNT_NUMBER=your_actual_jpmorgan_account_number
   JPMORGAN_ROUTING_NUMBER=your_actual_jpmorgan_routing_number

   # Production Server Settings (Optional)
   PRODUCTION_HOST=0.0.0.0
   PRODUCTION_PORT=8000
   WAITRESS_THREADS=4
   ```

## Deployment Steps

1. Stop any running development servers

2. Start the production server:
   ```bash
   python production_server.py
   ```

3. The server will start on http://0.0.0.0:8000 by default

## Security Notes
- Always use HTTPS in production
- Set appropriate firewall rules
- Keep your `.env` file secure and never commit it to version control
- Regularly update dependencies
- Monitor server logs for suspicious activities

## Testing Production Setup
Test the production endpoints:
```bash
# Test bank account info endpoint
curl http://localhost:8000/api/banks/citi-private-bank/account

# Test transfer endpoint
curl -X POST http://localhost:8000/api/transfer \
  -H "Content-Type: application/json" \
  -d '{"from_bank": "citi-private-bank", "to_bank": "jpmorgan-chase", "amount": 1000}'
```

## Monitoring
- Use logging to monitor application behavior
- Check server logs for errors and performance issues
- Monitor system resources (CPU, memory, disk usage)

## Troubleshooting
If you encounter issues:
1. Check the logs for error messages
2. Verify environment variables are set correctly
3. Ensure all required packages are installed
4. Check system resources and server status

## Performance Tuning
Adjust these settings in your `.env` file for optimal performance:
- `WAITRESS_THREADS`: Number of threads (default: 4)
- `PRODUCTION_PORT`: Server port (default: 8000)
