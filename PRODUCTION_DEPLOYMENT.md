# Production Deployment Guide

## Prerequisites

### AWS Setup
1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. AWS ECR repository created
4. AWS ECS cluster configured
5. AWS RDS instance for PostgreSQL database
6. AWS ElastiCache for Redis (rate limiting and caching)

### Required Secrets
Configure the following secrets in GitHub repository settings:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
SLACK_WEBHOOK_URL
```

### Environment Variables
The following environment variables must be set in production:
```
PRODUCTION_HOST=0.0.0.0
PRODUCTION_PORT=8000
WAITRESS_THREADS=4
API_KEY=<secure-api-key>
JWT_SECRET=<secure-jwt-secret>
CORS_ORIGINS=https://your-domain.com
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_BURST=100
LOG_LEVEL=INFO
LOG_FILE=/var/log/equity-shield/production.log
LOG_FORMAT=json
LOG_MAX_SIZE=100MB
LOG_BACKUP_COUNT=10
DB_HOST=<your-rds-endpoint>
DB_PORT=5432
DB_NAME=equity_shield
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>
REDIS_HOST=<your-elasticache-endpoint>
REDIS_PORT=6379
REDIS_PASSWORD=<your-redis-password>
```

## Deployment Steps

### 1. Database Setup
1. Connect to your AWS RDS instance
2. Run the database initialization script:
```bash
psql -h <your-rds-endpoint> -U <your-db-user> -d postgres -f scripts/Setup-Database.sql
```

### 2. Infrastructure Setup
1. Create an AWS ECR repository:
```bash
aws ecr create-repository --repository-name equity-shield-api
```

2. Create an ECS cluster:
```bash
aws ecs create-cluster --cluster-name equity-shield-cluster
```

3. Create an ECS task definition using the provided task-definition.json:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 3. Application Deployment
The CI/CD pipeline will automatically:
1. Run tests and security scans
2. Build and push Docker image to ECR
3. Deploy to ECS
4. Verify deployment

To manually trigger a deployment:
```bash
aws ecs update-service \
  --cluster equity-shield-cluster \
  --service equity-shield-api \
  --force-new-deployment
```

### 4. Monitoring Setup
1. Configure CloudWatch Logs:
```bash
aws logs create-log-group --log-group-name /ecs/equity-shield-api
```

2. Set up CloudWatch Alarms for:
- CPU utilization
- Memory utilization
- API response times
- Error rates
- Rate limiting metrics

### 5. Security Measures
1. Enable AWS WAF for the API
2. Configure security groups
3. Set up AWS Shield for DDoS protection
4. Enable AWS CloudTrail for API activity logging

### 6. Backup and Recovery
1. Configure automated RDS snapshots
2. Set up cross-region replication for disaster recovery
3. Implement regular configuration backups

## Verification

### 1. Health Check
Verify the deployment by accessing the health endpoint:
```bash
curl https://your-api-endpoint/health
```

### 2. Load Testing
Run load tests using the provided locustfile.py:
```bash
locust -f locustfile.py --host=https://your-api-endpoint
```

### 3. Security Testing
1. Run security scans:
```bash
bandit -r src/
safety check -r config/requirements.txt
```

2. Verify SSL configuration:
```bash
ssllabs-scan your-api-endpoint
```

## Rollback Procedure

If issues are detected:

1. Revert to previous task definition:
```bash
aws ecs update-service \
  --cluster equity-shield-cluster \
  --service equity-shield-api \
  --task-definition equity-shield-api:<previous-version>
```

2. Monitor the rollback:
```bash
aws ecs wait services-stable \
  --cluster equity-shield-cluster \
  --services equity-shield-api
```

## Maintenance

### Regular Tasks
1. Monitor error rates and performance metrics
2. Review and rotate security credentials
3. Apply security patches
4. Update SSL certificates
5. Review and optimize resource allocation

### Troubleshooting
1. Check application logs:
```bash
aws logs get-log-events \
  --log-group-name /ecs/equity-shield-api \
  --log-stream-name <stream-name>
```

2. Monitor ECS service events:
```bash
aws ecs describe-services \
  --cluster equity-shield-cluster \
  --services equity-shield-api
```

## Support
For production issues:
1. Check CloudWatch logs
2. Review ECS service status
3. Contact AWS support if needed
4. Escalate to development team for application-specific issues
