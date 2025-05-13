param(
    [string]$ConfigPath = ".\\config.json",
    [string]$LANSharedFolder = "\\192.168.1.1\SharedData"
)

# Import PnP PowerShell module
Import-Module PnP.PowerShell -ErrorAction Stop

# Load config
$config = Get-Content $ConfigPath | ConvertFrom-Json

# Connect to SharePoint Online
Connect-PnPOnline -Url $config.SiteUrl -Interactive

# Get target document library
$libraryName = $config.LibraryName

# Verify LAN shared folder path accessibility
if (-not (Test-Path $LANSharedFolder)) {
    Write-Error "LAN shared folder path '$LANSharedFolder' is not accessible. Please verify the network path."
    exit 1
}

# Upload dashboard page to Site Pages library
$dashboardFilePath = $config.DashboardFilePath
$dashboardFileName = $config.DashboardFile

if (Test-Path $dashboardFilePath) {
    Write-Host "Uploading dashboard page $dashboardFileName to SharePoint Site Pages library..."
    Add-PnPFile -Path $dashboardFilePath -Folder "SitePages" -Overwrite
    Write-Host "Dashboard page uploaded successfully."
} else {
    Write-Warning "Dashboard file $dashboardFilePath not found. Skipping upload."
}

# Upload or sync files from LAN shared folder to SharePoint document library
Write-Host "Uploading files from $LANSharedFolder to SharePoint library $libraryName..."

$files = Get-ChildItem -Path $LANSharedFolder -Recurse -File

foreach ($file in $files) {
    $relativePath = $file.FullName.Substring($LANSharedFolder.Length).TrimStart('\')
    $targetFolder = Split-Path $relativePath -Parent
    $targetFolder = if ($targetFolder) { $targetFolder } else { "" }

    # Ensure target folder exists in SharePoint
    if ($targetFolder -ne "") {
        $folderExists = Get-PnPFolder -Url $targetFolder -ErrorAction SilentlyContinue
        if (-not $folderExists) {
            Write-Host "Creating folder $targetFolder in SharePoint library..."
            New-PnPFolder -Name $targetFolder -Folder $libraryName
        }
    }

    # Upload file
    $targetUrl = if ($targetFolder -ne "") { "$targetFolder/$($file.Name)" } else { $file.Name }
    Write-Host "Uploading $($file.FullName) to $targetUrl"
    Add-PnPFile -Path $file.FullName -Folder $targetFolder -Overwrite
}

Write-Host "Upload complete."

# Optionally trigger dashboard refresh (if applicable)
# You can call Setup-Refresh.ps1 or trigger refresh jobs here if needed
