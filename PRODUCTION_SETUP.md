# Production Setup and Deployment Guide

## Overview
This guide explains how to deploy and manage the Equity Shield Advocates API in a production environment using Windows Service and Waitress WSGI server.

## Prerequisites
- Windows Server or Windows 10/11 Pro
- Python 3.x
- Administrator privileges
- Chocolatey package manager

## Step 1: Environment Setup

1. Install required packages:
```powershell
pip install waitress python-dotenv flask
```

2. Configure environment variables:
   - Copy `production.env.example` to `production.env`
   - Update with your actual values:
     - Bank account numbers
     - API keys
     - Server settings

## Step 2: Deploy as Windows Service

1. Open PowerShell as Administrator
2. Navigate to project directory
3. Run deployment script:
```powershell
./scripts/deploy_production.ps1
```

The script will:
- Install NSSM (Non-Sucking Service Manager)
- Create Windows service
- Configure environment variables
- Start the service
- Test API endpoints

## Step 3: Verify Deployment

Test the API endpoints:
```powershell
# Test bank account endpoint
curl -H "X-API-KEY: your_api_key" http://localhost:8000/api/banks/citi-private-bank/account

# Test transfer endpoint
curl -X POST -H "Content-Type: application/json" -H "X-API-KEY: your_api_key" `
     -d "{\"from_bank\":\"citi-private-bank\",\"to_bank\":\"jpmorgan-chase\",\"amount\":1000}" `
     http://localhost:8000/api/banks/transfer
```

## Managing the Service

Common service management commands:
```powershell
# Start service
Start-Service EquityShieldAPI

# Stop service
Stop-Service EquityShieldAPI

# Restart service
Restart-Service EquityShieldAPI

# Check status
Get-Service EquityShieldAPI
```

## Monitoring and Logs

1. Check Windows Event Viewer for service logs
2. Monitor `production.log` for application logs
3. Use Windows Performance Monitor for resource usage

## Security Best Practices

1. Protect sensitive files:
   - Secure `production.env`
   - Restrict file permissions
   - Never commit sensitive data to version control

2. Network security:
   - Configure Windows Firewall
   - Use HTTPS in production
   - Implement rate limiting

## Troubleshooting

1. Service fails to start:
   - Check Event Viewer logs
   - Verify environment variables
   - Check Python path in service config

2. API endpoint issues:
   - Verify service is running
   - Check API key authentication
   - Validate request format

## Maintenance

1. Regular updates:
```powershell
Stop-Service EquityShieldAPI
pip install --upgrade -r requirements.txt
Start-Service EquityShieldAPI
```

2. Backup procedures:
   - Backup configuration files
   - Document custom settings
   - Version control deployment scripts

For additional assistance, contact the development team or refer to the technical documentation.
