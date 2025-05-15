#!/bin/bash
# Script to authenticate GitHub CLI using Personal Access Token (PAT) and trigger deployment workflow

echo "Step 1: Generate a Personal Access Token (PAT) with 'repo' and 'workflow' scopes if you haven't already."
echo "Visit: https://github.com/settings/tokens"
echo "Click 'Generate new token' (classic), provide a name, expiration, and select scopes 'repo' and 'workflow'."
echo "Copy the generated token securely."

read -p "Press Enter once you have your PAT ready..."

echo "Step 2: Set the GH_TOKEN environment variable with your PAT."
export GH_TOKEN="your_token_here"
echo "Replace 'your_token_here' with your actual PAT in this script before running."

read -p "Press Enter once you have set the GH_TOKEN environment variable..."

echo "Step 3: Verify GitHub CLI authentication status:"
gh auth status

echo "Step 4: Trigger the deployment workflow:"
gh workflow run ci-cd-updated.yml -f ref=main

echo "Deployment triggered. Monitor the GitHub Actions workflow for progress."
