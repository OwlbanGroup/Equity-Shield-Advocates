# Final Deployment Steps for Equity Shield Advocates

## Prerequisites
1. AWS CLI installed and configured with appropriate credentials
2. PowerShell 7.0 or later
3. Domain name registered and accessible
4. SSL certificate request prepared
5. All required secrets and credentials ready

## Step-by-Step Deployment Process

### 1. Initial Setup
```powershell
# Clone the repository and navigate to the project directory
git clone https://github.com/equity-shield-advocates/api.git
cd api

# Create a new branch for deployment
git checkout -b deployment
```

### 2. Configure Environment Variables
1. Copy the production environment template:
```powershell
Copy-Item production.env.example production.env
```

2. Update the following values in `production.env`:
- `API_KEY`: Generate a secure API key
- `JWT_SECRET`: Generate a secure JWT secret
- `DB_PASSWORD`: Set a strong database password
- `REDIS_PASSWORD`: Set a strong Redis password

### 3. Deploy AWS Infrastructure
```powershell
# Deploy core infrastructure
./scripts/deploy-aws-infrastructure.ps1 `
    -AwsRegion "us-east-1" `
    -Environment "production" `
    -DomainName "api.equity-shield-advocates.com"

# Wait for infrastructure deployment to complete (typically 15-20 minutes)
```

### 4. Configure DNS
1. Get the ALB DNS name from AWS Console
2. Create an A record pointing your domain to the ALB
3. Wait for DNS propagation (typically 15-30 minutes)

### 5. Initialize Database
```powershell
# Get the RDS endpoint from AWS Console
$DB_ENDPOINT="your-rds-endpoint"

# Run database initialization script
psql -h $DB_ENDPOINT -U admin -d equity_shield -f scripts/Setup-Database.sql
```

### 6. Deploy Application
```powershell
# Push changes to trigger CI/CD pipeline
git add .
git commit -m "Production deployment"
git push origin deployment

# Create and merge pull request to main branch
# This will trigger the deployment pipeline
```

### 7. Verify Deployment
```powershell
# Run verification script
./scripts/verify-deployment.ps1 `
    -AwsRegion "us-east-1" `
    -Environment "production" `
    -ApiEndpoint "https://api.equity-shield-advocates.com"
```

### 8. Post-Deployment Tasks

#### Monitor Application
1. Check CloudWatch logs for any errors
2. Verify CloudWatch alarms are active
3. Monitor API response times
4. Check resource utilization

#### Security Verification
1. Verify SSL certificate is properly installed
2. Confirm security groups are correctly configured
3. Validate API key authentication
4. Test rate limiting

#### Performance Testing
1. Run load tests using provided scripts
2. Monitor database performance
3. Check cache hit rates
4. Verify auto-scaling triggers

## Rollback Procedure

If issues are detected during deployment:

1. Revert to previous ECS task definition:
```powershell
aws ecs update-service `
    --cluster equity-shield-cluster `
    --service equity-shield-api `
    --task-definition equity-shield-api:<previous-version>
```

2. Monitor rollback:
```powershell
aws ecs wait services-stable `
    --cluster equity-shield-cluster `
    --services equity-shield-api
```

## Support and Maintenance

### Regular Maintenance Tasks
1. Review and rotate security credentials
2. Apply security patches
3. Update SSL certificates
4. Review and optimize resource allocation

### Monitoring
1. Set up email notifications for CloudWatch alarms
2. Monitor error rates and performance metrics
3. Review access logs regularly
4. Check database backup status

### Troubleshooting
1. Check application logs:
```powershell
aws logs get-log-events `
    --log-group-name /ecs/equity-shield-api `
    --log-stream-name <stream-name>
```

2. Monitor service health:
```powershell
aws ecs describe-services `
    --cluster equity-shield-cluster `
    --services equity-shield-api
```

## Contact Information

For urgent issues:
1. DevOps Team: devops@equity-shield-advocates.com
2. Security Team: security@equity-shield-advocates.com
3. Database Team: dba@equity-shield-advocates.com

## Additional Resources
- AWS Documentation: https://docs.aws.amazon.com
- Project Wiki: https://wiki.equity-shield-advocates.com
- Monitoring Dashboard: https://monitoring.equity-shield-advocates.com
