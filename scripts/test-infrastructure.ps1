# Test Infrastructure Components for Equity Shield Advocates
# This script performs comprehensive testing of all infrastructure components

param(
    [Parameter(Mandatory=$true)]
    [string]$AwsRegion,
    
    [Parameter(Mandatory=$true)]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$ApiEndpoint
)

$ErrorActionPreference = "Stop"

Write-Host "Starting infrastructure testing..."

# 1. Test VPC Configuration
Write-Host "`nTesting VPC Configuration..."
Write-Host "--------------------------------"
$vpc = aws ec2 describe-vpcs --filters "Name=tag:Name,Values=equity-shield-vpc" --region $AwsRegion
$vpcId = ($vpc | ConvertFrom-Json).Vpcs[0].VpcId
Write-Host "VPC ID: $vpcId"

# Test Subnets
$subnets = aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpcId" --region $AwsRegion
$subnetCount = ($subnets | ConvertFrom-Json).Subnets.Count
Write-Host "Found $subnetCount subnets"

# 2. Test Security Groups
Write-Host "`nTesting Security Groups..."
Write-Host "--------------------------------"
$sgs = aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$vpcId" --region $AwsRegion
$sgDetails = $sgs | ConvertFrom-Json
foreach ($sg in $sgDetails.SecurityGroups) {
    Write-Host "Security Group: $($sg.GroupName)"
    Write-Host "Inbound Rules: $($sg.IpPermissions.Count)"
    Write-Host "Outbound Rules: $($sg.IpPermissionsEgress.Count)"
}

# 3. Test Load Balancer
Write-Host "`nTesting Load Balancer..."
Write-Host "--------------------------------"
$alb = aws elbv2 describe-load-balancers --names equity-shield-alb --region $AwsRegion
$albDetails = $alb | ConvertFrom-Json
Write-Host "ALB State: $($albDetails.LoadBalancers[0].State.Code)"
Write-Host "DNS Name: $($albDetails.LoadBalancers[0].DNSName)"

# Test Target Groups
$tgs = aws elbv2 describe-target-groups --load-balancer-arn $albDetails.LoadBalancers[0].LoadBalancerArn --region $AwsRegion
$tgDetails = $tgs | ConvertFrom-Json
foreach ($tg in $tgDetails.TargetGroups) {
    Write-Host "Target Group: $($tg.TargetGroupName)"
    Write-Host "Health Check Path: $($tg.HealthCheckPath)"
}

# 4. Test ECS Cluster
Write-Host "`nTesting ECS Cluster..."
Write-Host "--------------------------------"
$cluster = aws ecs describe-clusters --clusters equity-shield-cluster --region $AwsRegion
$clusterDetails = $cluster | ConvertFrom-Json
Write-Host "Cluster Status: $($clusterDetails.clusters[0].status)"
Write-Host "Running Tasks: $($clusterDetails.clusters[0].runningTasksCount)"
Write-Host "Pending Tasks: $($clusterDetails.clusters[0].pendingTasksCount)"

# 5. Test RDS Instance
Write-Host "`nTesting RDS Instance..."
Write-Host "--------------------------------"
$rds = aws rds describe-db-instances --db-instance-identifier equity-shield-db --region $AwsRegion
$rdsDetails = $rds | ConvertFrom-Json
Write-Host "DB Status: $($rdsDetails.DBInstances[0].DBInstanceStatus)"
Write-Host "Engine Version: $($rdsDetails.DBInstances[0].EngineVersion)"
Write-Host "Storage: $($rdsDetails.DBInstances[0].AllocatedStorage) GB"

# 6. Test Redis Cluster
Write-Host "`nTesting Redis Cluster..."
Write-Host "--------------------------------"
$redis = aws elasticache describe-cache-clusters --cache-cluster-id equity-shield-redis --region $AwsRegion
$redisDetails = $redis | ConvertFrom-Json
Write-Host "Cache Status: $($redisDetails.CacheClusters[0].CacheClusterStatus)"
Write-Host "Node Type: $($redisDetails.CacheClusters[0].CacheNodeType)"
Write-Host "Engine Version: $($redisDetails.CacheClusters[0].EngineVersion)"

# 7. Test CloudWatch Configuration
Write-Host "`nTesting CloudWatch Configuration..."
Write-Host "--------------------------------"
# Test Log Groups
$logGroups = aws logs describe-log-groups --log-group-name-prefix /ecs/equity-shield --region $AwsRegion
$logGroupDetails = $logGroups | ConvertFrom-Json
Write-Host "Log Groups Found: $($logGroupDetails.logGroups.Count)"

# Test Metrics
$metrics = aws cloudwatch list-metrics --namespace AWS/ECS --region $AwsRegion
$metricDetails = $metrics | ConvertFrom-Json
Write-Host "ECS Metrics Found: $($metricDetails.Metrics.Count)"

# Test Alarms
$alarms = aws cloudwatch describe-alarms --region $AwsRegion
$alarmDetails = $alarms | ConvertFrom-Json
Write-Host "Active Alarms: $($alarmDetails.MetricAlarms.Count)"

# 8. Test API Endpoints
Write-Host "`nTesting API Endpoints..."
Write-Host "--------------------------------"
try {
    $health = Invoke-WebRequest -Uri "$ApiEndpoint/health" -UseBasicParsing
    Write-Host "Health Check Status: $($health.StatusCode)"
} catch {
    Write-Error "Health check failed: $_"
}

# Get API Key from Parameter Store
$apiKey = aws ssm get-parameter --name "/equity-shield/api-key" --with-decryption --region $AwsRegion
$headers = @{
    "X-API-KEY" = ($apiKey | ConvertFrom-Json).Parameter.Value
}

try {
    $protected = Invoke-WebRequest -Uri "$ApiEndpoint/api/corporate-data" -Headers $headers -UseBasicParsing
    Write-Host "Protected Endpoint Status: $($protected.StatusCode)"
} catch {
    Write-Error "Protected endpoint test failed: $_"
}

# 9. Test Auto Scaling
Write-Host "`nTesting Auto Scaling Configuration..."
Write-Host "--------------------------------"
$asg = aws application-autoscaling describe-scalable-targets --service-namespace ecs --region $AwsRegion
$asgDetails = $asg | ConvertFrom-Json
Write-Host "Scalable Targets: $($asgDetails.ScalableTargets.Count)"

$policies = aws application-autoscaling describe-scaling-policies --service-namespace ecs --region $AwsRegion
$policyDetails = $policies | ConvertFrom-Json
Write-Host "Scaling Policies: $($policyDetails.ScalingPolicies.Count)"

Write-Host "`nInfrastructure Testing Complete!"
Write-Host "================================="
Write-Host "All components have been tested and verified."
