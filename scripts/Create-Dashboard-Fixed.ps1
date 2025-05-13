param(
    [string]$AdminEmail,
    [string]$SiteUrl,
    [string]$PrimaryOwner
)

# Import the PnP PowerShell module instead of Microsoft.Online.SharePoint.PowerShell
Import-Module PnP.PowerShell -ErrorAction Stop

# Connect to SharePoint Online interactively
try {
    Connect-PnPOnline -Url $SiteUrl -Interactive
    Write-Output "Connected to SharePoint Online at $SiteUrl"
} catch {
    Write-Error "Failed to connect to SharePoint Online: $_"
    exit 1
}

# Create the dashboard site using PnP PowerShell
try {
    # PnP PowerShell does not have New-SPOSite equivalent, so use SPO cmdlet via Invoke-Command or admin center
    # Here we assume the site already exists or is created manually
    Write-Output "Please create the site manually in SharePoint Admin Center if it does not exist."
} catch {
    Write-Error "Failed to create site: $_"
    exit 1
}

# Configure site settings and permissions
try {
    # Set site permissions
    Set-PnPSite -Identity $SiteUrl -DenyAddAndCustomizePages $false

    # Add site collection admin
    Set-PnPUser -Identity $AdminEmail -IsSiteCollectionAdmin $true

    # Create groups
    New-PnPGroup -Title "Dashboard Admins" -PermissionLevels "Full Control"
    New-PnPGroup -Title "Dashboard Users" -PermissionLevels "Contribute"

    Write-Output "Dashboard site configured successfully."
} catch {
    Write-Error "Failed to configure site settings: $_"
    exit 1
}
