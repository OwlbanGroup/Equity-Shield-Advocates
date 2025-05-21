# Test script for advanced SharePoint sync scenarios
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

function Test-LongRunningSyncOperation {
    Write-Host "`nTesting Long-Running Sync Operation..." -ForegroundColor Blue
    
    try {
        # Create a large test file (100MB)
        $testFile = "large_test_file.dat"
        $buffer = New-Object byte[] 1048576  # 1MB buffer
        $rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
        $fileStream = [System.IO.File]::Create($testFile)
        
        try {
            for ($i = 0; $i -lt 100; $i++) {  # 100 x 1MB = 100MB
                $rng.GetBytes($buffer)
                $fileStream.Write($buffer, 0, $buffer.Length)
                Write-Progress -Activity "Creating test file" -Status "$i% Complete" -PercentComplete $i
            }
        }
        finally {
            $fileStream.Close()
        }
        
        # Test upload with progress tracking
        $start = Get-Date
        $uploadJob = Start-Job -ScriptBlock {
            param($SharePointSiteUrl, $LibraryName, $TestFile)
            
            Import-Module PnP.PowerShell
            Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
            Add-PnPFile -Path $TestFile -Folder $LibraryName
        } -ArgumentList $SharePointSiteUrl, $LibraryName, $testFile
        
        # Monitor progress
        while (Get-Job -Id $uploadJob.Id | Where-Object { $_.State -eq "Running" }) {
            $elapsed = (Get-Date) - $start
            Write-Progress -Activity "Uploading large file" -Status "Time elapsed: $($elapsed.ToString('mm\:ss'))"
            Start-Sleep -Seconds 1
        }
        
        # Check upload result
        $uploadResult = Receive-Job -Id $uploadJob.Id
        if ($uploadResult) {
            Write-TestResult "Long-running sync operation" $true "Upload completed in $($elapsed.ToString('mm\:ss'))"
        } else {
            Write-TestResult "Long-running sync operation" $false "Upload failed or returned no result"
        }
    }
    catch {
        Write-TestResult "Long-running sync operation" $false $_.Exception.Message
    }
    finally {
        Remove-Item $testFile -Force -ErrorAction SilentlyContinue
        Remove-Job -Id $uploadJob.Id -Force -ErrorAction SilentlyContinue
    }
}

function Test-ConcurrentFileUploads {
    Write-Host "`nTesting Concurrent File Uploads..." -ForegroundColor Blue
    
    try {
        # Create test files
        $testFiles = @()
        1..5 | ForEach-Object {
            $fileName = "test_file_$_.json"
            Set-Content $fileName "{`"test`": `"data $_ `"}"
            $testFiles += $fileName
        }
        
        # Upload files concurrently
        $jobs = @()
        foreach ($file in $testFiles) {
            $jobs += Start-Job -ScriptBlock {
                param($SharePointSiteUrl, $LibraryName, $File)
                
                Import-Module PnP.PowerShell
                Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
                Add-PnPFile -Path $File -Folder $LibraryName
            } -ArgumentList $SharePointSiteUrl, $LibraryName, $file
        }
        
        # Wait for all uploads to complete and check results
        $successCount = 0
        foreach ($job in $jobs) {
            $jobResult = Wait-Job $job | Receive-Job
            if ($jobResult) { $successCount++ }
        }
        
        if ($successCount -eq $testFiles.Count) {
            Write-TestResult "Concurrent file uploads" $true "Successfully uploaded $successCount files concurrently"
        } else {
            Write-TestResult "Concurrent file uploads" $false "Only $successCount of $($testFiles.Count) files uploaded successfully"
        }
    }
    catch {
        Write-TestResult "Concurrent file uploads" $false $_.Exception.Message
    }
    finally {
        $testFiles | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
        $jobs | Remove-Job -Force -ErrorAction SilentlyContinue
    }
}

function Test-NetworkRecovery {
    Write-Host "`nTesting Network Recovery..." -ForegroundColor Blue
    
    try {
        # Create test file
        $testFile = "network_test.json"
        Set-Content $testFile "{`"test`": `"network recovery`"}"
        
        # Simulate network interruption during upload
        $uploadJob = Start-Job -ScriptBlock {
            param($SharePointSiteUrl, $LibraryName, $TestFile)
            
            Import-Module PnP.PowerShell
            Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
            
            # Simulate network interruption
            [System.Net.ServicePointManager]::DefaultConnectionLimit = 1
            Start-Sleep -Seconds 5  # Give time for connection to establish
            
            try {
                Add-PnPFile -Path $TestFile -Folder $LibraryName
            }
            catch {
                # Wait and retry
                Start-Sleep -Seconds 10
                Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
                Add-PnPFile -Path $TestFile -Folder $LibraryName
            }
        } -ArgumentList $SharePointSiteUrl, $LibraryName, $testFile
        
        # Check upload result
        $uploadResult = Wait-Job $uploadJob | Receive-Job
        if ($uploadResult) {
            Write-TestResult "Network recovery" $true "Successfully recovered from network interruption"
        } else {
            Write-TestResult "Network recovery" $false "Failed to recover from network interruption"
        }
    }
    catch {
        Write-TestResult "Network recovery" $false $_.Exception.Message
    }
    finally {
        Remove-Item $testFile -Force -ErrorAction SilentlyContinue
        Remove-Job -Id $uploadJob.Id -Force -ErrorAction SilentlyContinue
    }
}

function Test-FolderPermissions {
    Write-Host "`nTesting SharePoint Folder Permissions..." -ForegroundColor Blue
    
    try {
        # Create test folder
        $testFolder = "TestPermissions"
        
        # Connect to SharePoint
        Connect-PnPOnline -Url $SharePointSiteUrl -DeviceLogin
        
        # Create folder and test file
        Add-PnPFolder -Name $testFolder -Folder $LibraryName
        $testFile = "permission_test.json"
        Set-Content $testFile "{`"test`": `"permissions`"}"
        
        # Upload file to test folder
        Add-PnPFile -Path $testFile -Folder "$LibraryName/$testFolder"
        
        # Verify folder exists and has inherited permissions
        $folder = Get-PnPFolder -Url "$LibraryName/$testFolder"
        $hasInheritedPerms = Get-PnPProperty -ClientObject $folder -Property "ListItemAllFields" | 
                            Select-Object -ExpandProperty HasInheritedPermissions
        
        Write-TestResult "Folder permission inheritance" $hasInheritedPerms
    }
    catch {
        Write-TestResult "Folder permission inheritance" $false $_.Exception.Message
    }
    finally {
        Remove-Item $testFile -Force -ErrorAction SilentlyContinue
        # Cleanup folder
        try {
            Remove-PnPFolder -Name $testFolder -Folder $LibraryName -Force
        }
        catch {
            # Ignore cleanup errors
        }
    }
}

# Run all tests
Write-Host "Starting Advanced Scenario Tests" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

Test-LongRunningSyncOperation
Test-ConcurrentFileUploads
Test-NetworkRecovery
Test-FolderPermissions

Write-Host "`nTesting completed!" -ForegroundColor Yellow
