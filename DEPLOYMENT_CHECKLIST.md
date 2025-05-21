# Deployment Checklist

## Pre-Deployment

### AWS Infrastructure
- [ ] AWS account has required permissions
- [ ] AWS CLI is installed and configured
- [ ] ECR repository is created
- [ ] ECS cluster is set up
- [ ] RDS instance is provisioned
- [ ] ElastiCache cluster is configured
- [ ] Parameter Store is populated with secrets

### Security
- [ ] SSL certificates are obtained
- [ ] Security groups are configured
- [ ] IAM roles and policies are set up
- [ ] API keys are generated and secured
- [ ] JWT secrets are generated and secured
- [ ] WAF rules are configured

### Database
- [ ] Database is created and initialized
- [ ] Database backups are configured
- [ ] Database user permissions are set
- [ ] Connection strings are tested

### Application
- [ ] All tests pass
- [ ] Security scans pass
- [ ] Dependencies are up to date
- [ ] Environment variables are configured
- [ ] Health check endpoint responds correctly
- [ ] Rate limiting is configured
- [ ] CORS settings are correct

### CI/CD
- [ ] GitHub secrets are configured:
  - [ ] AWS_ACCESS_KEY_ID
  - [ ] AWS_SECRET_ACCESS_KEY
  - [ ] AWS_REGION
  - [ ] SLACK_WEBHOOK_URL
- [ ] ECR repository is specified in workflow
- [ ] Task definition is registered
- [ ] Service is created in ECS

## Deployment

### Infrastructure
- [ ] Run setup-aws-parameters.sh
- [ ] Verify Parameter Store values
- [ ] Check ECS cluster capacity
- [ ] Verify auto-scaling settings

### Database
- [ ] Run Setup-Database.sql
- [ ] Verify database connections
- [ ] Check replication if configured

### Application
- [ ] Build and push Docker image
- [ ] Deploy to ECS
- [ ] Verify health check endpoint
- [ ] Check application logs
- [ ] Monitor error rates

## Post-Deployment

### Verification
- [ ] API endpoints respond correctly
- [ ] Rate limiting works as expected
- [ ] Authentication is working
- [ ] CORS is properly configured
- [ ] Logs are being generated
- [ ] Metrics are being collected

### Monitoring
- [ ] CloudWatch alarms are set up
- [ ] Log groups are configured
- [ ] Metrics dashboards are created
- [ ] Alert notifications are working

### Documentation
- [ ] API documentation is updated
- [ ] Runbook is current
- [ ] Contact information is updated
- [ ] Incident response plan is in place

### Backup & Recovery
- [ ] Database backup is verified
- [ ] Restore procedure is tested
- [ ] Disaster recovery plan is documented
- [ ] Rollback procedure is verified

## Final Steps
- [ ] Team is notified of deployment
- [ ] Deployment is logged
- [ ] Documentation is distributed
- [ ] Support team is briefed
