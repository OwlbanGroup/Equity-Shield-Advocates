# Deployment Guide for Equity Shield Advocates

## Overview
This document outlines the steps to deploy the Equity Shield Advocates application in a production environment using Docker and the existing CI/CD pipeline.

## Prerequisites
- Docker installed on the deployment server.
- Access to Docker Hub account with credentials stored as GitHub secrets.
- SSH access to the deployment server.
- Python 3.11 environment for local testing (optional).

## Environment Variables and Secrets
- Ensure all sensitive information such as API keys, database credentials, and other secrets are stored securely.
- Use environment variables or secret management tools on the deployment server.
- The current Dockerfile and app do not hardcode secrets; configure them externally.

## Building and Running Locally
1. Build the Docker image locally:
   ```
   docker build -t equity-shield-advocates:latest .
   ```
2. Run the container:
   ```
   docker run -d -p 8000:8000 --name equity-shield-advocates equity-shield-advocates:latest
   ```
3. Access the app at `http://localhost:8000`.

## CI/CD Pipeline
- The GitHub Actions workflow `.github/workflows/ci-cd-updated.yml` automates:
  - Code checkout
  - Python environment setup
  - Dependency installation
  - Running tests and linting
  - Docker image build, tag, and push to Docker Hub
  - Deployment to the server via SSH and Docker commands

## Deployment Server Setup
- Ensure Docker is installed and running.
- Configure SSH keys for GitHub Actions to access the server.
- The deployment script pulls the latest Docker image, stops and removes the old container, and runs the new container.

## Monitoring and Rollback
- Monitor container logs using:
  ```
  docker logs -f equity-shield-advocates
  ```
- To rollback, manually pull and run a previous Docker image tag.
- Consider adding monitoring tools and alerting for production readiness.

## Additional Recommendations
- Add HTTPS termination via reverse proxy (e.g., Nginx).
- Implement health checks and readiness probes.
- Automate database migrations if applicable.
- Add load balancing for scalability.

## Summary
The project is ready for deployment with Docker and CI/CD automation. Follow the above steps to deploy and maintain the application in production.

For any issues or further enhancements, please refer to the project documentation or contact the development team.
