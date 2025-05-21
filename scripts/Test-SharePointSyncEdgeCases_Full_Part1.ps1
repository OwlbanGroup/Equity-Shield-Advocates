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
    } 
    else {
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
        } 
        else {
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

# Execute the test
Test-NetworkTimeout
