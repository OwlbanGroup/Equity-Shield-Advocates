# Verify Equity Shield Advocates Deployment
# This script performs post-deployment verification checks

param(
    [Parameter(Mandatory=$true)]
    [string]$AwsRegion,
    
    [Parameter(Mandatory=$true)]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$ApiEndpoint
)

$ErrorActionPreference = "Stop"

Write-Host "Starting deployment verification..."

# 1. Check Infrastructure Components
Write-Host "Checking infrastructure components..."

# VPC and Networking
$vpc = aws cloudformation describe-stacks --stack-name equity-shield-network --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($vpc | ConvertFrom-Json).Stacks[0].StackStatus -ne 'CREATE_COMPLETE') {
    Write-Error "VPC stack verification failed"
}
Write-Host "VPC stack status: " ($vpc | ConvertFrom-Json).Stacks[0].StackStatus

# Security Groups
$security = aws cloudformation describe-stacks --stack-name equity-shield-security --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($security | ConvertFrom-Json).Stacks[0].StackStatus -ne 'CREATE_COMPLETE') {
    Write-Error "Security stack verification failed"
}
Write-Host "Security stack status: " ($security | ConvertFrom-Json).Stacks[0].StackStatus

# SSL Certificate
$ssl = aws cloudformation describe-stacks --stack-name equity-shield-ssl --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($ssl | ConvertFrom-Json).Stacks[0].StackStatus -ne 'CREATE_COMPLETE') {
    Write-Error "SSL certificate verification failed"
}
Write-Host "SSL stack status: " ($ssl | ConvertFrom-Json).Stacks[0].StackStatus

# 2. Check Database Connectivity
Write-Host "Verifying database connectivity..."
$dbInstance = aws rds describe-db-instances --db-instance-identifier equity-shield-db --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($dbInstance | ConvertFrom-Json).DBInstances[0].DBInstanceStatus -ne 'available') {
    Write-Error "Database instance verification failed"
}
Write-Host "Database status: " ($dbInstance | ConvertFrom-Json).DBInstances[0].DBInstanceStatus

# 3. Check Redis Connectivity
Write-Host "Verifying Redis connectivity..."
$redis = aws elasticache describe-cache-clusters --cache-cluster-id equity-shield-redis --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($redis | ConvertFrom-Json).CacheClusters[0].CacheClusterStatus -ne 'available') {
    Write-Error "Redis cluster verification failed"
}
Write-Host "Redis status: " ($redis | ConvertFrom-Json).CacheClusters[0].CacheClusterStatus

# 4. Check ECS Service Health
Write-Host "Checking ECS service health..."
$service = aws ecs describe-services `
    --cluster equity-shield-cluster `
    --services equity-shield-api `
    --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($service | ConvertFrom-Json).services[0].status -ne 'ACTIVE') {
    Write-Error "ECS service verification failed"
}
Write-Host "ECS service status: " ($service | ConvertFrom-Json).services[0].status

# 5. Verify API Endpoints
Write-Host "Verifying API endpoints..."

# Health Check
Write-Host "Testing health check endpoint..."
$health = Invoke-WebRequest -Uri "$ApiEndpoint/health" -UseBasicParsing
if ($health.StatusCode -ne 200) {
    Write-Error "Health check endpoint failed"
}

# Protected Endpoint with API Key
Write-Host "Testing protected endpoint..."
$apiKey = aws ssm get-parameter --name "/equity-shield/api-key" --with-decryption --region $AwsRegion
$headers = @{
    "X-API-KEY" = $apiKey.Parameter.Value
}
$protected = Invoke-WebRequest -Uri "$ApiEndpoint/api/corporate-data" -Headers $headers -UseBasicParsing
if ($protected.StatusCode -ne 200) {
    Write-Error "Protected endpoint verification failed"
}

# 6. Check CloudWatch Logs
Write-Host "Verifying CloudWatch logs..."
$logs = aws logs describe-log-streams `
    --log-group-name /ecs/equity-shield-api `
    --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($logs | ConvertFrom-Json).logStreams.Count -eq 0) {
    Write-Error "CloudWatch logs verification failed"
}
Write-Host "CloudWatch log streams found: " ($logs | ConvertFrom-Json).logStreams.Count

# 7. Check CloudWatch Alarms
Write-Host "Verifying CloudWatch alarms..."
$alarms = aws cloudwatch describe-alarms `
    --alarm-names equity-shield-api-errors `
    --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($alarms | ConvertFrom-Json).MetricAlarms[0].StateValue -eq 'ALARM') {
    Write-Error "CloudWatch alarms verification failed"
}
Write-Host "Alarm state: " ($alarms | ConvertFrom-Json).MetricAlarms[0].StateValue

# 8. Check SSL Certificate Status
Write-Host "Verifying SSL certificate status..."
$cert = aws acm describe-certificate `
    --certificate-arn (Get-SSLCertificateArn) `
    --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($cert | ConvertFrom-Json).Certificate.Status -ne 'ISSUED') {
    Write-Error "SSL certificate status verification failed"
}
Write-Host "Certificate status: " ($cert | ConvertFrom-Json).Certificate.Status

# 9. Verify Load Balancer
Write-Host "Checking load balancer health..."
$alb = aws elbv2 describe-load-balancers `
    --names equity-shield-alb `
    --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($alb | ConvertFrom-Json).LoadBalancers[0].State.Code -ne 'active') {
    Write-Error "Load balancer verification failed"
}
Write-Host "Load balancer state: " ($alb | ConvertFrom-Json).LoadBalancers[0].State.Code

# 10. Check Auto Scaling
Write-Host "Verifying auto scaling configuration..."
$scaling = aws application-autoscaling describe-scaling-policies `
    --service-namespace ecs `
    --region $AwsRegion
if ($LASTEXITCODE -ne 0 -or ($scaling | ConvertFrom-Json).ScalingPolicies.Count -eq 0) {
    Write-Error "Auto scaling verification failed"
}
Write-Host "Scaling policies found: " ($scaling | ConvertFrom-Json).ScalingPolicies.Count

Write-Host "Deployment verification completed successfully!"
Write-Host "All components are operational and properly configured."
Write-Host ""
Write-Host "Summary:"
Write-Host "- Infrastructure: OK"
Write-Host "- Database: OK"
Write-Host "- Redis: OK"
Write-Host "- ECS Service: OK"
Write-Host "- API Endpoints: OK"
Write-Host "- Monitoring: OK"
Write-Host "- SSL: OK"
Write-Host "- Load Balancer: OK"
Write-Host "- Auto Scaling: OK"
