# Production Deployment Script

# Ensure running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Install required Python packages
Write-Host "Installing required packages..." -ForegroundColor Green
pip install waitress python-dotenv flask

# Create and configure Windows service
Write-Host "Setting up Windows Service..." -ForegroundColor Green
$serviceName = "EquityShieldAPI"
$serviceDescription = "Equity Shield Advocates Production API Server"
$pythonPath = (Get-Command python).Source
$scriptPath = Join-Path $PSScriptRoot "..\production_server.py"
$workingDirectory = Split-Path $scriptPath -Parent

# Create service using NSSM (Non-Sucking Service Manager)
if (-not (Get-Command nssm -ErrorAction SilentlyContinue)) {
    Write-Host "Installing NSSM..." -ForegroundColor Yellow
    choco install nssm -y
}

# Remove existing service if it exists
if (Get-Service $serviceName -ErrorAction SilentlyContinue) {
    Write-Host "Removing existing service..." -ForegroundColor Yellow
    nssm remove $serviceName confirm
}

# Install new service
Write-Host "Creating new service..." -ForegroundColor Green
nssm install $serviceName $pythonPath
nssm set $serviceName AppParameters $scriptPath
nssm set $serviceName Description $serviceDescription
nssm set $serviceName AppDirectory $workingDirectory
nssm set $serviceName DisplayName "Equity Shield API Server"
nssm set $serviceName Start SERVICE_AUTO_START

# Set environment variables for the service
Write-Host "Configuring environment variables..." -ForegroundColor Green
$envPath = Join-Path $PSScriptRoot "..\production.env"
if (Test-Path $envPath) {
    Get-Content $envPath | ForEach-Object {
        $name, $value = $_.Split('=')
        if ($name -and $value) {
            nssm set $serviceName AppEnvironmentExtra "$name=$value"
        }
    }
}

# Start the service
Write-Host "Starting service..." -ForegroundColor Green
Start-Service $serviceName

# Verify service status
$service = Get-Service $serviceName
Write-Host "Service Status: $($service.Status)" -ForegroundColor Green

# Test the API
Write-Host "Testing API endpoints..." -ForegroundColor Green
$testEndpoints = @(
    "http://localhost:8000/api/ping",
    "http://localhost:8000/api/banks/citi-private-bank/account"
)

foreach ($endpoint in $testEndpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Headers @{"X-API-KEY"="secret-api-key"} -ErrorAction Stop
        Write-Host "Endpoint $endpoint : $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "Endpoint $endpoint : Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nDeployment Complete!" -ForegroundColor Green
Write-Host "The API server is running as a Windows service named '$serviceName'"
Write-Host "You can manage it using the following commands:"
Write-Host "  Start-Service $serviceName"
Write-Host "  Stop-Service $serviceName"
Write-Host "  Restart-Service $serviceName"
