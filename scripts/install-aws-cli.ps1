# Script to download and install AWS CLI v2

Write-Host "Downloading AWS CLI installer..." -ForegroundColor Green

# Create temp directory if it doesn't exist
$tempDir = "C:\temp"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir
}

# Download AWS CLI installer
$installerUrl = "https://awscli.amazonaws.com/AWSCLIV2.msi"
$installerPath = Join-Path $tempDir "AWSCLIV2.msi"

try {
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
    Write-Host "AWS CLI installer downloaded successfully." -ForegroundColor Green
} catch {
    Write-Error "Failed to download AWS CLI installer: $_"
    exit 1
}

# Install AWS CLI
Write-Host "Installing AWS CLI..." -ForegroundColor Green
try {
    Start-Process msiexec.exe -Wait -ArgumentList "/i $installerPath /quiet"
    Write-Host "AWS CLI installed successfully." -ForegroundColor Green
} catch {
    Write-Error "Failed to install AWS CLI: $_"
    exit 1
}

# Clean up
Remove-Item $installerPath -Force

# Update PATH environment variable
Write-Host "Updating PATH environment variable..." -ForegroundColor Green
try {
    # Add AWS CLI path to user PATH if it's not already there
    $awsPath = "C:\Program Files\Amazon\AWSCLIV2"
    $currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    if ($currentPath -notlike "*$awsPath*") {
        $newPath = "$currentPath;$awsPath"
        [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "Added AWS CLI to user PATH." -ForegroundColor Green
    }

    # Refresh current session's PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    # Force PowerShell to refresh its PATH
    $env:PSModulePath = [System.Environment]::GetEnvironmentVariable("PSModulePath", "Machine")
} catch {
    Write-Error "Failed to update PATH: $_"
    Write-Host "You may need to manually add C:\Program Files\Amazon\AWSCLIV2 to your system PATH" -ForegroundColor Yellow
}

# Verify installation
Write-Host "Verifying AWS CLI installation..." -ForegroundColor Green
try {
    # Try direct path first
    if (Test-Path "C:\Program Files\Amazon\AWSCLIV2\aws.exe") {
        & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" --version
        Write-Host "AWS CLI verification successful." -ForegroundColor Green
    } else {
        throw "AWS CLI executable not found at expected location"
    }
} catch {
    Write-Error "AWS CLI verification failed: $_"
    Write-Host "`nTroubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Close and reopen your PowerShell window" -ForegroundColor Yellow
    Write-Host "2. Try running 'aws --version' again" -ForegroundColor Yellow
    Write-Host "3. If still failing, verify that C:\Program Files\Amazon\AWSCLIV2 exists and contains aws.exe" -ForegroundColor Yellow
    Write-Host "4. Add C:\Program Files\Amazon\AWSCLIV2 to your system PATH manually if needed" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nNext steps:" -ForegroundColor Green
Write-Host "1. Close and reopen your PowerShell window to ensure PATH changes take effect" -ForegroundColor Yellow
Write-Host "2. Configure AWS credentials by running: aws configure" -ForegroundColor Yellow
Write-Host "3. Enter your AWS Access Key ID when prompted" -ForegroundColor Yellow
Write-Host "4. Enter your AWS Secret Access Key when prompted" -ForegroundColor Yellow
Write-Host "5. Enter default region (e.g., us-east-1) when prompted" -ForegroundColor Yellow
Write-Host "6. Enter output format (json) when prompted" -ForegroundColor Yellow
