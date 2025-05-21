# Deployment and Testing Guide

## Deployment Steps

### 1. Prerequisites
- Windows Server or Windows 10/11 Pro
- Python 3.x
- Administrator privileges
- PowerShell

### 2. Initial Setup
1. Open PowerShell as Administrator:
   - Press Win + X
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. Navigate to project directory:
   ```powershell
   cd "c:/Users/Dell/OneDrive/Documents/GitHub/Equity-Shield-Advocates"
   ```

3. Set execution policy:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   ```

### 3. Environment Configuration
1. Copy environment template:
   ```powershell
   Copy-Item production.env.example production.env
   ```

2. Update production.env with your values:
   ```
   PRODUCTION_HOST=0.0.0.0
   PRODUCTION_PORT=8000
   WAITRESS_THREADS=4
   API_KEY=your_secure_api_key
   CITI_ACCOUNT_NUMBER=your_actual_number
   CITI_ROUTING_NUMBER=your_actual_number
   JPMORGAN_ACCOUNT_NUMBER=your_actual_number
   JPMORGAN_ROUTING_NUMBER=your_actual_number
   ```

### 4. Deploy Production Server
Run the deployment script:
```powershell
./scripts/deploy_production.ps1
```

This will:
- Install required packages
- Configure the Windows service
- Start the production server

## Testing Steps

### 1. Run Comprehensive Tests
Execute the test suite:
```powershell
./scripts/test_production_deployment.ps1
```

The test suite verifies:

1. Service Management
   - Service installation
   - Start/Stop/Restart operations
   - Status monitoring

2. API Endpoints
   - Bank account information retrieval
   - Transfer functionality
   - Routing number validation
   - Authentication checks

3. Error Handling
   - Unauthorized access responses
   - Invalid endpoint handling
   - Malformed request handling

4. Load Testing
   - Concurrent request processing
   - Response time monitoring
   - Service stability under load

5. Security Configuration
   - API key validation
   - CORS headers
   - SSL/TLS settings (if configured)

### 2. Manual Verification
After automated tests complete:

1. Check service status:
   ```powershell
   Get-Service EquityShieldAPI
   ```

2. Monitor logs:
   ```powershell
   Get-Content -Path production.log -Tail 20 -Wait
   ```

3. Test API manually:
   ```powershell
   # Test ping endpoint
   curl -H "X-API-KEY: your_api_key" http://localhost:8000/api/ping

   # Test bank account endpoint
   curl -H "X-API-KEY: your_api_key" http://localhost:8000/api/banks/citi-private-bank/account
   ```

## Troubleshooting

### Service Issues
1. Check Windows Event Viewer
2. Review production.log
3. Verify environment variables
4. Check service account permissions

### API Issues
1. Confirm service is running
2. Verify API key in requests
3. Check endpoint URLs
4. Review error responses

### Performance Issues
1. Monitor CPU/Memory usage
2. Check concurrent connection limits
3. Review Waitress thread configuration
4. Analyze response times

## Security Checklist

- [ ] Environment variables properly set
- [ ] API keys securely stored
- [ ] SSL/TLS configured (if required)
- [ ] Firewall rules configured
- [ ] Access logs enabled
- [ ] Regular security updates planned

## Maintenance

### Regular Tasks
1. Monitor logs
2. Update dependencies
3. Rotate API keys
4. Backup configuration
5. Test backups

### Emergency Procedures
1. Stop service:
   ```powershell
   Stop-Service EquityShieldAPI
   ```

2. Backup logs:
   ```powershell
   Copy-Item production.log "logs/production_$(Get-Date -Format 'yyyyMMdd').log"
   ```

3. Restore service:
   ```powershell
   Start-Service EquityShieldAPI
   ```

For additional assistance, refer to PRODUCTION_SETUP.md or contact the development team.
