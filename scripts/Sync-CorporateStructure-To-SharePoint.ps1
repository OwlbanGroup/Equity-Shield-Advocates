# PowerShell script to upload corporate_structure.json and data/corporate_structure.json
# to a SharePoint document library and update a dashboard

param(
    [string]$SiteUrl = "https://yourtenant.sharepoint.com/sites/yoursite",
    [string]$LibraryName = "Documents",
    [string]$LocalFilePath1 = "corporate_structure.json",
    [string]$LocalFilePath2 = "data/corporate_structure.json",
    [string]$DashboardPageUrl = "https://yourtenant.sharepoint.com/sites/yoursite/SitePages/Dashboard.aspx"
)

# Import PnP PowerShell module
if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
    Install-Module -Name PnP.PowerShell -Force -AllowClobber
}
Import-Module PnP.PowerShell

# Connect to SharePoint Online
Write-Host "Connecting to SharePoint site $SiteUrl ..."
Connect-PnPOnline -Url $SiteUrl -Interactive

# Upload corporate_structure.json
Write-Host "Uploading $LocalFilePath1 to $LibraryName ..."
Add-PnPFile -Path $LocalFilePath1 -Folder $LibraryName -Overwrite

# Upload data/corporate_structure.json
Write-Host "Uploading $LocalFilePath2 to $LibraryName ..."
Add-PnPFile -Path $LocalFilePath2 -Folder $LibraryName -Overwrite

# Optionally, refresh or update dashboard page (this depends on your dashboard implementation)
Write-Host "Dashboard page URL: $DashboardPageUrl"
Write-Host "Please manually refresh or configure your dashboard to reflect updated data."

Write-Host "Sync completed successfully."
