#!/bin/bash

# This script sets up secure parameters in AWS Systems Manager Parameter Store
# Run this script with AWS credentials configured

# Set your AWS region
AWS_REGION=${AWS_REGION:-"us-east-1"}

# Function to create a secure string parameter
create_secure_parameter() {
    local name=$1
    local value=$2
    local description=$3

    aws ssm put-parameter \
        --name "/equity-shield/$name" \
        --value "$value" \
        --type "SecureString" \
        --description "$description" \
        --overwrite \
        --region "$AWS_REGION"
}

echo "Setting up AWS Systems Manager parameters for Equity Shield Advocates..."

# API Security
create_secure_parameter "api-key" "REPLACE_WITH_SECURE_KEY" "API Key for authentication"
create_secure_parameter "jwt-secret" "REPLACE_WITH_SECURE_JWT_SECRET" "JWT signing secret"

# Database Credentials
create_secure_parameter "db-password" "REPLACE_WITH_SECURE_PASSWORD" "Database password"
create_secure_parameter "db-user" "REPLACE_WITH_DB_USER" "Database username"

# Redis Credentials
create_secure_parameter "redis-password" "REPLACE_WITH_SECURE_REDIS_PASSWORD" "Redis password"

# Bank Account Information
create_secure_parameter "citi-account-number" "REPLACE_WITH_ACCOUNT_NUMBER" "Citi account number"
create_secure_parameter "citi-routing-number" "REPLACE_WITH_ROUTING_NUMBER" "Citi routing number"
create_secure_parameter "jpmorgan-account-number" "REPLACE_WITH_ACCOUNT_NUMBER" "JPMorgan account number"
create_secure_parameter "jpmorgan-routing-number" "REPLACE_WITH_ROUTING_NUMBER" "JPMorgan routing number"

echo "Creating non-sensitive parameters..."

# Application Configuration
aws ssm put-parameter \
    --name "/equity-shield/production-host" \
    --value "0.0.0.0" \
    --type "String" \
    --description "Production host" \
    --overwrite \
    --region "$AWS_REGION"

aws ssm put-parameter \
    --name "/equity-shield/production-port" \
    --value "8000" \
    --type "String" \
    --description "Production port" \
    --overwrite \
    --region "$AWS_REGION"

aws ssm put-parameter \
    --name "/equity-shield/waitress-threads" \
    --value "4" \
    --type "String" \
    --description "Number of Waitress threads" \
    --overwrite \
    --region "$AWS_REGION"

aws ssm put-parameter \
    --name "/equity-shield/cors-origins" \
    --value "https://your-domain.com,https://api.your-domain.com" \
    --type "String" \
    --description "CORS allowed origins" \
    --overwrite \
    --region "$AWS_REGION"

# Logging Configuration
aws ssm put-parameter \
    --name "/equity-shield/log-level" \
    --value "INFO" \
    --type "String" \
    --description "Log level" \
    --overwrite \
    --region "$AWS_REGION"

aws ssm put-parameter \
    --name "/equity-shield/log-format" \
    --value "json" \
    --type "String" \
    --description "Log format" \
    --overwrite \
    --region "$AWS_REGION"

# Rate Limiting
aws ssm put-parameter \
    --name "/equity-shield/rate-limit-per-minute" \
    --value "60" \
    --type "String" \
    --description "Rate limit per minute" \
    --overwrite \
    --region "$AWS_REGION"

aws ssm put-parameter \
    --name "/equity-shield/rate-limit-burst" \
    --value "100" \
    --type "String" \
    --description "Rate limit burst" \
    --overwrite \
    --region "$AWS_REGION"

echo "Parameters created successfully!"
echo "IMPORTANT: Remember to update the sensitive parameter values with secure credentials!"
echo "You can update parameters using:"
echo "aws ssm put-parameter --name \"/equity-shield/parameter-name\" --value \"new-value\" --type \"SecureString\" --overwrite"
