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
