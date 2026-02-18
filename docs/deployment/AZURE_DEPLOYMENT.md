# Azure Deployment Guide - BADI Oerlikon Attendance Tracker

This guide walks you through deploying the BADI Oerlikon Attendance Tracker to Azure.

## Architecture Overview

The solution consists of three main components:

1. **Web App Frontend** - Azure App Service (Python Flask)
2. **Blob Storage** - Azure Storage Account for storing scraped data
3. **Crawler Service** - Azure Container Instances for continuous scraping

```
┌─────────────────────────────────────────────────────────┐
│                   Azure Cloud                            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐      ┌──────────────┐                 │
│  │  Web App     │◄────►│ Blob Storage │                 │
│  │ (Flask UI)   │      │  (scraped    │                 │
│  │              │      │   data)      │                 │
│  └──────────────┘      └──────────────┘                 │
│         ▲                      ▲                         │
│         │                      │                         │
│         └──────────┬───────────┘                         │
│                    │                                     │
│              ┌─────▼─────┐                               │
│              │  Crawler   │                              │
│              │ (Container │                              │
│              │ Instances) │                              │
│              └────────────┘                              │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

- Azure CLI installed and configured
- Docker installed (for local testing)
- A valid Azure subscription
- Git access to this repository

## Step 1: Prepare Azure Credentials

### 1.1 Log in to Azure

```bash
az login
```

### 1.2 Set your subscription

```bash
az account set --subscription <SUBSCRIPTION_ID>
```

### 1.3 Create a resource group

```bash
export RESOURCE_GROUP_NAME="badi-oerlikon-rg"
export LOCATION="eastus"

az group create \
  --name $RESOURCE_GROUP_NAME \
  --location $LOCATION
```

## Step 2: Deploy Infrastructure

### 2.1 Deploy using Bicep

```bash
cd azure
./deploy.sh
```

The deployment script will:
- Create a storage account with blob containers
- Set up an App Service Plan and Web App
- Configure a Container Registry
- Output resource information

### 2.2 Get Deployment Outputs

```bash
az deployment group show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name main \
  --query properties.outputs \
  -o table
```

Save these outputs:
- `storageAccountName`
- `webAppUrl`
- `containerRegistryLoginServer`
- `storageAccountKey`

## Step 3: Configure Web App

### 3.1 Get Storage Connection String

```bash
STORAGE_ACCOUNT_NAME=$(az deployment group show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name main \
  --query properties.outputs.storageAccountName.value \
  -o tsv)

STORAGE_CONNECTION_STRING=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  -o tsv)
```

### 3.2 Set App Settings

```bash
WEB_APP_NAME="badi-oerlikon-dev-app"

az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME \
  --settings \
    AZURE_STORAGE_CONNECTION_STRING="$STORAGE_CONNECTION_STRING" \
    BLOB_CONTAINER_NAME="scraped-data" \
    FLASK_ENV="production" \
    PORT="8000"
```

## Step 4: Build and Push Docker Images

### 4.1 Log in to Container Registry

```bash
REGISTRY_LOGIN_SERVER=$(az deployment group show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name main \
  --query properties.outputs.containerRegistryLoginServer.value \
  -o tsv)

az acr login --name $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1)
```

### 4.2 Build Web App Image

```bash
az acr build \
  --registry $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1) \
  --image badi-webapp:latest \
  --file docker/Dockerfile.webapp \
  .
```

### 4.3 Build Crawler Image

```bash
az acr build \
  --registry $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1) \
  --image badi-crawler:latest \
  --file docker/Dockerfile.crawler \
  .
```

## Step 5: Deploy Web App

### 5.1 Deploy from Container

```bash
az webapp config container set \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME \
  --docker-custom-image-name $REGISTRY_LOGIN_SERVER/badi-webapp:latest \
  --docker-registry-server-url https://$REGISTRY_LOGIN_SERVER \
  --docker-registry-server-user $(az acr credential show --name $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1) --query username -o tsv) \
  --docker-registry-server-password $(az acr credential show --name $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1) --query passwords[0].value -o tsv)
```

### 5.2 Enable continuous deployment

```bash
az webapp deployment container config \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME \
  --enable-cd true
