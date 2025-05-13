# Wrapper script to run Sync-LANDataToSharePoint.ps1 with robust module check and user guidance

function Import-PnPModule {
    $module = Get-Module -ListAvailable -Name PnP.PowerShell
    if ($module) {
        Import-Module PnP.PowerShell -ErrorAction Stop
        return $true
    }
    return $false
}

if (-not (Import-PnPModule)) {
    Write-Warning "PnP.PowerShell module not found. Attempting to install..."
    try {
        Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force -AllowClobber
        if (-not (Import-PnPModule)) {
            Write-Error "Failed to import PnP.PowerShell module after installation."
            exit 1
        }
    } catch {
        Write-Error "Failed to install PnP.PowerShell module. Please install it manually."
        exit 1
    }
}

# Verify LAN shared folder path accessibility
$LANSharedFolder = "\\192.168.1.1\SharedData"
if (-not (Test-Path $LANSharedFolder)) {
    Write-Error "LAN shared folder path '$LANSharedFolder' is not accessible. Please verify the network path."
    exit 1
}

# Run the sync script
.\Sync-LANDataToSharePoint.ps1 -ConfigPath ".\config.json" -LANSharedFolder $LANSharedFolder
