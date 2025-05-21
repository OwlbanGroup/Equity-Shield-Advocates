# Test script for production deployment verification
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

function Test-ProductionEnvironment {
    Write-Host "`nTesting Production Environment..." -ForegroundColor Blue
    
    try {
        # Test PowerShell version
        $psVersion = $PSVersionTable.PSVersion
        $psVersionOk = $psVersion.Major -ge 5
        Write-TestResult "PowerShell version" $psVersionOk "Version: $psVersion"
        
        # Test PnP.PowerShell module
        $pnpModule = Get-Module -ListAvailable -Name PnP.PowerShell
        Write-TestResult "PnP.PowerShell module" ($null -ne $pnpModule) "Version: $($pnpModule.Version)"
        
        # Test scheduled task existence
        $task = Get-ScheduledTask -TaskName "EquityShield_AutoUpload" -ErrorAction SilentlyContinue
        Write-TestResult "Scheduled task" ($null -ne $task) "Status: $($task.State)"
        
        # Return overall status
        return $psVersionOk -and ($null -ne $pnpModule) -and ($null -ne $task)
    }
    catch {
        Write-TestResult "Production environment" $false $_.Exception.Message
        return $false
    }
}

function Test-SharePointAccess {
    Write-Host "`nTesting SharePoint Access..." -ForegroundColor Blue
    
    try {
        # Test connection
        Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin -ErrorAction Stop
        Write-TestResult "SharePoint connection" $true
        
        # Test library access
        $library = Get-PnPList -Identity $LibraryName -ErrorAction Stop
        Write-TestResult "Library access" ($null -ne $library) "Library: $LibraryName"
        
        # Test file operations
        $testFile = "production_test.txt"
        Set-Content $testFile "Test content"
        
        try {
            Add-PnPFile -Path $testFile -Folder $LibraryName -ErrorAction Stop
            Write-TestResult "File upload" $true
            
            Remove-PnPFile -ServerRelativeUrl "$LibraryName/$testFile" -Force -ErrorAction Stop
            Write-TestResult "File deletion" $true
            
            return $true
        }
        finally {
            Remove-Item $testFile -Force -ErrorAction SilentlyContinue
        }
    }
    catch {
        Write-TestResult "SharePoint access" $false $_.Exception.Message
        return $false
    }
}

function Test-AutomatedSync {
    Write-Host "`nTesting Automated Sync..." -ForegroundColor Blue
    
    try {
        # Create test file
        $testFile = "sync_test.json"
        Set-Content $testFile '{"test": "automated sync"}'
        
        # Run sync script
        $scriptPath = Join-Path $PSScriptRoot "Sync-CorporateStructure-To-SharePoint.ps1"
        $syncSuccess = & $scriptPath -SharePointSiteUrl $SharePointSiteUrl -LocalFilePath1 $testFile
        Write-TestResult "Automated sync" $syncSuccess
        
        # Verify file exists in SharePoint
        $file = Get-PnPFile -Url "$LibraryName/$testFile" -ErrorAction SilentlyContinue
        $fileExists = $null -ne $file
        Write-TestResult "File verification" $fileExists
        
        # Cleanup
        if ($fileExists) {
            Remove-PnPFile -ServerRelativeUrl "$LibraryName/$testFile" -Force -ErrorAction SilentlyContinue
        }
        Remove-Item $testFile -Force -ErrorAction SilentlyContinue
        
        return $syncSuccess -and $fileExists
    }
    catch {
        Write-TestResult "Automated sync" $false $_.Exception.Message
        return $false
    }
}

# Run all tests
Write-Host "Starting Production Deployment Tests" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

$envOk = Test-ProductionEnvironment
$accessOk = Test-SharePointAccess
$syncOk = Test-AutomatedSync

# Overall status
$allTestsPassed = $envOk -and $accessOk -and $syncOk
Write-Host "`nOverall Test Status:" -ForegroundColor Yellow
Write-TestResult "Production deployment" $allTestsPassed

if ($allTestsPassed) {
    Write-Host "`nProduction deployment verified successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nProduction deployment verification failed. Please review the test results above." -ForegroundColor Red
    exit 1
}
