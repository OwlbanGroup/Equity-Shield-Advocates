#!/bin/bash

# Deployment script for Equity Shield Advocates using GitHub Actions CI/CD pipeline

echo "Starting deployment process..."

# Step 1: Authenticate GitHub CLI (if not already authenticated)
if ! gh auth status > /dev/null 2>&1; then
  echo "GitHub CLI not authenticated. Please login:"
  gh auth login
else
  echo "GitHub CLI already authenticated."
fi

# Step 2: Trigger the CI/CD workflow on the main branch
echo "Triggering CI/CD workflow..."
gh workflow run ci-cd-updated.yml -f ref=main

echo "Deployment triggered. Monitor the GitHub Actions workflow for progress."

# Optional: You can add commands here to monitor the workflow status or notify upon completion.
