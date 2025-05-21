# Deploy AWS Infrastructure for Equity Shield Advocates
# This script deploys all AWS infrastructure components in the correct order

param(
    [Parameter(Mandatory=$true)]
    [string]$AwsRegion,
    
    [Parameter(Mandatory=$true)]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$DomainName
)

$ErrorActionPreference = "Stop"

Write-Host "Starting deployment of Equity Shield Advocates infrastructure..."

# 1. Deploy VPC and Network Infrastructure
Write-Host "Deploying VPC and networking components..."
aws cloudformation create-stack `
    --stack-name equity-shield-network `
    --template-body file://aws/network/vpc-config.json `
    --region $AwsRegion `
    --capabilities CAPABILITY_IAM

Write-Host "Waiting for network stack creation to complete..."
aws cloudformation wait stack-create-complete `
    --stack-name equity-shield-network `
    --region $AwsRegion

# 2. Create Security Groups
Write-Host "Creating security groups..."
aws cloudformation create-stack `
    --stack-name equity-shield-security `
    --template-body file://aws/security/security-groups.json `
    --region $AwsRegion

Write-Host "Waiting for security stack creation to complete..."
aws cloudformation wait stack-create-complete `
    --stack-name equity-shield-security `
    --region $AwsRegion

# 3. Create IAM Roles
Write-Host "Creating IAM roles..."
aws iam create-role `
    --role-name equity-shield-task-execution-role `
    --assume-role-policy-document file://aws/iam/task-execution-role.json

# 4. Request and Validate SSL Certificate
Write-Host "Requesting SSL certificate..."
aws cloudformation create-stack `
    --stack-name equity-shield-ssl `
    --template-body file://aws/ssl/certificate-config.json `
    --region $AwsRegion `
    --parameters ParameterKey=DomainName,ParameterValue=$DomainName

Write-Host "Waiting for SSL certificate validation..."
aws cloudformation wait stack-create-complete `
    --stack-name equity-shield-ssl `
    --region $AwsRegion

# 5. Create ECR Repository
Write-Host "Creating ECR repository..."
aws ecr create-repository `
    --repository-name equity-shield-api `
    --region $AwsRegion

# 6. Create ECS Cluster
Write-Host "Creating ECS cluster..."
aws ecs create-cluster `
    --cluster-name equity-shield-cluster `
    --region $AwsRegion

# 7. Create RDS Instance
Write-Host "Creating RDS instance..."
aws rds create-db-instance `
    --db-instance-identifier equity-shield-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --master-username admin `
    --master-user-password (New-Guid).ToString() `
    --allocated-storage 20 `
    --vpc-security-group-ids (Get-SecurityGroupId "equity-shield-rds-sg") `
    --db-subnet-group-name equity-shield-db-subnet-group

# 8. Create ElastiCache Redis Cluster
Write-Host "Creating Redis cluster..."
aws elasticache create-cache-cluster `
    --cache-cluster-id equity-shield-redis `
    --engine redis `
    --cache-node-type cache.t3.micro `
    --num-cache-nodes 1 `
    --security-group-ids (Get-SecurityGroupId "equity-shield-redis-sg")

# 9. Create Parameter Store Entries
Write-Host "Setting up Parameter Store entries..."
./scripts/setup-aws-parameters.sh

# 10. Create CloudWatch Log Groups
Write-Host "Creating CloudWatch log groups..."
aws logs create-log-group `
    --log-group-name /ecs/equity-shield-api `
    --region $AwsRegion

# 11. Set up CloudWatch Alarms
Write-Host "Setting up CloudWatch alarms..."
aws cloudwatch put-metric-alarm `
    --alarm-name equity-shield-api-errors `
    --alarm-description "Alert on API errors" `
    --metric-name Errors `
    --namespace AWS/ECS `
    --statistic Sum `
    --period 300 `
    --threshold 5 `
    --comparison-operator GreaterThanThreshold `
    --evaluation-periods 2 `
    --alarm-actions $SNSTopicArn

Write-Host "Infrastructure deployment completed successfully!"
Write-Host "Next steps:"
Write-Host "1. Update DNS records to point to the ALB"
Write-Host "2. Deploy the application using the CI/CD pipeline"
Write-Host "3. Verify all monitoring and alerting systems"
