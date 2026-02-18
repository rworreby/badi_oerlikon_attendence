# BADI Oerlikon Attendance Tracker - Quick Start Guide

This guide helps you quickly set up and deploy the BADI Oerlikon Attendance Tracker on Azure.

## What is this project?

This project scrapes swimming pool attendance data from the Stadt Zürich website and provides:
- **Real-time dashboard** showing pool occupancy
- **Historical data** stored in Azure Blob Storage
- **Continuous crawler service** that updates data every hour
- **REST API** for accessing data

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Cloud**: Azure (App Service, Blob Storage, Container Instances)
- **Deployment**: Docker, GitHub Actions, Bicep

## Quick Start (Local Development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd badi_oerlikon_attendence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings
# For local development, you can use Azurite (local storage emulator)
```

### 3. Run Locally with Docker Compose

```bash
# Start local services (Azurite + optional services)
docker-compose up

# In another terminal, run the web app
export FLASK_APP=src.api.app
flask run

# In another terminal, run the crawler
python -m src.crawler_main
```

### 4. Access the Dashboard

Open http://localhost:5000 in your browser

## Azure Deployment

### Prerequisites

```bash
# Install Azure CLI
# macOS: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# Windows: Installers available at https://aka.ms/azure-cli

# Login to Azure
az login

# Verify subscription
az account show
```

### 1-Minute Deploy

```bash
# Set your resource group
export RESOURCE_GROUP_NAME="badi-oerlikon-rg"
export LOCATION="eastus"

# Run the deployment script
cd azure
chmod +x deploy.sh
./deploy.sh

# Follow the on-screen instructions
```

### Detailed Deployment

See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for comprehensive step-by-step instructions.

## Project Structure

```
├── src/
│   ├── api/                    # Flask web app
│   │   ├── app.py              # Flask application
│   │   └── static/             # Frontend (HTML, CSS, JS)
│   ├── azure_storage/          # Azure integration
│   │   ├── blob_adapter.py     # Blob storage client
│   │   └── repository.py       # Data persistence
│   ├── services/               # Business logic
│   │   └── crawler_service.py  # Scraping service
│   ├── scraper/                # Web scraping
│   │   ├── fetcher.py          # HTTP requests
│   │   └── parser.py           # HTML parsing
│   ├── db/                     # Database models (legacy)
│   ├── utils/                  # Utilities
│   └── tests/                  # Unit tests
├── docker/                     # Docker configurations
│   ├── Dockerfile.webapp       # Web app container
│   └── Dockerfile.crawler      # Crawler container
├── azure/                      # Azure infrastructure
│   ├── main.bicep              # Infrastructure as Code
│   ├── parameters.bicepparam   # Deployment parameters
│   └── deploy.sh               # Deployment script
├── .github/workflows/          # CI/CD pipelines
├── docker-compose.yml          # Local development
├── requirements.txt            # Python dependencies
└── AZURE_DEPLOYMENT.md         # Detailed guide
```

## Key Features

### Web Dashboard
- Real-time occupancy status
- Color-coded indicators (green=available, yellow=busy, red=full)
- Historical data browser
- Auto-refresh capability

### API Endpoints
- `GET /health` - Health check
- `GET /api/data/latest` - Latest scraped data
- `GET /api/data/blobs` - List all data blobs
- `GET /api/data/<blob_name>` - Get specific data

### Continuous Crawler
- Runs in Azure Container Instances
- Configurable scrape interval (default 1 hour)
- Automatic retry on failure
- Logs to application insights

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage connection string | Required |
| `BLOB_CONTAINER_NAME` | Container for storing data | `scraped-data` |
| `SCRAPE_URL` | URL to scrape | BADI Oerlikon page |
| `SCRAPE_INTERVAL_SECONDS` | Scrape interval in seconds | 3600 |
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Enable debug mode | `False` |
| `PORT` | Port for web app | 8000 |
| `LOG_LEVEL` | Logging level | `INFO` |

## Common Tasks

### View Scraped Data

```bash
# Get latest data
curl https://your-app.azurewebsites.net/api/data/latest

# List all data files
curl https://your-app.azurewebsites.net/api/data/blobs

# Get specific file
curl https://your-app.azurewebsites.net/api/data/scraped_data_2024-01-15_14-30-45.json
```

### Check Crawler Status

```bash
# Get resource group name
RESOURCE_GROUP_NAME="badi-oerlikon-rg"

# View logs
az container logs \
  --resource-group $RESOURCE_GROUP_NAME \
  --name badi-crawler

# Check status
az container show \
  --resource-group $RESOURCE_GROUP_NAME \
  --name badi-crawler \
  --query containers[0].instanceView.currentState.state
```

### Monitor Storage Usage

```bash
# List files in blob storage
az storage blob list \
  --container-name scraped-data \
  --account-name your-storage-account \
  -o table

# Get storage account size
az storage account show \
  --name your-storage-account \
  --resource-group $RESOURCE_GROUP_NAME \
  --query primaryEndpoints.blob
```

## Troubleshooting

### Dashboard shows "Error loading data"

1. Check if the web app is running:
   ```bash
   az webapp show --name your-app-name --resource-group your-rg --query state
   ```

2. Check app logs:
   ```bash
   az webapp log tail --name your-app-name --resource-group your-rg
   ```

3. Verify storage connection:
   ```bash
   curl https://your-app.azurewebsites.net/health
   ```

### Crawler not updating data

1. Check container status:
   ```bash
   az container show --name badi-crawler --resource-group your-rg
   ```

2. Check logs:
   ```bash
   az container logs --name badi-crawler --resource-group your-rg
   ```

3. Verify environment variables:
   ```bash
   az container show --name badi-crawler --resource-group your-rg \
     --query containers[0].environmentVariables
   ```

### Storage account access denied

1. Verify connection string:
   ```bash
   az storage account show-connection-string --name your-storage --resource-group your-rg
   ```

2. Check permissions and create new access key if needed:
   ```bash
   az storage account keys list --name your-storage --resource-group your-rg
   ```

## Costs

Estimated monthly costs (US East region):
- **App Service (B1)**: ~$12
- **Storage Account**: ~$0.50
- **Container Instances (1 instance, 24/7)**: ~$100
- **Total**: ~$112/month

Use **auto-scaling** and **scheduled shutdowns** to reduce costs.

## Next Steps

1. **Monitor with Application Insights**
   ```bash
   az webapp config appsettings set \
     --resource-group your-rg \
     --name your-app \
     --settings APPINSIGHTS_INSTRUMENTATIONKEY=your-key
   ```

2. **Set up Alerts**
   - Crawler failures
   - Storage quota exceeded
   - High API error rates

3. **Implement Auto-Scaling**
   - Scale web app based on traffic
   - Use spot instances for crawler

4. **Enable HTTPS**
   - Already enabled by default on azurewebsites.net

## Support & Resources

- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure Blob Storage Guide](https://docs.microsoft.com/en-us/azure/storage/blobs/)
- [Bicep Documentation](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/)

## License

See LICENSE file for details

## Contributors

See CONTRIBUTORS.md

## FAQ

**Q: How often is data scraped?**
A: By default, every 1 hour. Change `SCRAPE_INTERVAL_SECONDS` to adjust.

**Q: Can I use a different database?**
A: Yes! Modify `src/azure_storage/repository.py` to use your preferred database.

**Q: Is the data publicly accessible?**
A: No, blob storage is private. The API provides a secure interface.

**Q: Can I run multiple crawlers?**
A: Yes! Deploy multiple container instances with the same connection string.

**Q: How do I update the code?**
A: Push to main branch. GitHub Actions will automatically build and deploy.
