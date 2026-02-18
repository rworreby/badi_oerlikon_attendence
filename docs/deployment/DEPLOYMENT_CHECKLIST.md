# Azure Deployment Checklist

Use this checklist to ensure you've completed all necessary steps for deploying to Azure.

## Prerequisites Checklist

- [ ] Azure subscription created and active
- [ ] Azure CLI installed (`az --version`)
- [ ] Docker installed (`docker --version`)
- [ ] Git configured (`git config user.name`)
- [ ] GitHub account with repository access
- [ ] Terminal/PowerShell access

## Azure Setup Checklist

### 1. Azure Account

- [ ] Azure subscription ID known
- [ ] Resource group naming decided (e.g., `badi-oerlikon-rg`)
- [ ] Azure region selected (e.g., `eastus`)
- [ ] Logged in to Azure CLI (`az login`)

### 2. Infrastructure Deployment

- [ ] Bicep files reviewed (`azure/main.bicep`)
- [ ] Parameters configured (`azure/parameters.bicepparam`)
- [ ] Deploy script executable (`chmod +x azure/deploy.sh`)
- [ ] Infrastructure deployed successfully
- [ ] Resource group created
- [ ] Storage account created
- [ ] App Service Plan created
- [ ] Web App created
- [ ] Container Registry created

### 3. Storage Configuration

- [ ] Storage account connection string obtained
- [ ] Connection string tested
- [ ] `scraped-data` container created
- [ ] `logs` container created
- [ ] Access keys rotated (if needed)

## Docker Setup Checklist

### 1. Local Development

- [ ] Docker Compose file reviewed (`docker-compose.yml`)
- [ ] Local images built (`docker build`)
- [ ] Azurite container works (`docker-compose up azurite`)
- [ ] Local development tested

### 2. Docker Images

- [ ] Web app Dockerfile reviewed (`docker/Dockerfile.webapp`)
- [ ] Crawler Dockerfile reviewed (`docker/Dockerfile.crawler`)
- [ ] Images build successfully
- [ ] Images tested locally

## GitHub Setup Checklist

### 1. Repository Configuration

- [ ] Repository cloned locally
- [ ] Remote URL verified (`git remote -v`)
- [ ] Branch structure set (main as default)
- [ ] `.gitignore` configured

### 2. GitHub Secrets (See GITHUB_SECRETS.md)

- [ ] `AZURE_CREDENTIALS` secret configured
- [ ] `RESOURCE*GROUP*NAME` secret configured
- [ ] `REGISTRY*LOGIN*SERVER` secret configured
- [ ] `REGISTRY_USERNAME` secret configured
- [ ] `REGISTRY_PASSWORD` secret configured
- [ ] `AZURE*STORAGE*CONNECTION_STRING` secret configured
- [ ] `WEB*APP*NAME` secret configured
- [ ] `CRAWLER*CONTAINER*NAME` secret configured

### 3. GitHub Actions

- [ ] Workflow file exists (`.github/workflows/azure-deploy.yml`)
- [ ] Workflow permissions configured (Settings > Actions)
- [ ] Secrets accessible to workflow
- [ ] Workflow runs without errors

## Container Registry Setup Checklist

### 1. Authentication

- [ ] Logged in to Container Registry (`az acr login`)
- [ ] Credentials stored securely
- [ ] Service principal created for GitHub Actions

### 2. Images

- [ ] Web app image built (`badi-webapp:latest`)
- [ ] Crawler image built (`badi-crawler:latest`)
- [ ] Images pushed to registry
- [ ] Image tags verified

## Application Configuration Checklist

### 1. Web App Settings

- [ ] App settings configured:
  - [ ] `AZURE*STORAGE*CONNECTION_STRING`
  - [ ] `BLOB*CONTAINER*NAME`
  - [ ] `FLASK_ENV=production`
  - [ ] `PORT=8000`
- [ ] Container configuration set
- [ ] Startup command configured
- [ ] Health checks enabled

### 2. Crawler Configuration

- [ ] Container instance created
- [ ] Environment variables set:
  - [ ] `AZURE*STORAGE*CONNECTION_STRING`
  - [ ] `BLOB*CONTAINER*NAME`
  - [ ] `SCRAPE*INTERVAL*SECONDS`
  - [ ] `LOG_LEVEL`
- [ ] Restart policy set to `Always`
- [ ] Resource limits set

### 3. Environment Variables

- [ ] `.env.example` reviewed
- [ ] `.env` created locally (NOT committed)
- [ ] All required variables present
- [ ] No hardcoded credentials

