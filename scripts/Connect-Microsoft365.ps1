# PowerShell script to authenticate and connect to Microsoft 365 services

# Install required modules
Install-Module -Name Microsoft.Graph -Force -AllowClobber
Import-Module Microsoft.Graph

Write-Host "Connecting to Microsoft 365 services..."
Connect-MgGraph -Scopes "User.Read.All", "Group.ReadWrite.All", "Device.ReadWrite.All", "Policy.ReadWrite.ConditionalAccess"

Write-Host "Connection to Microsoft 365 established."
