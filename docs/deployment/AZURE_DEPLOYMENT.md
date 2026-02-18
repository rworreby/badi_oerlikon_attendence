# Azure Deployment Guide - BADI Oerlikon Attendance Tracker

This guide walks you through deploying the BADI Oerlikon Attendance Tracker to Azure.

## Architecture Overview

The solution consists of three main components:

1. **Web App Frontend** - Azure App Service (Python Flask)

2. **Blob Storage** - Azure Storage Account for storing scraped data

3. **Crawler Service** - Azure Container Instances for continuous scraping

```txt
┌─────────────────────────────────────────────────────────┐
│                   Azure Cloud                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐                 │
│  │  Web App     │◄────►│ Blob Storage │                 │
│  │ (Flask UI)   │      │  (scraped    │                 │
│  │              │      │   data)      │                 │
│  └──────────────┘      └──────────────┘                 │
│         ▲                      ▲                        │
│         │                      │                        │
│         └──────────┬───────────┘                        │
│                    │                                    │
│              ┌─────▼─────┐                              │
│              │  Crawler   │                             │
│              │ (Container │                             │
│              │ Instances) │                             │
│              └────────────┘                             │
│                                                         │
└─────────────────────────────────────────────────────────┘

```text

## Prerequisites

- Azure CLI installed and configured
- Docker installed (for local testing)
- A valid Azure subscription
- Git access to this repository

## Step 1: Prepare Azure Credentials

### 1.1 Log in to Azure

```bash
az login

```text

### 1.2 Set your subscription

```bash
az account set --subscription <SUBSCRIPTION_ID>

```text

### 1.3 Create a resource group

```bash
export RESOURCE*GROUP*NAME="badi-oerlikon-rg"
export LOCATION="eastus"

az group create \
  --name $RESOURCE*GROUP*NAME \
  --location $LOCATION

```text

## Step 2: Deploy Infrastructure

### 2.1 Deploy using Bicep

```bash
cd azure
./deploy.sh

```text

The deployment script will:

- Create a storage account with blob containers
- Set up an App Service Plan and Web App
- Configure a Container Registry
- Output resource information

### 2.2 Get Deployment Outputs

```bash
az deployment group show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name main \
  --query properties.outputs \
  -o table

```text

Save these outputs:

- `storageAccountName`
- `webAppUrl`
- `containerRegistryLoginServer`
- `storageAccountKey`

## Step 3: Configure Web App

### 3.1 Get Storage Connection String

```bash
STORAGE*ACCOUNT*NAME=$(az deployment group show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name main \
  --query properties.outputs.storageAccountName.value \
  -o tsv)

STORAGE*CONNECTION*STRING=$(az storage account show-connection-string \
  --name $STORAGE*ACCOUNT*NAME \
  --resource-group $RESOURCE*GROUP*NAME \
  -o tsv)

```text

### 3.2 Set App Settings

```bash
WEB*APP*NAME="badi-oerlikon-dev-app"

az webapp config appsettings set \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME \
  --settings \
    AZURE*STORAGE*CONNECTION*STRING="$STORAGE*CONNECTION_STRING" \
    BLOB*CONTAINER*NAME="scraped-data" \
    FLASK_ENV="production" \
    PORT="8000"

```text

## Step 4: Build and Push Docker Images

### 4.1 Log in to Container Registry

```bash
REGISTRY*LOGIN*SERVER=$(az deployment group show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name main \
  --query properties.outputs.containerRegistryLoginServer.value \
  -o tsv)

az acr login --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1)

```text

### 4.2 Build Web App Image

```bash
az acr build \
  --registry $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) \
  --image badi-webapp:latest \
  --file docker/Dockerfile.webapp \
  .

```text

### 4.3 Build Crawler Image

```bash
az acr build \
  --registry $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) \
  --image badi-crawler:latest \
  --file docker/Dockerfile.crawler \
  .

```text

## Step 5: Deploy Web App

### 5.1 Deploy from Container

```bash
az webapp config container set \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME \
  --docker-custom-image-name $REGISTRY*LOGIN*SERVER/badi-webapp:latest \
  --docker-registry-server-url https://$REGISTRY*LOGIN*SERVER \
  --docker-registry-server-user $(az acr credential show --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) --query username -o tsv) \
  --docker-registry-server-password $(az acr credential show --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) --query passwords[0].value -o tsv)

```text

