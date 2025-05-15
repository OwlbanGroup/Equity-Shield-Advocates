#!/bin/bash

# This script guides through setting up GitHub CLI authentication and triggering the CI/CD workflow

echo "Step 1: Authenticate GitHub CLI"
echo "Run the following command and follow the prompts to authenticate:"
echo "  gh auth login"

echo "Step 2: Verify authentication"
echo "Run:"
echo "  gh auth status"
echo "to confirm you are logged in."

echo "Step 3: Trigger the CI/CD workflow"
echo "Run the following command to trigger the deployment workflow on the main branch:"
echo "  gh workflow run ci-cd-updated.yml -f ref=main"

echo "Note: Make sure you have the GitHub CLI installed and configured in your PATH."

echo "If you want me to run these commands interactively, please run this script in your terminal."
