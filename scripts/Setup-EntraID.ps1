# PowerShell script to set up Microsoft Entra ID

# Install Microsoft Graph module with CurrentUser scope to avoid admin rights issues
Install-Module -Name Microsoft.Graph -Scope CurrentUser -Force -AllowClobber
Import-Module Microsoft.Graph

Write-Host "Connecting to Microsoft Graph..."
# Connect interactively to Microsoft Graph
Connect-MgGraph -Scopes "User.Read.All", "Group.ReadWrite.All", "Directory.ReadWrite.All" -Interactive

Write-Host "Entra ID setup script completed."
