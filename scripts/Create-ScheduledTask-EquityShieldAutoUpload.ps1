# PowerShell script to create the scheduled task "EquityShield_AutoUpload" to run the sync script periodically

param(
    [Parameter(Mandatory=$true)]
    [string]$SharePointSiteUrl
)

$taskName = "EquityShield_AutoUpload"
$scriptPath = Join-Path $PSScriptRoot "Sync-CorporateStructure-To-SharePoint.ps1"
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`" -SharePointSiteUrl `"$SharePointSiteUrl`""
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    # Check if task exists
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -ne $existingTask) {
        Write-Host "Scheduled task '$taskName' already exists. Deleting existing task..."
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }

    # Register new scheduled task
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    Write-Host "Scheduled task '$taskName' created successfully."
    exit 0
}
catch {
    Write-Host "Failed to create scheduled task '$taskName': $_"
    exit 1
}
