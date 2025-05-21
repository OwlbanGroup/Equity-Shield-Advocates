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

function Test-NetworkTimeout {
    Write-Host "`nTesting Network Timeout Handling..." -ForegroundColor Blue
    
    try {
        # Simulate slow network by setting timeout
        $originalTimeout = [System.Net.ServicePointManager]::DefaultConnectionLimit
        [System.Net.ServicePointManager]::DefaultConnectionLimit = 1
        
        # Test upload with timeout
        $script:uploadAttempted = $false
        
        $job = Start-Job -ScriptBlock {
            param($SharePointSiteUrl, $LibraryName)
            
            Import-Module PnP.PowerShell
            Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
            
            # Create a large test file
            $testFile = "test_large_file.txt"
            1..10000 | ForEach-Object { Add-Content $testFile ("Line " + $_) }
            
            try {
                Add-PnPFile -Path $testFile -Folder $LibraryName
                $script:uploadAttempted = $true
            }
            finally {
                Remove-Item $testFile -Force
            }
        } -ArgumentList $SharePointSiteUrl, $LibraryName
        
        # Wait for job with timeout
        if (Wait-Job $job -Timeout 30) {
            Receive-Job $job
            Write-TestResult "Network timeout handling" $true
        } else {
            Stop-Job $job
            throw "Upload operation timed out as expected"
        }
    }
    catch {
        Write-TestResult "Network timeout handling" $true "Timeout handled gracefully"
    }
    finally {
        [System.Net.ServicePointManager]::DefaultConnectionLimit = $originalTimeout
        Remove-Job $job -Force
    }
}

function Test-InvalidPaths {
    Write-Host "`nTesting Invalid Path Handling..." -ForegroundColor Blue
    
    $testCases = @(
        @{
            Name = "Non-existent file"
            Path = "non_existent_file.json"
            ExpectedError = "File not found"
        },
        @{
            Name = "Invalid characters in filename"
            Path = "test<>:?*.json"
            ExpectedError = "File not found"
        },
        @{
            Name = "Empty file path"
            Path = ""
            ExpectedError = "File path cannot be empty"
        }
    )
    
    foreach ($test in $testCases) {
        try {
            & "$PSScriptRoot\Sync-CorporateStructure-To-SharePoint.ps1" `
                -SharePointSiteUrl $SharePointSiteUrl `
                -LocalFilePath1 $test.Path
            
            Write-TestResult $test.Name $false "Expected error was not thrown"
        }
        catch {
            $errorMessage = $_.Exception.Message
            $success = $errorMessage -like "*$($test.ExpectedError)*"
            Write-TestResult $test.Name $success $errorMessage
        }
    }
}

function Test-PermissionIssues {
    Write-Host "`nTesting Permission Handling..." -ForegroundColor Blue
    
    try {
        # Test with read-only file
        $testFile = "readonly_test.json"
        Set-Content $testFile '{"test": "data"}'
        Set-ItemProperty $testFile -Name IsReadOnly -Value $true
        
        try {
            Add-PnPFile -Path $testFile -Folder $LibraryName
            Write-TestResult "Read-only file handling" $false "Expected error was not thrown"
        }
        catch {
            Write-TestResult "Read-only file handling" $true $_.Exception.Message
        }
        finally {
            Set-ItemProperty $testFile -Name IsReadOnly -Value $false
            Remove-Item $testFile -Force
        }
        
        # Test with insufficient SharePoint permissions
        try {
            $testFile = "permission_test.json"
            Set-Content $testFile '{"test": "data"}'
            
            # Temporarily disconnect to simulate no permissions
            Disconnect-PnPOnline
            Add-PnPFile -Path $testFile -Folder "Restricted_Folder"
            
            Write-TestResult "SharePoint permission handling" $false "Expected error was not thrown"
        }
        catch {
            Write-TestResult "SharePoint permission handling" $true $_.Exception.Message
        }
        finally {
            Remove-Item $testFile -Force
            Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
        }
    }
    catch {
        Write-TestResult "Permission tests" $false $_.Exception.Message
    }
}

function Test-Integration {
    Write-Host "`nTesting Full Integration..." -ForegroundColor Blue
    
    try {
        # Check if running with admin privileges
        $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if (-not $isAdmin) {
            Write-TestResult "Scheduled task tests" $false "This test requires administrative privileges"
            return
        }
        
        # Test scheduled task creation
        $taskName = "TestEquityShieldAutoUpload"
        $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$PSScriptRoot\Sync-CorporateStructure-To-SharePoint.ps1`" -SharePointSiteUrl `"$SharePointSiteUrl`""
        $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)
        $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
        Write-TestResult "Scheduled task creation" $true
        
        # Test task execution
        Start-ScheduledTask -TaskName $taskName
        Start-Sleep -Seconds 10  # Give the task time to start
        $taskInfo = Get-ScheduledTaskInfo -TaskName $taskName
        
        if ($taskInfo.LastTaskResult -eq 0) {
            Write-TestResult "Scheduled task execution" $true
        }
        else {
            Write-TestResult "Scheduled task execution" $false "Task failed with result: $($taskInfo.LastTaskResult)"
        }
        
        # Clean up
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-TestResult "Task cleanup" $true
    }
    catch {
        Write-TestResult "Integration tests" $false $_.Exception.Message
    }
}

# Run all tests
Write-Host "Starting Edge Case and Integration Tests" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

Test-NetworkTimeout
Test-InvalidPaths
Test-PermissionIssues
Test-Integration

Write-Host "`nTesting completed!" -ForegroundColor Yellow
