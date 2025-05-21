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

function Test-Authentication {
    Write-Host "`nTesting SharePoint Authentication..." -ForegroundColor Blue
    try {
        Import-Module PnP.PowerShell -ErrorAction Stop
        
        try { Disconnect-PnPOnline } catch { }
        
        Write-Host "Initiating legacy authentication using credentials..." -ForegroundColor Gray
        Write-Host "Please provide username and password when prompted." -ForegroundColor Yellow
        
        # Prompt for credentials
        $cred = Get-Credential
        
        # Connect using credentials
        $connection = Connect-PnPOnline -Url $SharePointSiteUrl -Credentials $cred -ReturnConnection
        
        if ($connection) {
            $context = Get-PnPContext
            if ($context) {
                Write-TestResult "SharePoint Authentication" $true "Successfully authenticated to SharePoint"
                return $true
            }
        }
        Write-TestResult "SharePoint Authentication" $false "Connection established but context not available"
        return $false
    }
    catch {
        $errorMessage = $_.Exception.Message
        Write-TestResult "SharePoint Authentication" $false "Authentication failed: $errorMessage"
        
        Write-Host "`nDetailed Error Information:" -ForegroundColor Yellow
        Write-Host "Exception Type: $($_.Exception.GetType().FullName)" -ForegroundColor Yellow
        Write-Host "Stack Trace: $($_.ScriptStackTrace)" -ForegroundColor Yellow
        
        return $false
    }
}

function Test-BasicFileOperations {
    Write-Host "`nTesting Basic File Operations..." -ForegroundColor Blue
    
    $testFile = "test_file.txt"
    $testContent = "Test content $(Get-Date)"
    
    try {
        # Create test file
        Set-Content $testFile $testContent -ErrorAction Stop
        Write-Host "Created local test file" -ForegroundColor Gray
        
        try {
            # Test upload
            Write-Host "Attempting to upload file..." -ForegroundColor Gray
            Add-PnPFile -Path $testFile -Folder $LibraryName -ErrorAction Stop
            Write-TestResult "File Upload" $true
            
            # Test download
            Write-Host "Attempting to download file..." -ForegroundColor Gray
            $downloadPath = "downloaded_$testFile"
            Get-PnPFile -Url "$LibraryName/$testFile" -Path $downloadPath -AsFile -ErrorAction Stop
            
            # Verify content
            $downloadedContent = Get-Content $downloadPath -Raw
            $contentMatch = $downloadedContent -eq $testContent
            Write-TestResult "File Download and Content Verification" $contentMatch
            
            # Test delete
            Write-Host "Attempting to delete file..." -ForegroundColor Gray
            Remove-PnPFile -ServerRelativeUrl "$LibraryName/$testFile" -Force -ErrorAction Stop
            Write-TestResult "File Delete" $true
        }
        catch {
            Write-TestResult "File Operations" $false $_.Exception.Message
        }
    }
    catch {
        Write-TestResult "Test File Creation" $false $_.Exception.Message
    }
    finally {
        # Cleanup
        if (Test-Path $testFile) { Remove-Item $testFile }
        if (Test-Path $downloadPath) { Remove-Item $downloadPath }
    }
}

# Main execution
Write-Host "SharePoint Critical Path Testing" -ForegroundColor Cyan
Write-Host "Site URL: $SharePointSiteUrl" -ForegroundColor Cyan
Write-Host "Library: $LibraryName" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$authSuccess = Test-Authentication
if ($authSuccess) {
    Test-BasicFileOperations
    Disconnect-PnPOnline
    Write-Host "`nTests completed. Disconnected from SharePoint." -ForegroundColor Cyan
}
else {
    Write-Host "`nSkipping file operations tests due to authentication failure." -ForegroundColor Yellow
    Write-Host "Please ensure you have appropriate permissions to access the SharePoint site." -ForegroundColor Yellow
}
