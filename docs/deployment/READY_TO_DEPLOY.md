# 🚀 Ready to Deploy - WebSocket Listener

**Status:** ✅ ALL SYSTEMS GO
**WebSocket Configured:** CrowdMonitor API (SSD-7 - BADI Oerlikon)
**Subscription ID:** cc569079-9e12-412d-8dfb-a5d60a028f75
**Region:** Recommended: westeurope

---

## What's Ready

### ✅ Code Implementation

```
src/functions/websocket_listener/
├── __init__.py                    ✅ Main handler (COMPLETE)
├── websocket_handler.py           ✅ CrowdMonitor WebSocket logic (COMPLETE)
├── function.json                  ✅ Timer: every 5 min (COMPLETE)
├── requirements.txt               ✅ All dependencies (COMPLETE)
└── local.settings.json            ✅ Local config (COMPLETE)
```

**Key Configuration:**
- WebSocket URL: `wss://badi-public.crowdmonitor.ch:9591/api`
- Target UID: `SSD-7` (BADI Oerlikon)
- Occupancy Field: `currentfill`
- Timer: Every 5 minutes (`0 */5 * * * *`)
- Expected: ~60 occupancy readings per window

### ✅ Azure Infrastructure

- Bicep templates: `azure/main.bicep` ✅
- GitHub Actions CI/CD: `.github/workflows/azure-deploy.yml` ✅
- Docker setup: `docker-compose.functions.yml` ✅

### ✅ Documentation

- `DEPLOYMENT_GUIDE_WEBSOCKET.md` - Complete deployment instructions
- `WEBSOCKET_BADI_IMPLEMENTATION.md` - BADI-specific implementation
- 25 total markdown files covering all aspects

---

## Quick Start (3 Steps)

### 1. Test Locally (Optional but Recommended)

```bash
# Start with Docker
docker-compose -f docker-compose.functions.yml up

# In another terminal
cd src/functions/websocket_listener
func start
```

**Expected Output:**
```
Connected to WebSocket: wss://badi-public.crowdmonitor.ch:9591/api
Sent 'all' command to WebSocket
Update 1: occupancy=45
Update 2: occupancy=45
... (60 updates total)
Collected 60 updates in 5-minute window
Stats: count=60, min=45, max=52, avg=48.3
```

### 2. Deploy Infrastructure

```bash
# Set variables
SUBSCRIPTION="cc569079-9e12-412d-8dfb-a5d60a028f75"
RESOURCE_GROUP="badi-oerlikon-rg"
REGION="westeurope"

# Authenticate
az login
az account set --subscription $SUBSCRIPTION

# Create resource group
az group create --name $RESOURCE_GROUP --location $REGION

# Deploy infrastructure
cd azure
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file main.bicep \
  --parameters \
    webAppName=badi-oerlikon-app \
    functionAppName=badi-oerlikon-func \
    storageAccountName=badioerlikon \
    location=$REGION
```

### 3. Deploy Function Code

```bash
# Package function
cd src/functions/websocket_listener
mkdir -p build
cp __init__.py websocket_handler.py function.json requirements.txt build/
cd build && zip -r ../websocket-listener.zip . && cd ..

# Deploy
FUNCTION_APP="badi-oerlikon-func"
az functionapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FUNCTION_APP \
  --src websocket-listener.zip

# Set environment variables
STORAGE_ACCOUNT="badioerlikon"
CONN_STRING=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query connectionString -o tsv)

az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    WEBSOCKET_URL="wss://badi-public.crowdmonitor.ch:9591/api" \
    TARGET_UID="SSD-7" \
    AZURE_STORAGE_CONNECTION_STRING="$CONN_STRING"
```

### 4. Verify

```bash
# View logs (should see updates immediately)
az functionapp log tail \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP
```

---

## What You'll Get

### Data Collection

```json
{
  "window": {
    "start": "2026-02-17T10:00:00Z",
    "end": "2026-02-17T10:05:02Z",
    "duration_seconds": 300
  },
  "target_uid": "SSD-7",
  "updates": [
    {"occupancy": 45, "timestamp": "2026-02-17T10:00:00Z"},
    {"occupancy": 45, "timestamp": "2026-02-17T10:00:05Z"},
    {"occupancy": 46, "timestamp": "2026-02-17T10:00:10Z"},
    ... (57 more) ...
  ],
  "statistics": {
    "count": 60,
    "min": 45,
    "max": 52,
    "avg": 48.3,
    "median": 48
  }
}
```

### Storage Location

```
Blob Container: scraped-data/
├── 2026-02-17/
│   ├── 10-00-to-10-05.json    ← 60 readings
│   ├── 10-05-to-10-10.json    ← 60 readings
│   ├── 10-10-to-10-15.json    ← 60 readings
│   └── ... (288 files per day)
```

---

## Performance & Costs

### Performance Metrics

| Metric | Value |
|--------|-------|
| Function execution | ~1-2 sec CPU |
| Updates per window | ~60 |
| Readings per day | ~17,280 |
| Timeout safety | 150-300x buffer |
| Success rate | >99% expected |

### Monthly Costs

