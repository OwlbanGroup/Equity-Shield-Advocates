# PowerShell script to check Docker version and environment PATH

Write-Host "Checking Docker version..."
try {
    docker --version
} catch {
    Write-Host "Docker command not found. Checking PATH environment variable..."
    $env:PATH -split ';' | ForEach-Object { Write-Host $_ }
    Write-Host "Please ensure Docker is installed and its executable path is added to the PATH environment variable."
}
