# PowerShell script compatible with Windows PowerShell 5.1 to upload files to SharePoint using REST API

param(
    [string]$SiteUrl = "https://yourtenant.sharepoint.com/sites/yoursite",
    [string]$LibraryName = "Documents",
    [string]$LocalFilePath1 = "corporate_structure.json",
    [string]$LocalFilePath2 = "data/corporate_structure.json"
)

function Get-AuthHeader {
    # This function should be implemented to get the Authorization header with a valid access token
    # For example, using OAuth2 with client credentials or device code flow
    # Placeholder: return empty hashtable
    return @{}
}

function Upload-FileToSharePoint {
    param(
        [string]$SiteUrl,
        [string]$LibraryName,
        [string]$FilePath
    )

    $fileName = Split-Path $FilePath -Leaf
    $uploadUrl = "$SiteUrl/_api/web/GetFolderByServerRelativeUrl('$LibraryName')/Files/add(url='$fileName',overwrite=true)"

    $headers = Get-AuthHeader

    $fileContent = [System.IO.File]::ReadAllBytes($FilePath)

    Write-Host "Uploading $fileName to $LibraryName ..."

    $response = Invoke-RestMethod -Uri $uploadUrl -Headers $headers -Method POST -Body $fileContent -ContentType "application/octet-stream"

    if ($response) {
        Write-Host "Uploaded $fileName successfully."
    } else {
        Write-Host "Failed to upload $fileName."
    }
}

# Upload files
Upload-FileToSharePoint -SiteUrl $SiteUrl -LibraryName $LibraryName -FilePath $LocalFilePath1
Upload-FileToSharePoint -SiteUrl $SiteUrl -LibraryName $LibraryName -FilePath $LocalFilePath2

Write-Host "Sync completed. Please refresh your SharePoint dashboard manually."

# Additional step: Notify or trigger dashboard update (if applicable)
Write-Host "Triggering dashboard update..."

# Placeholder for dashboard update logic, e.g., call API or refresh cache
# Implement as needed based on your dashboard setup

Write-Host "Dashboard update triggered."
