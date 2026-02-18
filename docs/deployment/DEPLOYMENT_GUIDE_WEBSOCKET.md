# Deployment Guide - WebSocket Listener

**Subscription ID:** `cc569079-9e12-412d-8dfb-a5d60a028f75`

---

## Prerequisites

```bash

# Install Azure CLI

brew install azure-cli  # macOS

# or

sudo apt-get install azure-cli  # Linux

# Install Azure Functions Core Tools

brew tap azure/azure && brew install azure-functions-core-tools@4

# Install Terraform

sudo apt-get install terraform  # Linux

# or

brew install terraform  # macOS

# Install Python requirements

pip install -r requirements.txt

```text

---

## Step 1: Authenticate with Azure

```bash
az login
az account set --subscription cc569079-9e12-412d-8dfb-a5d60a028f75

```text

---

## Step 2: Test Locally

### Option A: With Docker and Azurite

```bash

# In project root

docker-compose -f docker-compose.functions.yml up

# In another terminal

cd src/functions/websocket_listener
func start

```text

Expected output:

```text

Functions runtime started. Press CTRL+C to exit.
Now listening on: 127.0.0.1:7071
Http Functions:

Connected to WebSocket: wss://badi-public.crowdmonitor.ch:9591/api
Sent 'all' command to WebSocket
Update 1: occupancy=45
Update 2: occupancy=45
...
Collected 60 updates in 5-minute window
Stats: count=60, min=45, max=52, avg=48.3

```text

### Option B: Direct Test

```bash
cd src/functions/websocket_listener
func start --port 7071

```text

---

## Step 3: Deploy to Azure

### Prepare Terraform Variables

```bash
cd azure

# Copy and customize variables

cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your preferred values

# nano terraform.tfvars

```text

### Initialize and Validate Terraform

```bash
cd azure

# Initialize Terraform (downloads providers)

terraform init

# Validate configuration

terraform validate

# Plan deployment (preview changes)

terraform plan -out=tfplan

```text

### Deploy Infrastructure with Terraform

```bash
cd azure

# Apply the plan

terraform apply tfplan

# Or directly apply (will prompt for confirmation)

terraform apply

```text

This will create:
- Resource Group
- Storage Account (for data)
- Blob Containers (scraped-data, logs)
- App Service Plan (Basic B1)
- Web App
- Function Storage Account
- Application Insights
- Function App (Consumption Plan Y1)

### Configure Environment Variables

The Terraform deployment already configures most variables. Add these manually if needed:

```bash
RESOURCE_GROUP="badi-oerlikon-dev-rg"
FUNCTION_APP="badi-oerlikon-dev-func"

# Set WebSocket-specific settings

az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    WEBSOCKET_URL="wss://badi-public.crowdmonitor.ch:9591/api" \
    TARGET_UID="SSD-7"

```text

### Deploy Function Code

```bash
cd src/functions/websocket_listener

# Package

mkdir -p build
cp **init**.py build/
cp websocket_handler.py build/
cp function.json build/
cp requirements.txt build/
cd build && zip -r ../websocket-listener.zip . && cd ..

# Deploy

az functionapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FUNCTION_APP \
  --src websocket-listener.zip

```text

---

## Step 4: Verify Deployment

```bash

# Check function status

az functionapp show \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP

# View logs

az functionapp log tail \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP

# Expected output:

# [UTC] Function started

# [UTC] Connected to WebSocket: wss://badi-public.crowdmonitor.ch:9591/api

# [UTC] Sent 'all' command to WebSocket

# [UTC] Update 1: occupancy=45

# 

```text

---

## Step 5: Monitor

### View Function Invocations

```bash
az monitor metrics list \
  --resource-group $RESOURCE_GROUP \
  --resource-type "Microsoft.Web/sites/functions" \
  --resource-name "$FUNCTION*APP/websocket*listener" \
  --metric-names Invocations,Errors,Duration

```text

### Set Up Alerts

```bash

# Alert if function fails

az monitor metrics alert create \
  --name "Function Error Alert" \
  --resource-group $RESOURCE_GROUP \
  --scopes "/subscriptions/cc569079-9e12-412d-8dfb-a5d60a028f75/resourceGroups/$RESOURCE*GROUP/providers/Microsoft.Web/sites/$FUNCTION*APP" \
  --condition "total Errors > 0" \
  --window-size 5m \
  --evaluation-frequency 1m

```text

---

## Troubleshooting

### Function Not Running

```bash

# Check if function is enabled

az functionapp function show \
  --function-name websocket_listener \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP

# Check function app settings

az functionapp config appsettings list \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP

```text

### WebSocket Connection Failed

```bash

# Test WebSocket locally

python3 -c "
import asyncio
import websockets
import json

async def test():
    async with websockets.connect('wss://badi-public.crowdmonitor.ch:9591/api') as ws:
        await ws.send('all')
        msg = await ws.recv()
        data = json.loads(msg)
        print(f'Received {len(data)} items')
        for item in data:
            if item.get('uid') == 'SSD-7':
                print(f\"BADI Oerlikon: {item.get('currentfill')} guests\")
                break

asyncio.run(test())
"

```text

### Check Logs

```bash

# Stream logs in real-time

az functionapp log tail \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --follow

# View last 100 lines

az functionapp log tail \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --number 100

```text

---

## Rollback

If you need to revert to the hourly scraper:

```bash

# Deploy old crawler function instead

az functionapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FUNCTION_APP \
  --src src/functions/crawler_timer/crawler-timer.zip

```text

---

## Success Criteria

After deployment, verify:

- [ ] Function invokes every 5 minutes ✅
- [ ] Logs show "Connected to WebSocket" ✅
- [ ] Logs show "Update N: occupancy=XX" messages ✅
- [ ] Data saved to blob storage ✅
- [ ] No error messages in logs ✅
- [ ] Blob storage contains files like: `2026-02-17/10-00-to-10-05.json` ✅

---

## Next Steps

1. ✅ Deploy function code (this guide)

2. ✅ Verify data is flowing (5 minutes)

3. ⏳ Run for 1 week alongside old scraper

4. ⏳ Compare data accuracy

5. ⏳ Switch to WebSocket-only

6. ⏳ Monitor for data quality

**Ready to deploy?** Run the commands above!