```
App Service (B1):         $12.00
Blob Storage:              $1.00
Application Insights:      $0.50
Azure Functions:           $0.96
────────────────────────────────
TOTAL:                    $14.46/month

vs. Hourly scraper:       $13.66/month
Extra cost:               +$0.80/month
Data improvement:         +71,900%

ROI: Exceptional ✅
```

---

## Architecture Diagram

```
Every 5 minutes:

Scheduled Timer
        ↓
Azure Function triggers
        ↓
Connect to CrowdMonitor WebSocket
        ├─ URL: wss://badi-public.crowdmonitor.ch:9591/api
        ├─ Send: "all" command
        ├─ Receive: JSON array of all locations
        └─ Filter: SSD-7 only
        ↓
Listen for 5 minutes
        ├─ ~60 occupancy updates
        ├─ One every 5 seconds
        └─ Extract: currentfill field
        ↓
Calculate statistics
        ├─ count, min, max, avg, median
        └─ Trend analysis
        ↓
Save to Azure Blob Storage
        ├─ Format: JSON
        ├─ Path: 2026-02-17/10-00-to-10-05.json
        └─ Compressed with archive tier
        ↓
Wait for next 5-minute window
```

---

## Deployment Checklist

- [ ] Azure subscription configured (`cc569079-9e12-412d-8dfb-a5d60a028f75`)
- [ ] Azure CLI installed and authenticated
- [ ] Resource group created (`badi-oerlikon-rg`)
- [ ] Bicep infrastructure deployed
- [ ] Function app created
- [ ] WebSocket listener code deployed
- [ ] Environment variables set
- [ ] Logs show successful connection
- [ ] Data appearing in blob storage
- [ ] Monitor set up for alerts

---

## Monitoring Commands

```bash
# View logs in real-time
az functionapp log tail \
  --name badi-oerlikon-func \
  --resource-group badi-oerlikon-rg \
  --follow

# Check invocations
az monitor metrics list \
  --resource-group badi-oerlikon-rg \
  --resource-type "Microsoft.Web/sites" \
  --resource-name badi-oerlikon-func \
  --metric Invocations

# List blob storage files
az storage blob list \
  --container-name scraped-data \
  --account-name badioerlikon \
  --query "[].name" -o table
```

---

## Next Steps

1. **Deploy locally first** (optional but recommended)
   - Takes 5 minutes
   - Verifies WebSocket connection works
   - See real data flowing

2. **Deploy to Azure** (30 minutes)
   - Follow "Quick Start" section above
   - Verify logs show successful connection
   - Check blob storage for data

3. **Run in parallel** (1 week)
   - Keep existing hourly scraper running
   - Monitor WebSocket listener for reliability
   - Compare data accuracy

4. **Switch over** (after 1 week validation)
   - Verify data consistency
   - Stop hourly scraper
   - Monitor WebSocket-only system

---

## Support & Troubleshooting

**See these files for detailed help:**
- `DEPLOYMENT_GUIDE_WEBSOCKET.md` - Detailed deployment steps
- `WEBSOCKET_BADI_IMPLEMENTATION.md` - Implementation details
- `TIMEOUT_CONSIDERATIONS.md` - Timeout analysis
- `PROJECT_STATUS.md` - Complete status checklist

**Common Issues:**

| Issue | Solution |
|-------|----------|
| WebSocket connection fails | Check firewall/network, try local test first |
| No data in blob storage | Check logs for parsing errors, verify UID is "SSD-7" |
| Function timeout | Won't happen (2-4s < 10min limit), but check logs |
| High costs | Monitor invocation count, adjust timer if needed |

---

## Key Files

```
Ready-to-deploy code:
├── src/functions/websocket_listener/__init__.py
├── src/functions/websocket_listener/websocket_handler.py
├── src/functions/websocket_listener/function.json
├── src/functions/websocket_listener/requirements.txt
└── src/functions/websocket_listener/local.settings.json

Deployment:
├── DEPLOYMENT_GUIDE_WEBSOCKET.md (THIS IS YOUR MAIN GUIDE)
├── azure/main.bicep
└── .github/workflows/azure-deploy.yml
```

---

## Status Summary

| Component | Status | Details |
|-----------|--------|---------|
| Code | ✅ Ready | All files in place, WebSocket configured |
| Configuration | ✅ Ready | CrowdMonitor API, SSD-7, currentfill field |
| Infrastructure | ✅ Ready | Bicep templates, CI/CD pipeline |
| Documentation | ✅ Ready | 25 markdown guides |
| Subscription | ✅ Ready | cc569079-9e12-412d-8dfb-a5d60a028f75 |
| **DEPLOYMENT** | 🚀 **READY** | **Execute Quick Start above** |

---

## Final Verification

Before deploying, verify you have:

```bash
✅ Azure CLI installed:        az --version
✅ Azure Functions Core Tools:  func --version
✅ Subscription access:         az account list
✅ Python 3.9+:               python3 --version
✅ WebSocket access:           telnet badi-public.crowdmonitor.ch 9591
✅ Internet connectivity:       curl https://www.google.com
```

---

## Ready? 🚀

All systems are configured and ready to deploy!

**Start with:** Follow the "Quick Start (3 Steps)" section above.

**Questions?** See `DEPLOYMENT_GUIDE_WEBSOCKET.md` for detailed instructions.

**Let's go!** 🎉
