# Quick Deployment Instructions

## 1. Open PowerShell as Administrator
1. Press Win + X
2. Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

## 2. Navigate to Project Directory
```powershell
cd "c:/Users/Dell/OneDrive/Documents/GitHub/Equity-Shield-Advocates"
```

## 3. Set Execution Policy
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
```

## 4. Install Chocolatey (if not installed)
```powershell
[System.Net.ServicePoint]::SecurityProtocol = [System.Net.ServicePoint]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

## 5. Run Deployment Script
```powershell
./scripts/deploy_production.ps1
```

## 6. Verify Installation
After deployment completes:
1. Check service status:
```powershell
Get-Service EquityShieldAPI
```

2. Test API endpoint:
```powershell
curl -H "X-API-KEY: secret-api-key" http://localhost:8000/api/ping
```

## Troubleshooting
If you encounter any issues:
1. Check Windows Event Viewer for service errors
2. Review production.log for application errors
3. Ensure all environment variables are set correctly in production.env

For detailed setup and configuration options, refer to PRODUCTION_SETUP.md
