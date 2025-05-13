param(
    [string]$AdminEmail,
    [string]$SiteUrl,
    [string]$PrimaryOwner
)

# Import the SharePoint Online Management Shell module
Import-Module Microsoft.Online.SharePoint.PowerShell -ErrorAction Stop

# Connect to SharePoint Online with interactive credential prompt
$cred = Get-Credential
Connect-SPOService -Url "https://owlban-admin.sharepoint.com" -Credential $cred

# Create the dashboard site
try {
    New-SPOSite -Url $SiteUrl -Owner $PrimaryOwner -Title "OWLban Internal Dashboard" -Template "STS#3" -StorageQuota 5000
    Write-Output "Dashboard site created at $SiteUrl"
} catch {
    Write-Error "Failed to create site: $_"
    exit 1
}

# Configure site settings
try {
    Set-SPOSite -Identity $SiteUrl -DenyAddAndCustomizePages $false
    Set-SPOUser -Site $SiteUrl -LoginName $AdminEmail -IsSiteCollectionAdmin $true
} catch {
    Write-Error "Failed to configure site settings: $_"
    exit 1
}

# Add default groups with correct cmdlet usage
try {
    # Note: New-SPOSiteGroup does not have -Name parameter, use Add-SPOUser or other cmdlets as needed
    # Here we create groups via PnP PowerShell as an alternative
    Import-Module PnP.PowerShell -ErrorAction Stop
    Connect-PnPOnline -Url $SiteUrl -Credentials $cred

    # Create groups
    New-PnPGroup -Title "Dashboard Admins" -PermissionLevels "Full Control"
    New-PnPGroup -Title "Dashboard Users" -PermissionLevels "Contribute"
} catch {
    Write-Error "Failed to create site groups: $_"
    exit 1
}
