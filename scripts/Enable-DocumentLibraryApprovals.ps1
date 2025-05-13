<#
.SYNOPSIS
    Configures document library approval workflows in SharePoint Online
    
.DESCRIPTION
    This script automates the setup of document approval workflows in SharePoint Online,
    including versioning, content approval, and Power Automate flow configuration.
    
.PARAMETER ConfigPath
    Path to JSON configuration file
    
.EXAMPLE
    .\Enable-DocumentLibraryApprovals.ps1 -ConfigPath ".\config.json"
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$ConfigPath
)

# Import configuration
try {
    $config = Get-Content $ConfigPath | ConvertFrom-Json
    $SiteUrl = $config.SiteUrl
    $LibraryName = $config.LibraryName
    $Approvers = $config.Approvers
    $LogPath = $config.LogPath
}
catch {
    Write-Error "Failed to load configuration: $_"
    exit 1
}

# Initialize logging
function Write-Log {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $message" | Out-File $LogPath -Append
    Write-Host $message
}

try {
    # Connect to SharePoint
    Write-Log "Connecting to SharePoint site: $SiteUrl"
    Connect-PnPOnline -Url $SiteUrl -Interactive -ErrorAction Stop
    
    # Configure library settings
    Write-Log "Configuring $LibraryName library settings"
    Set-PnPList -Identity $LibraryName `
        -EnableVersioning $true `
        -EnableModeration $true `
        -MajorVersionLimit 50 `
        -MajorWithMinorVersionsLimit 500 `
        -ErrorAction Stop
    
    # Create approval flow
    Write-Log "Creating approval workflow for $LibraryName"
    $flowParams = @{
        "DisplayName" = "$LibraryName Approval Flow"
        "Template" = "SharePoint File Approval"
        "Site" = $SiteUrl
        "List" = $LibraryName
        "Approvers" = $Approvers
    }
    
    # Save flow configuration
    $flowParams | ConvertTo-Json -Depth 5 | Out-File ".\flow-config.json"
    
    Write-Log "Successfully configured approvals for $LibraryName"
    return $true
}
catch {
    Write-Log "ERROR: $_"
    Write-Log "Stack Trace: $($_.ScriptStackTrace)"
    return $false
}
