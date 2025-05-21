# Financial Data Access Guide

## 1. Local File Access

### JSON Files
- **Main Data File**: `data/corporate_data.json`
  - Contains latest financial data (market cap, revenue) for all tracked companies
  - Updated automatically by the data fetching script
  - Includes historical backups with timestamps: `data/corporate_data.json.[timestamp].bak`

### View JSON Data
```powershell
# PowerShell command to view data
Get-Content data/corporate_data.json | ConvertFrom-Json | Format-Table
```

## 2. SharePoint Access

### Online Dashboard
1. Navigate to your SharePoint site: `https://yourtenant.sharepoint.com/sites/yoursite`
2. Access the dashboard: `SitePages/Dashboard.aspx`
3. View real-time financial data visualizations

### Document Library
- Location: `Documents` library in SharePoint
- Contains synchronized JSON files:
  - corporate_structure.json
  - data/corporate_structure.json
  - data/corporate_data.json

## 3. API Access

### REST Endpoints
1. Start the API server:
```powershell
python production_server.py
```

2. Access data via API endpoints:
```powershell
# Get all financial data
curl -H "X-API-KEY: secret-api-key" http://localhost:8000/api/financial-data

# Get specific company data
curl -H "X-API-KEY: secret-api-key" http://localhost:8000/api/financial-data/MSFT
```

## 4. Automated Updates

### Manual Update
Run the data fetch script:
```powershell
python scripts/fetch_financial_data_alpha_vantage.py
```

### SharePoint Integration

#### Manual Sync
Update SharePoint with latest data manually:
```powershell
# Replace with your actual values
$clientId = "your-client-id"
$tenantName = "your-tenant-name"

./scripts/Sync-CorporateStructure-To-SharePoint.ps1 -ClientId $clientId -TenantName $tenantName
```

Required parameters:
- ClientId: Your Entra ID App Registration Client ID
- TenantName: Your SharePoint tenant name (e.g., 'contoso' for contoso.sharepoint.com)

#### Automatic File Synchronization
Set up automatic file synchronization with SharePoint:
```powershell
# Replace with your actual values
$sharePointSiteUrl = "https://yourtenant.sharepoint.com/sites/yoursite"
$libraryName = "Documents"  # Optional, defaults to "Documents"

# For first-time setup
./scripts/Setup-EntraID-AutoUpload.ps1 -SharePointSiteUrl $sharePointSiteUrl -LibraryName $libraryName

# For manual sync
./scripts/Sync-CorporateStructure-To-SharePoint.ps1 -SharePointSiteUrl $sharePointSiteUrl
```

Configuration Values:
- SharePointSiteUrl: Full URL to your SharePoint site
- LibraryName: Name of the document library (default: "Documents")

Authentication:
- Uses modern authentication with interactive browser login
- Securely stores credentials for automated tasks
- No need to manage client IDs or secrets

This will:
1. Create an Entra ID app registration with necessary permissions
2. Configure a scheduled task to sync files every 15 minutes
3. Set up secure credential storage

The following files will be automatically synchronized:
- corporate_structure.json
- data/corporate_structure.json
- data/corporate_data.json

To modify sync settings:
1. Open Task Scheduler
2. Find the task named "EquityShield_AutoUpload"
3. Adjust schedule or other settings as needed

Note: The automatic sync requires:
- Windows Task Scheduler access
- PowerShell execution policy that allows running scripts
- Active Entra ID subscription

## 5. Data Analysis and Visualization Tools

### Interactive Visualization
```powershell
# Generate financial data visualizations
python scripts/visualize_financial_data.py
```
This will create:
1. Market Cap Visualization: `data/market_cap_visualization.png`
   - Horizontal bar chart showing company market capitalizations
   - Values in billions USD
   - Companies sorted by market cap

2. Revenue Visualization: `data/revenue_visualization.png`
   - Horizontal bar chart showing company revenues
   - Values in billions USD
   - Companies sorted by revenue

3. Summary Statistics
   - Market cap and revenue statistics
   - Mean, median, standard deviation
   - Quartile distributions

### PowerShell Analysis
```powershell
# Get companies by market cap
$data = Get-Content data/corporate_data.json | ConvertFrom-Json
$data.PSObject.Properties | 
    Where-Object { $_.Value.market_cap } | 
    Sort-Object { $_.Value.market_cap } -Descending | 
    Select-Object Name, @{N='Market Cap ($B)';E={$_.Value.market_cap/1e9}} | 
    Format-Table
```

### Python Analysis
Create a Python script for analysis:
```python
import json
import pandas as pd

# Load data
with open('data/corporate_data.json') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame.from_dict(data, orient='index')
print(df.sort_values('market_cap', ascending=False))
```

## 6. Backup and Recovery

### Access Backups
```powershell
# List available backups
Get-ChildItem data/corporate_data.json.*.bak

# Restore from backup
Copy-Item data/corporate_data.json.[timestamp].bak data/corporate_data.json
```

## 7. Troubleshooting

### Common Issues
1. **Data Not Updated**
   - Check Alpha Vantage API status
   - Verify API key in script
   - Review logs for errors

2. **SharePoint Sync Failed**
   - Verify SharePoint connection
   - Check PnP.PowerShell module status
   - Review permissions

### Support
For additional assistance:
1. Check `DEPLOYMENT.md` for setup issues
2. Review `PRODUCTION_SETUP.md` for environment configuration
3. Contact the development team for urgent issues

## 8. Security Notes

- Keep your API keys secure
- Use the provided authentication headers
- Follow SharePoint security best practices
- Regularly rotate credentials
