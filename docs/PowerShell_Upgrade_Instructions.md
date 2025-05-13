# How to Upgrade PowerShell to Version 7 or Higher on Windows

## Step 1: Check Current PowerShell Version
Open PowerShell and run:
```powershell
$PSVersionTable.PSVersion
```
If the Major version is less than 7, proceed with the upgrade.

## Step 2: Download PowerShell 7+
- Go to the official PowerShell GitHub releases page: https://github.com/PowerShell/PowerShell/releases
- Download the latest stable release MSI installer for Windows (e.g., `PowerShell-7.x.x-win-x64.msi`).

## Step 3: Install PowerShell 7+
- Run the downloaded MSI installer.
- Follow the installation wizard steps.
- Optionally, select "Add to PATH environment variable" and "Enable PowerShell Remoting".

## Step 4: Verify Installation
- Open a new PowerShell 7 window (search for "PowerShell 7" or "pwsh").
- Run:
```powershell
$PSVersionTable.PSVersion
```
- Confirm the version is 7 or higher.

## Step 5: Use PowerShell 7 for Scripts
- Run your PowerShell scripts using the `pwsh` command instead of `powershell`.
- Example:
```powershell
pwsh -File path\to\your\script.ps1
```

## Additional Notes
- PowerShell 7 can be installed side-by-side with Windows PowerShell 5.1.
- You can set PowerShell 7 as the default shell in your terminal or IDE.

If you need further assistance with the upgrade or running scripts in PowerShell 7, feel free to ask.