```

## Step 6: Set up Continuous Crawler

### 6.1 Create Azure Container Instance

```bash
az container create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name badi-crawler \
  --image $REGISTRY_LOGIN_SERVER/badi-crawler:latest \
  --registry-login-server $REGISTRY_LOGIN_SERVER \
  --registry-username $(az acr credential show --name $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1) --query username -o tsv) \
  --registry-password $(az acr credential show --name $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1) --query passwords[0].value -o tsv) \
  --restart-policy Always \
  --environment-variables \
    AZURE_STORAGE_CONNECTION_STRING="$STORAGE_CONNECTION_STRING" \
    BLOB_CONTAINER_NAME="scraped-data" \
    SCRAPE_INTERVAL_SECONDS="3600" \
    LOG_LEVEL="INFO"
```

### 6.2 Alternatively: Use Azure Container Apps (recommended for production)

```bash
az containerapp create \
  --name badi-crawler \
  --resource-group $RESOURCE_GROUP_NAME \
  --image $REGISTRY_LOGIN_SERVER/badi-crawler:latest \
  --environment-variables \
    AZURE_STORAGE_CONNECTION_STRING="$STORAGE_CONNECTION_STRING" \
    BLOB_CONTAINER_NAME="scraped-data" \
    SCRAPE_INTERVAL_SECONDS="3600" \
  --min-replicas 1 \
  --max-replicas 1
```

## Step 7: Verify Deployment

### 7.1 Check Web App Status

```bash
az webapp show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME \
  --query state -o tsv
```

### 7.2 Get Web App URL

```bash
WEB_APP_URL=$(az webapp show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME \
  --query defaultHostName -o tsv)

echo "Web App URL: https://$WEB_APP_URL"
```

### 7.3 Test the API

```bash
# Health check
curl https://$WEB_APP_URL/health

# Get latest data
curl https://$WEB_APP_URL/api/data/latest

# List blobs
curl https://$WEB_APP_URL/api/data/blobs
```

### 7.4 Check Crawler Status

```bash
az container show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name badi-crawler \
  --query containers[0].instanceView.currentState.state -o tsv

# View logs
az container logs \
  --resource-group $RESOURCE_GROUP_NAME \
  --name badi-crawler
```

## Step 8: Local Development

### 8.1 Set up local environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 8.2 Configure local development

Create a `.env` file:

```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;...
BLOB_CONTAINER_NAME=scraped-data
SCRAPE_URL=https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder/oerlikon.html
SCRAPE_INTERVAL_SECONDS=3600
FLASK_ENV=development
FLASK_DEBUG=True
```

### 8.3 Run locally with Docker Compose

```bash
docker-compose up
```

This starts:
- Azurite (local Azure Storage emulator)
- Crawler service
- You can add the web app service to docker-compose.yml

### 8.4 Run individually

```bash
# Terminal 1: Web App
export FLASK_APP=src.api.app
flask run

# Terminal 2: Crawler (in another venv)
python -m src.crawler_main
```

## Monitoring and Logs

### View App Service Logs

```bash
az webapp log tail \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME
```

### View Blob Storage Contents

```bash
az storage blob list \
  --container-name scraped-data \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_ACCOUNT_KEY
```

### View Container Instance Logs

```bash
az container logs \
  --resource-group $RESOURCE_GROUP_NAME \
  --name badi-crawler
```

## Cleanup

To remove all resources:

```bash
az group delete \
  --resource-group $RESOURCE_GROUP_NAME \
  --yes --no-wait
```

## Troubleshooting

### Issue: Web App shows error 500

**Solution:** Check app settings and logs
```bash
az webapp config appsettings list \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $WEB_APP_NAME
```

### Issue: Crawler not writing to blob storage

**Solution:** Verify connection string and permissions
```bash
az storage account show-connection-string \
  --name $STORAGE_ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP_NAME
```

### Issue: Docker image push fails

**Solution:** Ensure you're logged in and image is built
```bash
az acr login --name $(echo $REGISTRY_LOGIN_SERVER | cut -d'.' -f1)
docker build -f docker/Dockerfile.webapp -t badi-webapp:latest .
```

## Cost Optimization

- Use **B1 App Service Plan** for dev/test (lowest cost)
- Set container instance to **0 replicas when idle**
- Use **Blob Storage lifecycle policies** to move old data to cool tier
- Consider **Azure Functions** for scheduled tasks instead of Container Instances

## Security Best Practices

1. Use **Managed Identities** for authentication (preferred over connection strings)
2. Store secrets in **Azure Key Vault**
3. Enable **HTTPS** on App Service
4. Configure **network security groups** to limit access
5. Use **private endpoints** for storage account

## Next Steps

1. Configure **Application Insights** for monitoring
2. Set up **CI/CD** with GitHub Actions
3. Add **auto-scaling** rules
4. Configure **Azure Front Door** for CDN and DDoS protection
5. Set up **backup and disaster recovery**
