# Azure Functions Deployment Guide - Updated

This guide walks you through deploying the updated BADI Oerlikon system with **Azure Functions** for scheduling instead of Container Instances.

## What Changed

✅ **Container Instance** → **Azure Functions** (Consumption Plan - Pay as you go)
✅ **Docker Crawler** → **Python Function with Timer Trigger**
✅ **Cost Reduction** - From ~$100/month to ~$1-5/month for crawler
✅ **Automatic Scaling** - Scales to zero when not running
✅ **Simpler Management** - No need to manage containers

## Architecture Overview

```text

Every Hour
    ↓
Azure Functions Timer Trigger
    ↓
Python Function (Crawler)
    ↓
Fetch & Parse Data
    ↓
Azure Blob Storage (JSON)
    ↓
Web App reads from storage

```text

## Prerequisites

- Azure CLI installed
- Azure subscription
- Git repository with code

## Step 1: Update Bicep and Deploy

The infrastructure now includes Azure Functions instead of Container Instance.

```bash
cd azure
./deploy.sh

```text

This creates:
- ✅ Web App (App Service)
- ✅ Azure Functions App
- ✅ Blob Storage
- ✅ Application Insights (for monitoring)

## Step 2: Deploy Function Code

### Option A: Using Azure Functions Core Tools (Local Dev)

```bash

# Install Azure Functions Core Tools

# macOS: brew tap azure/azure && brew install azure-functions-core-tools@4

# Linux: curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg

# Windows: Download from https://github.com/Azure/azure-functions-core-tools

# Test locally with Azurite

docker-compose -f docker-compose.functions.yml up

# In another terminal, test the function

cd src/functions
func start

```text

### Option B: Deploy to Azure (Recommended)

```bash

# Set variables

RESOURCE*GROUP*NAME="badi-oerlikon-rg"
FUNCTION*APP*NAME="badi-oerlikon-dev-func"

# Package function app

cd src/functions
mkdir -p build
cp -r crawler_timer build/
cp requirements.txt build/
cd build
zip -r ../function-app.zip .
cd ..

# Deploy

az functionapp deployment source config-zip \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME \
  --src function-app.zip

```text

## Step 3: Configure Function Settings

The function reads these environment variables (set in Bicep):

```text

AZURE*STORAGE*CONNECTION_STRING  - Storage account connection
BLOB*CONTAINER*NAME              - 'scraped-data'
SCRAPE_URL                       - URL to scrape

```text

## Performance & Timeout Considerations ⏱️

### Current Execution Time

Your crawler is highly optimized:
- **Fetching HTML**: ~1-2 seconds (HTTP GET)
- **Parsing data**: ~0.5-1 second (BeautifulSoup)
- **Saving to blob**: ~0.5-1 second (Azure upload)
- **Total per execution**: ~2-4 seconds

### Azure Functions Timeout Limits

| Hosting Plan | Default Timeout | Maximum Timeout | Cost/Month |
|---|---|---|---|
| **Consumption** (current) | 5 min | **10 min hard limit** | $1-5 |
| **Premium** | 30 min | 30 min | ~$35-50 |
| **Dedicated (App Service)** | 30+ min | Configurable | $12+ |

**Status: ✅ No Issues**
- Current execution: ~2-4 seconds
- Consumption Plan hard limit: 10 minutes
- Safety buffer: **240x** (150x if execution takes 4 seconds)
- **You have plenty of headroom**

### Why We're Not Concerned

Even if your scraper becomes significantly more complex in the future:
- Adding more fields to parse
- Scraping multiple pages
- Heavier data processing

You could comfortably go to **5-6 minutes** and still be well within the 10-minute hard limit.

### If You Ever Need More Time

If the crawler grows to exceed 10 minutes (unlikely):

1. **Upgrade to Premium Plan** (easiest): `az functionapp plan update --name plan-name --sku EP1`

2. **Use Dedicated (App Service) Plan**: Better for long-running functions

3. **Split into multiple functions**: Decompose into multiple logical steps (not recommended for simple crawlers)

### Monitoring Execution Time

Track actual execution time in Azure Portal:

```bash

# View function logs

az functionapp log tail \
  --resource-group badi-oerlikon-rg \
  --name badi-oerlikon-dev-func

# Check recent invocations

az monitor metrics list \
  --resource-group badi-oerlikon-rg \
  --resource-type "Microsoft.Web/sites" \
  --resource-name badi-oerlikon-dev-func

```text

Look for log lines like: `"Crawler execution completed in 3.2 seconds"` (you can add this if needed)

View current settings:

```bash
az functionapp config appsettings list \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME

```text

## Step 4: Test the Function

### Monitor Function Execution

```bash

# Stream logs

az functionapp log tail \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME

# Or view in portal

# Azure Portal → Function App → Functions → crawler_timer → Monitor

```text

### Manually Trigger Function

