# Test script for production deployment verification
param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$ApiKey = $env:API_KEY
)

$ErrorActionPreference = "Stop"

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Success
    )
    if ($Success) {
        Write-Host "✓ $TestName" -ForegroundColor Green
    } else {
        Write-Host "✗ $TestName" -ForegroundColor Red
    }
}

function Test-Endpoint {
    param(
        [string]$Endpoint,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [int]$ExpectedStatus = 200
    )
    
    try {
        $response = Invoke-WebRequest -Uri "$BaseUrl$Endpoint" -Method $Method -Headers $Headers -UseBasicParsing
        return $response.StatusCode -eq $ExpectedStatus
    } catch {
        Write-Host "Error testing endpoint $Endpoint : $_" -ForegroundColor Red
        return $false
    }
}

function Test-LogFileAccess {
    $logPath = "/var/log/equity-shield/production.log"
    return Test-Path $logPath
}

# Initialize test results
$allTestsPassed = $true

Write-Host "`nStarting Production Deployment Tests" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

# Test 1: Health Check
$healthCheck = Test-Endpoint -Endpoint "/health"
Write-TestResult "Health Check Endpoint" $healthCheck
$allTestsPassed = $allTestsPassed -and $healthCheck

# Test 2: API Authentication
$headers = @{
    "X-API-Key" = $ApiKey
    "Content-Type" = "application/json"
}
$authTest = Test-Endpoint -Endpoint "/api/v1/status" -Headers $headers
Write-TestResult "API Authentication" $authTest
$allTestsPassed = $allTestsPassed -and $authTest

# Test 3: CORS Headers
$corsTest = $true
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method OPTIONS -UseBasicParsing
    $corsHeaders = @(
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers"
    )
    foreach ($header in $corsHeaders) {
        if (-not $response.Headers.ContainsKey($header)) {
            $corsTest = $false
            break
        }
    }
} catch {
    $corsTest = $false
}
Write-TestResult "CORS Headers" $corsTest
$allTestsPassed = $allTestsPassed -and $corsTest

# Test 4: Security Headers
$securityTest = $true
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method GET -UseBasicParsing
    $securityHeaders = @(
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection"
    )
    foreach ($header in $securityHeaders) {
        if (-not $response.Headers.ContainsKey($header)) {
            $securityTest = $false
            break
        }
    }
} catch {
    $securityTest = $false
}
Write-TestResult "Security Headers" $securityTest
$allTestsPassed = $allTestsPassed -and $securityTest

# Test 5: Log File Access
$logTest = Test-LogFileAccess
Write-TestResult "Log File Access" $logTest
$allTestsPassed = $allTestsPassed -and $logTest

# Test 6: Rate Limiting
$rateLimitTest = $true
try {
    for ($i = 1; $i -le 61; $i++) {
        $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method GET -UseBasicParsing
    }
    $rateLimitTest = $false  # Should have been rate limited
} catch {
    $rateLimitTest = $_.Exception.Response.StatusCode -eq 429
}
Write-TestResult "Rate Limiting" $rateLimitTest
$allTestsPassed = $allTestsPassed -and $rateLimitTest

Write-Host "`nOverall Test Status:" -ForegroundColor Yellow
if ($allTestsPassed) {
    Write-Host "`nProduction deployment verified successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nProduction deployment verification failed. Please review the test results above." -ForegroundColor Red
    exit 1
}
