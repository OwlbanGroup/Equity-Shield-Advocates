# This script installs the PnP.PowerShell module for the current user

try {
    Write-Host "Installing PnP.PowerShell module..."
    Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force -AllowClobber
    Write-Host "PnP.PowerShell module installed successfully."
} catch {
    Write-Error "Failed to install PnP.PowerShell module. $_"
    exit 1
}

# Verify installation
$module = Get-Module -ListAvailable -Name PnP.PowerShell
if ($module) {
    Write-Host "PnP.PowerShell module is available."
} else {
    Write-Error "PnP.PowerShell module installation verification failed."
    exit 1
}
