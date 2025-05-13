# Script to install and verify PnP.PowerShell module installation

# Install the module if not already installed
if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
    Write-Output "PnP.PowerShell module not found. Installing..."
    Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force -AllowClobber
} else {
    Write-Output "PnP.PowerShell module is already installed."
}

# Verify installation by importing the module
try {
    Import-Module PnP.PowerShell -Force -ErrorAction Stop
    Write-Output "PnP.PowerShell module imported successfully."
} catch {
    Write-Error "Failed to import PnP.PowerShell module: $_"
    Write-Output "Please restart your PowerShell session and try again."
}
