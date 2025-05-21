# Production Server Deployment Instructions

## Quick Start

1. **Stop any running Python processes**
   ```powershell
   taskkill /F /IM python.exe
   ```

2. **Start the Production Server**
   ```powershell
   python production_server.py
   ```
   The server will start on http://0.0.0.0:8000

## Testing the API

1. **Test Basic Connectivity**
   ```powershell
   curl -H "X-API-KEY: secret-api-key" http://localhost:8000/api/ping
   ```
   Expected response: `{"message":"pong"}`

2. **Get Bank Account Information**
   ```powershell
   curl -H "X-API-KEY: secret-api-key" http://localhost:8000/api/banks/citi-private-bank/account
   ```

3. **Make a Transfer**
   ```powershell
   curl -X POST -H "Content-Type: application/json" -H "X-API-KEY: secret-api-key" -d "{\"from_bank\":\"citi-private-bank\",\"to_bank\":\"jpmorgan-chase\",\"amount\":1000}" http://localhost:8000/api/banks/transfer
   ```

## Environment Configuration

The `production.env` file contains all necessary settings:
- Server configuration (host, port, threads)
- API key
- Bank account information
- Logging settings

To modify settings:
1. Edit production.env
2. Restart the server

## Troubleshooting

1. **Server Won't Start**
   - Check if port 8000 is in use
   - Verify Python is installed
   - Check production.env exists

2. **API Returns 401**
   - Verify X-API-KEY header matches production.env

3. **API Returns 500**
   - Check production.log for errors
   - Verify bank account information in production.env

## Windows Service Deployment (Administrator Only)

1. **Install as Service**
   ```powershell
   # Run PowerShell as Administrator
   ./scripts/deploy_production.ps1
   ```

2. **Manage Service**
   ```powershell
   # Start service
   Start-Service EquityShieldAPI

   # Stop service
   Stop-Service EquityShieldAPI

   # Restart service
   Restart-Service EquityShieldAPI
   ```

3. **View Service Status**
   ```powershell
   Get-Service EquityShieldAPI
   ```

## Monitoring

1. **View Logs**
   ```powershell
   Get-Content -Path production.log -Tail 20 -Wait
   ```

2. **Test Service Health**
   ```powershell
   curl -H "X-API-KEY: secret-api-key" http://localhost:8000/api/ping
   ```

## Security Notes

1. Keep production.env secure and never commit to version control
2. Regularly rotate the API key
3. Monitor access logs for suspicious activity
4. Keep dependencies updated

## Support

For additional assistance:
1. Check PRODUCTION_SETUP.md for detailed configuration
2. Review DEPLOYMENT_AND_TESTING.md for testing procedures
3. Contact the development team for urgent issues
