param(
    [string]$SiteUrl
)

Connect-PnPOnline -Url $SiteUrl -Interactive

# Test component loading
$components = Get-PnPPageComponent -Page "Dashboard"
if ($components.Count -eq 0) {
    throw "No components loaded on dashboard"
}

# Test permissions
try {
    $checkPermission = Get-PnPGroup -Identity "Dashboard Users"
    Write-Output "Permission test passed"
} catch {
    throw "Permission configuration failed: $_"
}

# Test data refresh
$refreshJobs = Get-ScheduledJob | Where-Object Name -like "*_Refresh"
if ($refreshJobs.Count -eq 0) {
    Write-Warning "No refresh jobs configured"
} else {
    Write-Output "$($refreshJobs.Count) refresh jobs configured"
}

# Generate test report
$testResults = @{
    Components = $components.Count
    Permissions = $null -ne $checkPermission
    RefreshJobs = $refreshJobs.Count
    LastTest = (Get-Date).ToString()
}

$testResults | ConvertTo-Json | Out-File "$PSScriptRoot\dashboard-test-results.json"
