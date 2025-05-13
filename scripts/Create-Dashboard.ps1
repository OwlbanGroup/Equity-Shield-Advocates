# OWLban Dashboard Creation Script
param(
    [string]$AdminEmail,
    [string]$SiteUrl,
    [string]$PrimaryOwner
)

# Connect to SharePoint
Connect-SPOService -Url "https://owlban-admin.sharepoint.com" -Credential (Get-Credential)

# Create dashboard site
New-SPOSite -Url $SiteUrl -Owner $PrimaryOwner -Title "OWLban Internal Dashboard" -Template "STS#3" -StorageQuota 5000

# Configure site settings
Set-SPOSite -Identity $SiteUrl -DenyAddAndCustomizePages $false
Set-SPOUser -Site $SiteUrl -LoginName $AdminEmail -IsSiteCollectionAdmin $true

# Add default groups
New-SPOSiteGroup -Site $SiteUrl -Name "Dashboard Admins" -PermissionLevels "Full Control"
New-SPOSiteGroup -Site $SiteUrl -Name "Dashboard Users" -PermissionLevels "Contribute"

Write-Output "Dashboard site created at $SiteUrl"
