# Test script for integration with external systems
param(
    [Parameter(Mandatory=$true)]
    [string]$ApiServerUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$DatabaseConnectionString,
    
    [Parameter(Mandatory=$false)]
    [string]$DashboardUrl = "http://localhost:3000"  # Default value provided
)

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Success,
        [string]$Message = ""
    )
    
    if ($Success) {
        Write-Host "$([char]0x221A) $TestName" -ForegroundColor Green
    } else {
        Write-Host "X $TestName" -ForegroundColor Red
        if ($Message) {
            Write-Host "  $Message" -ForegroundColor Red
        }
    }
}

function Test-ApiServer {
    Write-Host "`nTesting API Server..." -ForegroundColor Blue
    $testsPassed = 0
    $totalTests = 4  # Update this when adding new tests
    
    try {
        # Test API server health endpoint
        $healthUrl = "$ApiServerUrl/health"
        $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 10
        $healthData = $response.Content | ConvertFrom-Json
        
        if ($response.StatusCode -eq 200 -and $healthData.status -eq "healthy") {
            Write-TestResult -TestName "API server health" -Success $true
            $testsPassed++
            
            # Test specific API endpoints
            $endpoints = @(
                "/api/v1/corporate-data",
                "/api/v1/corporate-structure",
                "/api/v1/real-assets"
            )
            
            foreach ($endpoint in $endpoints) {
                $url = "$ApiServerUrl$endpoint"
                try {
                    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
                    $data = $response.Content | ConvertFrom-Json
                    
                    if ($response.StatusCode -eq 200 -and $data.status -eq "success") {
                        Write-TestResult -TestName "API endpoint $endpoint" -Success $true
                        Write-TestResult -TestName "$endpoint data" -Success ($null -ne $data.data) -Message "Data retrieved successfully"
                        $testsPassed++
                    } else {
                        Write-TestResult -TestName "API endpoint $endpoint" -Success $false -Message "Invalid response status"
                    }
                }
                catch {
                    Write-TestResult -TestName "API endpoint $endpoint" -Success $false -Message $_.Exception.Message
                }
            }
        } else {
            Write-TestResult -TestName "API server health" -Success $false -Message "Unhealthy status: $($healthData.status)"
        }
    }
    catch {
        Write-TestResult -TestName "API server health" -Success $false -Message $_.Exception.Message
    }
    
    return ($testsPassed, $totalTests)
}

function Test-DatabaseConsistency {
    Write-Host "`nTesting Database Consistency..." -ForegroundColor Blue
    $testsPassed = 0
    $totalTests = 4  # Update this when adding new tests
    
    try {
        # Test database connection
        $testQuery = "SELECT 1 AS TestResult"
        $result = Invoke-Sqlcmd -ConnectionString $DatabaseConnectionString -Query $testQuery -ErrorAction Stop
        
        if ($result) {
            Write-TestResult -TestName "Database connection" -Success $true
            $testsPassed++
            
            # Test data consistency
            $tables = @("CorporateData", "CorporateStructure", "RealAssets")
            
            foreach ($table in $tables) {
                $query = "IF OBJECT_ID('$table', 'U') IS NOT NULL SELECT COUNT(*) AS Count FROM $table ELSE SELECT -1 AS Count"
                try {
                    $result = Invoke-Sqlcmd -ConnectionString $DatabaseConnectionString -Query $query
                    if ($result.Count -ge 0) {
                        Write-TestResult -TestName "Table $table" -Success $true -Message "Row count: $($result.Count)"
                        $testsPassed++
                    } else {
                        Write-TestResult -TestName "Table $table" -Success $false -Message "Table does not exist"
                    }
                }
                catch {
                    Write-TestResult -TestName "Table $table" -Success $false -Message $_.Exception.Message
                }
            }
        }
    }
    catch {
        Write-TestResult -TestName "Database consistency" -Success $false -Message $_.Exception.Message
    }
    
    return ($testsPassed, $totalTests)
}

# Run all tests
Write-Host "Starting Integration Tests with External Systems" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Yellow

$apiResults = Test-ApiServer
$dbResults = Test-DatabaseConsistency

$totalPassed = $apiResults[0] + $dbResults[0]
$totalTests = $apiResults[1] + $dbResults[1]

Write-Host "`nTest Summary" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "API Tests: $($apiResults[0])/$($apiResults[1]) passed" -ForegroundColor $(if ($apiResults[0] -eq $apiResults[1]) { "Green" } else { "Red" })
Write-Host "Database Tests: $($dbResults[0])/$($dbResults[1]) passed" -ForegroundColor $(if ($dbResults[0] -eq $dbResults[1]) { "Green" } else { "Red" })
Write-Host "Total: $totalPassed/$totalTests tests passed" -ForegroundColor $(if ($totalPassed -eq $totalTests) { "Green" } else { "Red" })
