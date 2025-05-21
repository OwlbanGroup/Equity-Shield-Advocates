# PowerShell script to set up automatic file synchronization with SharePoint
param(
    [Parameter(Mandatory=$true)]
    [string]$SharePointSiteUrl,
    
    [string]$LibraryName = "Documents"
)

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Install-RequiredModules {
    if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
        Write-ColorOutput "Installing PnP.PowerShell module..." "Yellow"
        Install-Module -Name PnP.PowerShell -Force -AllowClobber -Scope CurrentUser
    }
    Import-Module PnP.PowerShell -ErrorAction Stop
    Write-ColorOutput "PnP.PowerShell module loaded successfully" "Green"
}

function Test-AdminPrivileges {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-ColorOutput "This script requires administrative privileges to create scheduled tasks." "Red"
        Write-ColorOutput "Please run PowerShell as Administrator and try again." "Red"
        exit 1
    }
}

function Test-SharePointConnection {
    param(
        [string]$SiteUrl
    )
    
    try {
        Write-ColorOutput "Testing SharePoint connection..." "Blue"
        Connect-PnPOnline -Url $SiteUrl -DeviceLogin -ErrorAction Stop
        Write-ColorOutput "SharePoint connection successful" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Failed to connect to SharePoint: $($_.Exception.Message)" "Red"
        Write-Host "`nTroubleshooting steps:"
        Write-Host "1. Verify your internet connection"
        Write-Host "2. Ensure you have appropriate SharePoint permissions"
        Write-Host "3. Check if the site URL is correct"
        Write-Host "4. Try clearing your browser cache and cookies"
        return $false
    }
}

function Set-ScheduledTask {
    param(
        [string]$SharePointSiteUrl,
        [string]$LibraryName
    )
    
    try {
        Write-ColorOutput "Setting up scheduled task..." "Blue"
        
        $taskName = "EquityShield_AutoUpload"
        $scriptPath = Join-Path $PSScriptRoot "Sync-CorporateStructure-To-SharePoint.ps1"
        
        # Create action to run sync script
        $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`" -SharePointSiteUrl `"$SharePointSiteUrl`" -LibraryName `"$LibraryName`""
        
        # Create trigger for every 15 minutes
        $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)
        
        # Set principal to run with highest privileges
        $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest
        
        # Configure settings
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        
        # Register the task
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
        
        Write-ColorOutput "Scheduled task created successfully" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Failed to create scheduled task: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Main script execution
try {
    Write-ColorOutput "Starting EntraID AutoUpload Setup" "Yellow"
    Write-ColorOutput "===============================" "Yellow"
    
    # Check for admin privileges
    Test-AdminPrivileges
    
    # Install required modules
    Install-RequiredModules
    
    # Test SharePoint connection
    if (-not (Test-SharePointConnection -SiteUrl $SharePointSiteUrl)) {
        exit 1
    }
    
    # Set up scheduled task
    if (-not (Set-ScheduledTask -SharePointSiteUrl $SharePointSiteUrl -LibraryName $LibraryName)) {
        exit 1
    }
    
    Write-ColorOutput "`nSetup completed successfully!" "Green"
    Write-Host "`nYour files will now automatically sync to SharePoint every 15 minutes."
    Write-Host "You can modify the schedule in Task Scheduler under the task name 'EquityShield_AutoUpload'"
    
    exit 0
}
catch {
    Write-ColorOutput "Setup failed: $($_.Exception.Message)" "Red"
    exit 1
}
finally {
    # Ensure we disconnect from SharePoint
    try {
        Disconnect-PnPOnline -ErrorAction SilentlyContinue
    }
    catch {
        # Ignore any disconnection errors
    }
}
