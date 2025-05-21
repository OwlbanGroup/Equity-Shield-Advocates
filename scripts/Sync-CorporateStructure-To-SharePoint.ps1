# PowerShell script to upload corporate_structure.json, data/corporate_structure.json, and data/corporate_data.json
# to a SharePoint document library and update a dashboard

param(
    [Parameter(Mandatory=$true)]
    [string]$SharePointSiteUrl,
    
    [string]$LibraryName = "Documents",
    [string]$LocalFilePath1 = "corporate_structure.json",
    [string]$LocalFilePath2 = "data/corporate_structure.json",
    [string]$LocalFilePath3 = "data/corporate_data.json"
)

# Set dashboard URL based on site URL
$DashboardPageUrl = $SharePointSiteUrl + "/SitePages/Dashboard.aspx"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check and install required modules
function Install-RequiredModules {
    if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
        Write-ColorOutput "Installing PnP.PowerShell module..." "Yellow"
        Install-Module -Name PnP.PowerShell -Force -AllowClobber -Scope CurrentUser
    }
    Import-Module PnP.PowerShell -ErrorAction Stop
    Write-ColorOutput "PnP.PowerShell module loaded successfully" "Green"
}

# Function to connect to SharePoint
function Connect-ToSharePoint {
    param(
        [string]$SiteUrl
    )
    
    try {
        Write-ColorOutput "Connecting to SharePoint site $SiteUrl..." "Blue"
        
        # Use app registration authentication with client id and secret
        $clientId = "<YOUR_CLIENT_ID>"
        $clientSecret = "<YOUR_CLIENT_SECRET>"
        $tenantId = "<YOUR_TENANT_ID>"
        $secureSecret = ConvertTo-SecureString $clientSecret -AsPlainText -Force
        $credentials = New-Object System.Management.Automation.PSCredential($clientId, $secureSecret)
        Connect-PnPOnline -Url $SiteUrl -ClientId $clientId -ClientSecret $secureSecret -Tenant $tenantId -ErrorAction Stop
        Write-ColorOutput "Connected successfully" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Failed to connect to SharePoint: $($_.Exception.Message)" "Red"
        Write-Host "`nTroubleshooting steps:"
        Write-Host "1. Verify your internet connection"
        Write-Host "2. Ensure you have appropriate SharePoint permissions"
        Write-Host "3. Check if the site URL is correct"
        Write-Host "4. Try clearing your browser cache and cookies"
        return $false
    }
}

# Function to upload file with error handling
function Add-FileToSharePoint {
    param(
        [string]$FilePath,
        [string]$Folder
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-ColorOutput "File not found: $FilePath" "Red"
        return $false
    }
    
    try {
        Write-ColorOutput "Uploading $FilePath to $Folder..." "Blue"
        Add-PnPFile -Path $FilePath -Folder $Folder -ErrorAction Stop
        Write-ColorOutput "Upload successful" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Failed to upload $FilePath" "Red"
        Write-ColorOutput $_.Exception.Message "Red"
        return $false
    }
}

# Main script execution
try {
    Write-ColorOutput "Starting SharePoint Sync" "Yellow"
    Write-ColorOutput "====================" "Yellow"
    
    # Install and import required modules
    Install-RequiredModules
    
    # Connect to SharePoint
    if (-not (Connect-ToSharePoint -SiteUrl $SharePointSiteUrl)) {
        return $false
    }
    
    # Upload files
    $uploadSuccess = $true
    $uploadSuccess = $uploadSuccess -and (Add-FileToSharePoint -FilePath $LocalFilePath1 -Folder $LibraryName)
    $uploadSuccess = $uploadSuccess -and (Add-FileToSharePoint -FilePath $LocalFilePath2 -Folder $LibraryName)
    $uploadSuccess = $uploadSuccess -and (Add-FileToSharePoint -FilePath $LocalFilePath3 -Folder $LibraryName)
    
    if ($uploadSuccess) {
        Write-ColorOutput "`nAll files uploaded successfully!" "Green"
        Write-Host "`nDashboard page URL: $DashboardPageUrl"
        Write-Host "Please manually refresh or configure your dashboard to reflect updated data."
        return $true
    }
    else {
        Write-ColorOutput "`nSome files failed to upload. Please check the error messages above." "Red"
        return $false
    }
}
catch {
    Write-ColorOutput "Sync failed: $($_.Exception.Message)" "Red"
    return $false
}
finally {
    # Ensure we disconnect from SharePoint
    try {
        Disconnect-PnPOnline -ErrorAction SilentlyContinue
    }
    catch {
        # Ignore any disconnection errors
    }
}
