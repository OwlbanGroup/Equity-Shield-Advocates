# Script to install and verify all prerequisites for integration testing

Write-Host "Installing Prerequisites for Integration Testing..." -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Yellow

# Install PnP.PowerShell module
Write-Host "`nInstalling PnP.PowerShell module..." -ForegroundColor Blue
if (-not (Get-Module -ListAvailable -Name "PnP.PowerShell")) {
    Install-Module -Name "PnP.PowerShell" -Force -AllowClobber -Scope CurrentUser
    Write-Host "PnP.PowerShell module installed successfully" -ForegroundColor Green
} else {
    Write-Host "PnP.PowerShell module already installed" -ForegroundColor Green
}

# Install SqlServer module
Write-Host "`nInstalling SqlServer module..." -ForegroundColor Blue
if (-not (Get-Module -ListAvailable -Name "SqlServer")) {
    Install-Module -Name "SqlServer" -Force -AllowClobber -Scope CurrentUser
    Write-Host "SqlServer module installed successfully" -ForegroundColor Green
} else {
    Write-Host "SqlServer module already installed" -ForegroundColor Green
}

# Add health endpoint to API server
Write-Host "`nAdding health endpoint to API server..." -ForegroundColor Blue
$apiServerPath = "./src/api_server.py"
$healthEndpoint = @"

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })
"@

if (Test-Path $apiServerPath) {
    $content = Get-Content $apiServerPath -Raw
    if ($content -notmatch '/health') {
        # Add necessary imports if not present
        if ($content -notmatch 'datetime') {
            $content = "import datetime`n" + $content
        }
        # Add health endpoint
        $content = $content + $healthEndpoint
        Set-Content $apiServerPath $content
        Write-Host "Health endpoint added to API server" -ForegroundColor Green
    } else {
        Write-Host "Health endpoint already exists" -ForegroundColor Green
    }
} else {
    Write-Host "API server file not found at $apiServerPath" -ForegroundColor Red
}

Write-Host "`nPrerequisites installation completed!" -ForegroundColor Yellow
