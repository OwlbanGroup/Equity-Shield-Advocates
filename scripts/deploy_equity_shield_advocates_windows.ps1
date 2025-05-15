# PowerShell deployment script for Windows environment

Write-Host "Starting deployment process for Equity Shield Advocates..."

# Step 1: Check if GitHub CLI is installed
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/ and try again."
    exit 1
}

# Step 2: Authenticate GitHub CLI if not already authenticated
$authStatus = gh auth status 2>&1
if ($authStatus -match "You are not logged in") {
    Write-Host "GitHub CLI not authenticated. Launching login..."
    gh auth login
} else {
    Write-Host "GitHub CLI already authenticated."
}

# Step 3: Trigger the CI/CD workflow on the main branch
Write-Host "Triggering CI/CD workflow..."
gh workflow run ci-cd-updated.yml -f ref=main

Write-Host "Deployment triggered. Monitor the GitHub Actions workflow for progress."
