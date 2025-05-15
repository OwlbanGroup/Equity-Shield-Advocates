# GitHub CLI Authentication Setup Instructions

To trigger GitHub Actions workflows using the GitHub CLI (`gh`), you need to authenticate the CLI with your GitHub account.

Follow these steps:

1. **Install GitHub CLI** (if not already installed):
   - Download and install from https://cli.github.com/

2. **Authenticate GitHub CLI:**
   - Open your terminal or PowerShell.
   - Run the command:
     ```
     gh auth login
     ```
   - When prompted:
     - Select **GitHub.com** as the account to log into.
     - Choose your preferred authentication method (e.g., web browser).
     - Follow the instructions to complete authentication.

3. **Verify Authentication:**
   - Run:
     ```
     gh auth status
     ```
   - You should see a message confirming you are logged in.

4. **Trigger Workflow:**
   - After authentication, you can trigger the deployment workflow with:
     ```
     gh workflow run ci-cd-updated.yml -f ref=main
     ```

If you prefer, you can also create a Personal Access Token (PAT) with appropriate scopes and set it as the `GH_TOKEN` environment variable for non-interactive authentication.

For more details, visit: https://cli.github.com/manual/gh_auth_login

---

If you want me to assist you with any of these steps, please let me know.