### 5.2 Enable continuous deployment

```bash
az webapp deployment container config \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME \
  --enable-cd true

```text

## Step 6: Set up Continuous Crawler

### 6.1 Create Azure Container Instance

```bash
az container create \
  --resource-group $RESOURCE*GROUP*NAME \
  --name badi-crawler \
  --image $REGISTRY*LOGIN*SERVER/badi-crawler:latest \
  --registry-login-server $REGISTRY*LOGIN*SERVER \
  --registry-username $(az acr credential show --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) --query username -o tsv) \
  --registry-password $(az acr credential show --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) --query passwords[0].value -o tsv) \
  --restart-policy Always \
  --environment-variables \
    AZURE*STORAGE*CONNECTION*STRING="$STORAGE*CONNECTION_STRING" \
    BLOB*CONTAINER*NAME="scraped-data" \
    SCRAPE*INTERVAL*SECONDS="3600" \
    LOG_LEVEL="INFO"

```text

### 6.2 Alternatively: Use Azure Container Apps (recommended for production)

```bash
az containerapp create \
  --name badi-crawler \
  --resource-group $RESOURCE*GROUP*NAME \
  --image $REGISTRY*LOGIN*SERVER/badi-crawler:latest \
  --environment-variables \
    AZURE*STORAGE*CONNECTION*STRING="$STORAGE*CONNECTION_STRING" \
    BLOB*CONTAINER*NAME="scraped-data" \
    SCRAPE*INTERVAL*SECONDS="3600" \
  --min-replicas 1 \
  --max-replicas 1

```text

## Step 7: Verify Deployment

### 7.1 Check Web App Status

```bash
az webapp show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME \
  --query state -o tsv

```text

### 7.2 Get Web App URL

```bash
WEB*APP*URL=$(az webapp show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME \
  --query defaultHostName -o tsv)

echo "Web App URL: https://$WEB*APP*URL"

```text

### 7.3 Test the API

```bash

# Health check

curl https://$WEB*APP*URL/health

# Get latest data

curl https://$WEB*APP*URL/api/data/latest

# List blobs

curl https://$WEB*APP*URL/api/data/blobs

```text

### 7.4 Check Crawler Status

```bash
az container show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name badi-crawler \
  --query containers[0].instanceView.currentState.state -o tsv

# View logs

az container logs \
  --resource-group $RESOURCE*GROUP*NAME \
  --name badi-crawler

```text

## Step 8: Local Development

### 8.1 Set up local environment

```bash

# Create virtual environment

python3 -m venv venv
source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

```text

### 8.2 Configure local development

Create a `.env` file:

```text

AZURE*STORAGE*CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;...
BLOB*CONTAINER*NAME=scraped-data
SCRAPE_URL=https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder/oerlikon.html
SCRAPE*INTERVAL*SECONDS=3600
FLASK_ENV=development
FLASK_DEBUG=True

```text

### 8.3 Run locally with Docker Compose

```bash
docker-compose up

```text

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

```text

## Monitoring and Logs

### View App Service Logs

```bash
az webapp log tail \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME

```text

### View Blob Storage Contents

```bash
az storage blob list \
  --container-name scraped-data \
  --account-name $STORAGE*ACCOUNT*NAME \
  --account-key $STORAGE*ACCOUNT*KEY

```text

### View Container Instance Logs

```bash
az container logs \
  --resource-group $RESOURCE*GROUP*NAME \
  --name badi-crawler

```text

## Cleanup

To remove all resources:

```bash
az group delete \
  --resource-group $RESOURCE*GROUP*NAME \
  --yes --no-wait

```text

## Troubleshooting

### Issue: Web App shows error 500

**Solution:** Check app settings and logs

```bash
az webapp config appsettings list \
  --resource-group $RESOURCE*GROUP*NAME \
  --name $WEB*APP*NAME

```text

### Issue: Crawler not writing to blob storage

**Solution:** Verify connection string and permissions

```bash
az storage account show-connection-string \
  --name $STORAGE*ACCOUNT*NAME \
  --resource-group $RESOURCE*GROUP*NAME

```text

### Issue: Docker image push fails

**Solution:** Ensure you're logged in and image is built

```bash
az acr login --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1)
docker build -f docker/Dockerfile.webapp -t badi-webapp:latest .

```text

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
