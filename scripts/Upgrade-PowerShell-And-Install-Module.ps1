# Script to upgrade PowerShell to latest stable version and install PnP.PowerShell module

# Step 1: Upgrade PowerShell using winget (requires Windows 10/11 and winget installed)
Write-Host "Upgrading PowerShell to latest version using winget..."
winget install --id Microsoft.PowerShell --source winget --accept-source-agreements --accept-package-agreements

# Step 2: Verify PowerShell version after upgrade
Write-Host "Please restart your PowerShell session after upgrade."
Write-Host "Current PowerShell version:"
$PSVersionTable.PSVersion

# Step 3: Install PnP.PowerShell module for current user
Write-Host "Installing PnP.PowerShell module for current user..."
try {
    Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force -AllowClobber
    Write-Host "PnP.PowerShell module installed successfully."
} catch {
    Write-Error "Failed to install PnP.PowerShell module. $_"
    exit 1
}

# Step 4: Import the module to verify installation
try {
    Import-Module PnP.PowerShell -Force -ErrorAction Stop
    Write-Host "PnP.PowerShell module imported successfully."
} catch {
    Write-Error "Failed to import PnP.PowerShell module. Please restart PowerShell and try again."
    exit 1
}
