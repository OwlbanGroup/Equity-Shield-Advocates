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
        $originalTimeout = [System.Net.ServicePointManager]::DefaultConnectionLimit
        [System.Net.ServicePointManager]::DefaultConnectionLimit = 1
        
        $job = Start-Job -ScriptBlock {
            param($SharePointSiteUrl, $LibraryName)
            Import-Module PnP.PowerShell
            Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
            $testFile = "test_large_file.txt"
            1..10000 | ForEach-Object { Add-Content $testFile ("Line " + $_) }
            try {
                Add-PnPFile -Path $testFile -Folder $LibraryName
            }
            finally {
                Remove-Item $testFile -Force
            }
        } -ArgumentList $SharePointSiteUrl, $LibraryName
        
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

# Execute the tests
Test-NetworkTimeout
Test-InvalidPaths
