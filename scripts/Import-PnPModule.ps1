# Script to import PnP.PowerShell module after installation

# Get the module path for the current user scope
$modulePath = Join-Path $env:USERPROFILE "Documents\PowerShell\Modules\PnP.PowerShell"

if (Test-Path $modulePath) {
    Write-Output "Importing PnP.PowerShell module from $modulePath"
    Import-Module $modulePath -Force -ErrorAction Stop
    Write-Output "PnP.PowerShell module imported successfully."
} else {
    Write-Error "PnP.PowerShell module not found in expected path: $modulePath"
    Write-Output "Please verify the module installation or restart your PowerShell session."
}
