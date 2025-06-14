# PowerShell script to deploy and configure Microsoft Intune

# Install Microsoft.Graph module for Intune management with CurrentUser scope
Install-Module -Name Microsoft.Graph -Scope CurrentUser -Force -AllowClobber
Import-Module Microsoft.Graph

Write-Host "Connecting to Microsoft Graph..."
Connect-MgGraph -Scopes "DeviceManagementConfiguration.ReadWrite.All", "DeviceManagementManagedDevices.ReadWrite.All"

# Example: Create a device compliance policy
$policyName = "EquityShieldCompliancePolicy"
$policyDescription = "Compliance policy for Equity Shield Advocates devices"

Write-Host "Creating device compliance policy: $policyName"

$policy = @{
    displayName = $policyName
    description = $policyDescription
    platform = "windows10AndLater"
    # Add compliance settings here as needed
}

New-MgDeviceManagementDeviceCompliancePolicy -BodyParameter $policy

Write-Host "Intune deployment script completed."
