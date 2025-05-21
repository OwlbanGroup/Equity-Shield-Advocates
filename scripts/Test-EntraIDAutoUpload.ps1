# Test script for EntraID auto-upload functionality
param(
    [Parameter(Mandatory=$true)]
    [string]$SharePointSiteUrl,
    
    [string]$LibraryName = "Documents"
)

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Success,
        [string]$Message = ""
    )
    
    if ($Success) {
        Write-Host "✓ $TestName" -ForegroundColor Green
    } else {
        Write-Host "✗ $TestName" -ForegroundColor Red
        if ($Message) {
            Write-Host "  $Message" -ForegroundColor Red
        }
    }
}

function Test-ModuleInstallation {
    Write-Host "`nTesting Module Installation..." -ForegroundColor Blue
    
    try {
        Import-Module PnP.PowerShell -ErrorAction Stop
        Write-TestResult "PnP.PowerShell module installation" $true
    }
    catch {
        Write-TestResult "PnP.PowerShell module installation" $false $_.Exception.Message
    }
}

function Test-SharePointConnection {
    Write-Host "`nTesting SharePoint Connection..." -ForegroundColor Blue
    
    try {
        Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin -ErrorAction Stop
        Write-TestResult "SharePoint connection" $true
        
        # Test basic operations
        $web = Get-PnPWeb
        if ($web) {
            Write-TestResult "SharePoint web access" $true
        } else {
            Write-TestResult "SharePoint web access" $false "Could not access SharePoint web"
        }
    }
    catch {
        Write-TestResult "SharePoint connection" $false $_.Exception.Message
    }
}

function Test-FileOperations {
    Write-Host "`nTesting File Operations..." -ForegroundColor Blue
    
    try {
        # Create test file
        $testFile = "test_upload.json"
        Set-Content $testFile '{"test": "data"}'
        
        # Test upload
        Add-PnPFile -Path $testFile -Folder $LibraryName -ErrorAction Stop
        Write-TestResult "File upload" $true
        
        # Test download
        $downloadPath = "test_download.json"
        Get-PnPFile -Url "$LibraryName/$testFile" -Path $downloadPath -AsFile -Force
        
        if (Test-Path $downloadPath) {
            Write-TestResult "File download" $true
            Remove-Item $downloadPath -Force
        } else {
            Write-TestResult "File download" $false "Downloaded file not found"
        }
        
        # Test deletion
        Remove-PnPFile -ServerRelativeUrl "$LibraryName/$testFile" -Force
        Write-TestResult "File deletion" $true
    }
    catch {
        Write-TestResult "File operations" $false $_.Exception.Message
    }
    finally {
        Remove-Item $testFile -Force -ErrorAction SilentlyContinue
    }
}

function Test-TaskScheduler {
    Write-Host "`nTesting Task Scheduler..." -ForegroundColor Blue
    
    try {
        # Check if running with admin privileges
        $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if (-not $isAdmin) {
            Write-TestResult "Task scheduler access" $false "This test requires administrative privileges"
            return
        }
        
        # Test task creation
        $taskName = "TestAutoUpload"
        $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"Write-Host 'Test'`""
        $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
        $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest
        
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null
        Write-TestResult "Task creation" $true
        
        # Clean up
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-TestResult "Task cleanup" $true
    }
    catch {
        Write-TestResult "Task scheduler" $false $_.Exception.Message
    }
}

# Run all tests
Write-Host "Starting EntraID AutoUpload Tests" -ForegroundColor Yellow
Write-Host "==============================" -ForegroundColor Yellow

Test-ModuleInstallation
Test-SharePointConnection
Test-FileOperations
Test-TaskScheduler

Write-Host "`nTesting completed!" -ForegroundColor Yellow
