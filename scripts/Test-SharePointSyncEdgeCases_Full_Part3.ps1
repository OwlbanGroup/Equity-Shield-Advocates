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

Write-Host "Starting Edge Case and Integration Tests" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

Test-NetworkTimeout
Test-InvalidPaths
Test-PermissionIssues
Test-Integration

Write-Host "`nTesting completed!" -ForegroundColor Yellow
