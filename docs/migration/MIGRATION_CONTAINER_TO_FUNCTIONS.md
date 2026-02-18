# Migration Guide: Container Instance → Azure Functions

This document explains the migration from Container Instances to Azure Functions.

## Why Azure Functions

| Feature | Container Instance | Azure Functions |
|---------|-----------------|-----------------|
| **Cost** | $100/month | $1-5/month |
| **Scaling** | Always running | Scales to zero |
| **Management** | Manual container updates | Automatic |
| **Cold Start** | N/A | ~3-5 seconds |
| **Billing** | Per second running | Per execution |
| **Development** | Docker required | Python functions |

## What Changed

### Architecture

### Before (Container Instance)

```text

GitHub → Build Docker image
  ↓
Push to Container Registry
  ↓
Create/update Container Instance
  ↓
Instance runs 24/7 with cron

```text

### After (Azure Functions)

```text

GitHub → Package Python code
  ↓
Deploy to Function App
  ↓
Timer trigger runs code every hour
  ↓
No containers, automatic scaling

```text

### Files Removed

```text

❌ docker/Dockerfile.crawler        - No longer needed
❌ src/services/crawler_service.py  - Simplified to function
❌ src/crawler_main.py              - Entry point not needed
❌ docker-compose.yml               - Replaced with .functions version
❌ src/db/                          - SQLAlchemy no longer used
❌ src/migrations/                  - Alembic migrations removed
❌ alembic.ini                      - Database config removed
❌ scripts/populate_db.py           - DB scripts removed

```text

### Files Added

```text

✅ src/functions/crawler_timer/**init**.py      - Function handler
✅ src/functions/crawler_timer/function.json    - Function config
✅ src/functions/requirements.txt               - Function dependencies
✅ src/functions/local.settings.json            - Local dev config
✅ docker-compose.functions.yml                 - Local testing
✅ AZURE*FUNCTIONS*GUIDE.md                     - Setup guide

```text

### Code Changes

### Before (Continuous Service)

```python

# src/services/crawler_service.py

class CrawlerService:
    def run_continuous(self):
        while self.is_running:
            self.scrape_once()
            time.sleep(3600)  # Sleep 1 hour

```text

### After (Function Handler)

```python

# src/functions/crawler_timer/**init**.py

def main(mytimer: func.TimerRequest) -> None:
    # Function runs when triggered by timer

    # No loop needed - Azure handles scheduling

    scrape_once()

```text

## Deployment Steps

### 1. Update Infrastructure

```bash
cd azure
./deploy.sh

```text

The Bicep template now creates:
- ✅ Function App (Consumption plan)
- ✅ Storage account for function runtime
- ✅ Application Insights (monitoring)

### 2. Deploy Function Code

```bash
cd src/functions
mkdir -p build
cp -r crawler_timer build/
cp requirements.txt build/
cd build
zip -r ../function-app.zip .
cd ..

az functionapp deployment source config-zip \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME \
  --src function-app.zip

```text

### 3. Test Function

```bash

# Monitor logs

az functionapp log tail \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME

# Or test locally with Docker Compose

docker-compose -f docker-compose.functions.yml up

```text

## GitHub Actions Changes

### Before
- Build Crawler Docker image
- Push to registry
- Create/update Container Instance
- Delete old container

### After
- Build Web App Docker image only
- Deploy Web App
- Package function code
- Deploy function code via zip

Removed CI/CD steps:

```yaml
❌ Build Crawler Docker Image
❌ Push Crawler Image
❌ Update Crawler Container

```text

## Configuration Changes

### Environment Variables

Location changed from Container Instance → Function App settings:

```bash

# Old way (Container Instance)

az container create ... --environment-variables \
  AZURE*STORAGE*CONNECTION_STRING="..."

# New way (Function App)

az functionapp config appsettings set \
  --settings AZURE*STORAGE*CONNECTION_STRING="..."

```text

### Schedule Configuration

### Old (Environment variable)

```bash
SCRAPE*INTERVAL*SECONDS=3600

```text

### New (function.json)

```json
{
  "schedule": "0 0 * * * *"  // Cron expression
}

```text

## Performance Considerations

### Cold Starts

- First execution: ~3-5 seconds
- Subsequent executions: <1 second
- Warmed up continuously during business hours

### Execution Time

- Typical scrape: 2-3 seconds
- Timeout default: 5 minutes
- Can be increased if needed

### Resource Usage

- Memory: 128 MB (default)
- CPU: Shared
- No pre-allocated resources

## Cost Analysis

### Old Setup (Container Instance)

```text

Execution time per run: ~5 seconds
Runs per month: 720 (hourly)
Total execution time: 3,600 seconds = 1 hour

Cost: $100/month for 24/7 instance

```text

### New Setup (Azure Functions)

```text

Execution time per run: ~5 seconds
Runs per month: 720 (hourly)
Total execution time: 3,600 seconds = 1 hour

Cost: ~$2-5/month (pay per execution + GB-seconds)

```text

**Monthly Savings: ~$95-98** (85% reduction)

## Monitoring

### Function Metrics

```bash

# View execution count

az monitor metrics list \
  --resource /subscriptions/{id}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{func-name} \
  --metric FunctionExecutionCount

# View errors

az monitor metrics list \
  --resource /subscriptions/{id}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{func-name} \
  --metric FunctionExecutionUnitsSum

```text

### Application Insights

View in Azure Portal:
- Functions → Monitor
- See execution history
- View logs and exceptions
- Track performance

## Rollback Plan

If you need to go back to Container Instance:

1. Keep old Bicep template backed up

2. Keep Container Instance image in registry

3. Redeploy infrastructure with old template

4. Update GitHub Actions workflow

## FAQ

**Q: Will the function run if I don't push code?**
A: Functions run on the schedule defined in function.json, regardless of code updates.

**Q: Can I manually trigger the function?**
A: Yes, via Azure Portal or CLI:

```bash
curl https://{function-app}.azurewebsites.net/admin/functions/crawler_timer \
  -H "x-functions-key: {key}"

```text

**Q: What if a function execution fails?**
A: Failed executions are logged in Application Insights and logs. You can set up alerts.

**Q: Can I change the schedule after deployment?**
A: Yes, modify `src/functions/crawler_timer/function.json` and redeploy.

**Q: How do I view function logs?**
A:

```bash
az functionapp log tail --resource-group {rg} --name {func-name}

```text

## Support Resources

- [Azure Functions Documentation](https://docs.microsoft.com/azure/azure-functions/)
- [Python Functions Developer Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Timer Trigger Reference](https://docs.microsoft.com/azure/azure-functions/functions-bindings-timer)

## Next Steps

1. Review this guide

2. Update infrastructure: `./azure/deploy.sh`

3. Deploy function code (Step 2 above)

4. Test locally: `docker-compose -f docker-compose.functions.yml up`

5. Monitor in Azure Portal

6. Set up alerts for failures

---

**Status**: ✅ Migration complete
**Deployment date**: [Your date]
**Cost savings**: ~85%
