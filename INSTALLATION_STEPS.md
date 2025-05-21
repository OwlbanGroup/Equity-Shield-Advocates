# Manual Installation Steps for Deployment Prerequisites

## 1. PowerShell 7 Installation
1. Visit https://github.com/PowerShell/PowerShell/releases
2. Download `PowerShell-7.4.6-win-x64.msi`
3. Run the MSI installer:
   - Accept the license agreement
   - Choose "Add PowerShell to PATH environment variable"
   - Complete the installation
4. Verify installation by opening a new terminal and running:
   ```powershell
   pwsh -Version
   ```

## 2. GitHub CLI Installation
1. Visit https://cli.github.com/
2. Download the Windows installer (MSI)
3. Run the installer:
   - Accept the license agreement
   - Keep default installation options
   - Complete the installation
4. Verify installation:
   ```powershell
   gh --version
   ```
5. Authenticate with GitHub:
   ```powershell
   gh auth login
   ```
   - Follow the prompts to complete authentication

## 3. AWS CLI Installation
1. Visit https://aws.amazon.com/cli/
2. Download the Windows installer (64-bit)
3. Run the MSI installer:
   - Accept the license agreement
   - Keep default installation options
   - Complete the installation
4. Verify installation:
   ```powershell
   aws --version
   ```
5. Configure AWS credentials:
   ```powershell
   aws configure
   ```
   Enter your:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., us-east-1)
   - Default output format (json)

## 4. Docker Desktop Installation
1. Visit https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for Windows
3. Run the installer:
   - Accept the license agreement
   - Keep default installation options
   - Enable WSL 2 if prompted
   - Complete the installation
4. Restart your computer when prompted
5. Verify installation:
   ```powershell
   docker --version
   ```

## Post-Installation Steps

1. Restart your computer to ensure all environment variables are properly set.

2. Verify all installations in a new PowerShell 7 window:
```powershell
pwsh -Version
gh --version
aws --version
docker --version
```

3. Test AWS credentials:
```powershell
aws sts get-caller-identity
```

4. Test Docker:
```powershell
docker run hello-world
```

## Next Steps

After installing all prerequisites:
1. Close and reopen VS Code
2. Open a new PowerShell 7 terminal in VS Code
3. Run the deployment script:
```powershell
./scripts/deploy_equity_shield_advocates_windows.ps1
```

## Troubleshooting

If you encounter any issues:

1. PowerShell 7 not recognized:
   - Ensure it was added to PATH during installation
   - Try running as `pwsh` instead of `powershell`

2. GitHub CLI authentication issues:
   - Run `gh auth status` to check authentication status
   - Try `gh auth login` again if needed

3. AWS CLI configuration issues:
   - Check credentials in `~/.aws/credentials`
   - Verify region in `~/.aws/config`

4. Docker issues:
   - Ensure Docker Desktop is running
   - Check Windows features for WSL 2 and Hyper-V
   - Run `docker system info` for detailed status

For any other issues, please refer to the respective documentation:
- PowerShell: https://docs.microsoft.com/powershell/
- GitHub CLI: https://cli.github.com/manual/
- AWS CLI: https://docs.aws.amazon.com/cli/
- Docker: https://docs.docker.com/desktop/windows/
