param(
    [string]$ConfigPath
)

$config = Get-Content $ConfigPath | ConvertFrom-Json
Connect-PnPOnline -Url $config.SiteUrl -Interactive

# Create scheduled refresh job
foreach ($component in $config.Components) {
    if ($component.RefreshInterval) {
        $jobName = "$($component.Type)_Refresh"
        $scriptBlock = {
            param($siteUrl, $componentType)
            Connect-PnPOnline -Url $siteUrl -Interactive
            Update-PnPWebPart -Page "Dashboard" -Identity $componentType
        }
        
        $trigger = New-JobTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $component.RefreshInterval)
        Register-ScheduledJob -Name $jobName -ScriptBlock $scriptBlock -Trigger $trigger -ArgumentList $config.SiteUrl, $component.Type
    }
}

# Set up log rotation
Add-Content -Path "$PSScriptRoot\dashboard-refresh.log" -Value "Refresh jobs configured on $(Get-Date)"