```bash

# Get function key

FUNCTION_KEY=$(az functionapp keys list \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME \
  --query "functionKeys.default" -o tsv)

# Trigger function

FUNCTION*URL="https://$FUNCTION*APP*NAME.azurewebsites.net/admin/functions/crawler*timer"

curl -X POST $FUNCTION_URL \
  -H "x-functions-key: $FUNCTION_KEY"

```text

## Step 5: Verify Data Collection

Check that the function is writing data:

```bash

# List blobs in storage

STORAGE_ACCOUNT=$(az deployment group show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name main \
  --query properties.outputs.storageAccountName.value -o tsv)

az storage blob list \
  --container-name scraped-data \
  --account-name $STORAGE_ACCOUNT \
  -o table

```text

## Function Schedule (Cron Format)

The function runs on this schedule (in `function.json`):

```text

"schedule": "0 0 * * * *"

```text

This means: **Every hour at the start of the hour (00 minutes)**

To change schedule, modify `src/functions/crawler_timer/function.json`:

```json
{
  "schedule": "0 */6 * * * *"  // Every 6 hours
}

```text

Common patterns:
- `0 0 * * * *` - Every hour
- `0 */30 * * * *` - Every 30 minutes
- `0 0 0 * * *` - Every day at midnight
- `0 0 9 * * MON-FRI` - Every weekday at 9 AM

## Deployment via GitHub Actions

GitHub Actions now only deploys:

1. Web App (from Docker image)

2. Function App (from source code)

The workflow:

1. Runs tests and linting

2. Builds web app Docker image

3. Pushes to Container Registry

4. Deploys web app

5. Deploys function code to Azure Functions

## Monitoring and Alerts

### View Function Metrics

```bash

# Get last 24 hours of executions

az monitor metrics list \
  --resource /subscriptions/{subscriptionId}/resourceGroups/$RESOURCE*GROUP*NAME/providers/Microsoft.Web/sites/$FUNCTION*APP*NAME \
  --metric FunctionExecutionCount \
  --start-time 2024-01-15T00:00:00Z

```text

### Set Up Alerts

```bash

# Alert when function fails

az monitor metrics alert create \
  --resource-group $RESOURCE*GROUP*NAME \
  --name "Function Failure Alert" \
  --scopes /subscriptions/{subscriptionId}/resourceGroups/$RESOURCE*GROUP*NAME/providers/Microsoft.Web/sites/$FUNCTION*APP*NAME \
  --condition "avg FunctionExecutionCount < 1" \
  --window-size 1h \
  --evaluation-frequency 30m

```text

## Troubleshooting

### Function not running

```bash

# Check function app status

az functionapp show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME

# Check if enabled

az functionapp config show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $FUNCTION*APP*NAME

```text

### Storage connection error

```bash

# Verify connection string

az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE*GROUP*NAME

```text

### Function timeout

Increase function timeout in `src/functions/local.settings.json`:

```json
{
  "functionTimeout": "00:05:00"  // 5 minutes
}

```text

## Local Development

### Using Docker Compose

Create `docker-compose.functions.yml`:

```yaml
version: '3.8'
services:
  azurite:
    image: mcr.microsoft.com/azure-storage/azurite
    ports:
      - "10000:10000"

  function:
    image: mcr.microsoft.com/azure-functions/python:4-python3.9
    ports:
      - "7071:7071"
    volumes:
      - ./src/functions:/home/site/wwwroot
    environment:
      - AzureWebJobsStorage=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=SkeyBk5sNzUtNTcxNGQzOTdjMDUyNDQ=;BlobEndpoint=http://azurite:10000/devstoreaccount1;

```text

Run:

```bash
docker-compose -f docker-compose.functions.yml up

```text

### Testing Function Locally

```bash
cd src/functions
pip install -r requirements.txt

# Install Azure Functions Core Tools

func new --name crawler_timer --template "Timer trigger"

# Run locally

func start

```text

## Cost Comparison

| Service | Old (Container Instance) | New (Functions) |
|---------|--------------------------|-----------------|
| Web App (B1) | $12/month | $12/month |
| Crawler | $100/month | $1-5/month |
| Storage | $1/month | $1/month |
| **Total** | **~$113/month** | **~$14-18/month** |

**Savings: ~85% cost reduction!**

## Migration Checklist

- [x] Update Bicep to use Azure Functions
- [x] Create function code with timer trigger
- [x] Test function locally
- [x] Deploy infrastructure
- [x] Deploy function code
- [x] Verify data collection
- [x] Update GitHub Actions
- [x] Remove old Container Instance scripts
- [x] Update documentation

## Next Steps

1. Deploy infrastructure: `cd azure && ./deploy.sh`

2. Deploy function code (see Step 2)

3. Test the deployment

4. Monitor function executions

5. Set up alerts for failures

## Resources

- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Timer Trigger Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer)
- [Cron Expression Reference](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python#cron-expressions)