## Testing Checklist

### 1. Local Testing

- [ ] Web app runs locally
- [ ] API endpoints respond
- [ ] Frontend loads
- [ ] Crawler executes
- [ ] Data saves to local storage
- [ ] Logs appear

### 2. Azure Testing

- [ ] Web app responds at Azure URL
- [ ] Health check passes (`/health`)
- [ ] Latest data endpoint works (`/api/data/latest`)
- [ ] Blob list endpoint works (`/api/data/blobs`)
- [ ] Dashboard displays correctly
- [ ] Auto-refresh works

### 3. Crawler Testing

- [ ] Crawler container runs
- [ ] Crawler logs appear
- [ ] Data appears in blob storage
- [ ] Timestamps are correct
- [ ] Error handling works

## Deployment Checklist

### 1. First Deployment

- [ ] All components tested
- [ ] Bicep validated (`az bicep validate`)
- [ ] Infrastructure deployed
- [ ] Images built and pushed
- [ ] Web app deployed
- [ ] Crawler deployed

### 2. Continuous Deployment

- [ ] GitHub Actions workflow runs
- [ ] Builds complete successfully
- [ ] Tests pass (if configured)
- [ ] Images pushed to registry
- [ ] Web app updated
- [ ] Deployment visible within 5 minutes

### 3. Rollback Procedure

- [ ] Previous image version available
- [ ] Rollback command documented
- [ ] Database backups available
- [ ] Recovery time documented

## Monitoring Checklist

### 1. Logging

- [ ] Application Insights configured (optional)
- [ ] App logs available (`az webapp log tail`)
- [ ] Crawler logs available (`az container logs`)
- [ ] Log retention policies set

### 2. Alerts

- [ ] Alert rule created for high error rate
- [ ] Alert rule created for crawler failure
- [ ] Alert rule created for storage quota
- [ ] Notification email configured

### 3. Metrics

- [ ] Response time monitored
- [ ] Error rate monitored
- [ ] Storage usage monitored
- [ ] Crawler success rate monitored

## Security Checklist

- [ ] HTTPS enabled (automatic on App Service)
- [ ] Connection strings in Key Vault (optional)
- [ ] Azure Firewall configured (if needed)
- [ ] NSG rules applied (if needed)
- [ ] Managed Identity configured (optional)
- [ ] API keys rotated
- [ ] Secrets not in code
- [ ] `.env` not committed

## Documentation Checklist

- [ ] README.md updated with Azure info
- [ ] QUICKSTART.md completed
- [ ] AZURE_DEPLOYMENT.md completed
- [ ] ARCHITECTURE.md completed
- [ ] TRANSFORMATION_SUMMARY.md completed
- [ ] GITHUB_SECRETS.md completed
- [ ] Runbooks created for common tasks
- [ ] Troubleshooting guide created

## Performance Checklist

- [ ] Response time measured
- [ ] Database query performance checked
- [ ] Image sizes optimized
- [ ] CDN configured (optional)
- [ ] Caching enabled
- [ ] Compression enabled

## Cost Optimization Checklist

- [ ] Cheapest appropriate tier selected
- [ ] Auto-scaling rules configured
- [ ] Unused resources removed
- [ ] Storage lifecycle policies set
- [ ] Reserved instances considered
- [ ] Spot instances used for crawler

## Maintenance Checklist

### Daily

- [ ] Check alerts
- [ ] Verify data is being updated
- [ ] Monitor error logs

### Weekly

- [ ] Review metrics
- [ ] Check storage usage
- [ ] Test manual processes

### Monthly

- [ ] Review costs
- [ ] Update dependencies
- [ ] Audit access
- [ ] Rotate secrets

## Post-Deployment Checklist

- [ ] Web app URL shared with stakeholders
- [ ] Documentation linked in README
- [ ] Team trained on operations
- [ ] On-call process established
- [ ] Disaster recovery tested
- [ ] Backup procedures verified
- [ ] Performance baselines established

## Sign-Off Checklist

- [ ] Technical lead reviewed architecture
- [ ] Security review completed
- [ ] Cost review approved
- [ ] Performance requirements met
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Deployment ready for production

---

## Notes

Use this section to document:
- Deployment date: _____________**
- Deployed by: **___________**
- Issues encountered: **___________**
- Resolution steps taken: **___________**
- Next steps: **_____________

---

## References

- QUICKSTART.md
- AZURE_DEPLOYMENT.md
- ARCHITECTURE.md
- GITHUB_SECRETS.md
- TRANSFORMATION_SUMMARY.md
