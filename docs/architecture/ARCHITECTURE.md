# Architecture Overview

## System Components

### 1. Frontend Web App (Azure App Service)

- **Technology**: Flask + HTML5/CSS3/JavaScript
- **Purpose**: Display real-time pool occupancy data
- **Features**:
  - Real-time dashboard with auto-refresh
  - Historical data browser
  - Responsive design for mobile/desktop
  - REST API for data retrieval

### 2. Azure Blob Storage

- **Purpose**: Persistent storage for scraped data
- **Containers**:
  - `scraped-data`: JSON files with pool data
  - `logs`: Application and crawler logs
- **Data Format**: JSON with timestamp metadata
- **Access**: Via Python SDK with connection string or managed identity

### 3. Continuous Crawler Service (Azure Container Instances)

- **Technology**: Python, Docker, Azure Container Instances
- **Purpose**: Periodically scrape pool data
- **Features**:
  - Configurable scrape interval (default 1 hour)
  - Automatic retry on failure
  - Logs to blob storage
  - Graceful error handling

### 4. Container Registry (Azure Container Registry)

- **Purpose**: Store and manage Docker images
- **Images**:
  - `badi-webapp:latest` - Web app image
  - `badi-crawler:latest` - Crawler image
- **CI/CD**: GitHub Actions automatically builds and pushes new images

## Data Flow

```text

Web Browser
    ↓
    ├─→ GET / → [Web App] → Serves index.html
    │
    └─→ GET /api/data/* → [Web App API]
                              ↓
                         [Python Code]
                              ↓
                    [Azure Blob Storage]
                              ↓
                         Returns JSON
                              ↓
                    [JavaScript Charts]

Scheduled Event
    ↓
[GitHub Actions Timer] (or Azure Logic Apps)
    ↓
[Trigger] → [Container Instance] → [Crawler Service]
                                         ↓
                                  [fetch_data]
                                         ↓
                                  [parse_html]
                                         ↓
                                  [save to blob]
                                         ↓
                              [Azure Blob Storage]

```text

## Deployment Topology

```text

┌──────────────────────────────────────────────────────────────┐
│                    Azure Resource Group                        │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐         ┌──────────────────────┐   │
│  │   App Service Plan  │         │ Container Registry   │   │
│  ├─────────────────────┤         ├──────────────────────┤   │
│  │                     │         │                      │   │
│  │  ┌─────────────┐    │         │ badi-webapp:latest   │   │
│  │  │   Web App   │────┼────────▶│ badi-crawler:latest  │   │
│  │  │ (Linux, B1) │    │         │                      │   │
│  │  └─────────────┘    │         └──────────────────────┘   │
│  │      :5000          │                                      │
│  │                     │                                      │
│  └─────────────────────┘                                      │
│           │                                                    │
│           │                                                    │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │         Azure Storage Account (StorageV2)             │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  Blob Service                                          │  │
│  │  ├── scraped-data (container)                         │  │
│  │  │   ├── scraped*data*2024-01-15_14-30-00.json       │  │
│  │  │   ├── scraped*data*2024-01-15_13-30-00.json       │  │
│  │  │   └── ...                                          │  │
│  │  └── logs (container)                                │  │
│  │      └── crawler_2024-01-15.log                       │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│           ▲                                                    │
│           │                                                    │
│  ┌────────┴──────────────────────────────────────────────┐  │
│  │  Container Instance (Crawler Service)                 │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  • Runs 24/7 with restart policy                      │  │
│  │  • Scrapes every 1 hour                               │  │
│  │  • Stores data to blob storage                        │  │
│  │  • Handles errors gracefully                          │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
└──────────────────────────────────────────────────────────────┘

External:
┌──────────────────────┐
│  GitHub Repository   │
├──────────────────────┤
│  • Source code       │
│  • GitHub Actions    │
│  • CI/CD automation  │
└──────────────────────┘
     ↓ (on push to main)
┌──────────────────────┐
│  Build & Push Images │
└──────────────────────┘
     ↓
[Azure Container Registry]

```text

## Key Integration Points

### 1. Web App ↔ Blob Storage

- **Authentication**: Connection string or Managed Identity
- **Operations**: Read JSON files, list blobs
- **Framework**: azure-storage-blob Python SDK

### 2. Crawler ↔ Blob Storage

- **Authentication**: Connection string or Managed Identity
- **Operations**: Write JSON files, read for validation
- **Framework**: azure-storage-blob Python SDK

### 3. GitHub ↔ Azure Container Registry

- **Authentication**: Service Principal with AcrPush role
- **Operations**: Build images, push to registry
- **Framework**: GitHub Actions + Azure CLI

### 4. Azure Container Registry ↔ App Service

- **Authentication**: Managed connection via deployment
- **Operations**: Pull and run container image
- **Update**: Manual or automated via CI/CD

## Security Architecture

```text

                    Internet
                       ↓
        ┌──────────────────────────┐
        │   Azure Front Door (CDN) │ ← Optional: DDoS protection
        └──────────────┬───────────┘
                       ↓
        ┌──────────────────────────┐
        │    HTTPS (TLS 1.2+)      │ ← Built-in with *.azurewebsites.net
        └──────────────┬───────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │   Network Security Group (NSG)       │ ← Optional firewall rules
        ├──────────────────────────────────────┤
        │   Allow: HTTPS (443)                 │
        │   Block: Everything else             │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │    App Service Environment           │
        ├──────────────────────────────────────┤
        │   Private App Service Endpoints      │ ← Optional
        │   (restricts access to VNet)         │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │   Application Authentication         │
        ├──────────────────────────────────────┤
        │   • Connection strings managed       │
        │   • No hardcoded credentials         │
        │   • Environment variables per env    │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │   Azure Storage Authentication       │
        ├──────────────────────────────────────┤
        │   • Managed Identity (preferred)     │
        │   • Connection string (backup)       │
        │   • Private endpoints (optional)     │
        └──────────────────────────────────────┘

```text

## Cost Optimization Strategies

### 1. Compute

- Use **B1 App Service Plan** for development ($12/month)
- Scale up to **B2+** only during peak load
- Use **Azure Container Instances - spot pricing** for crawler ($30-50/month vs $100)
- Implement **scale-to-zero** for non-critical crawlers

### 2. Storage

- Use **Blob Storage lifecycle policies** to archive old data
- Move historical data to **Cool tier** after 30 days
- Implement **data retention policies** (delete after 1 year)

### 3. Bandwidth

- Use **Azure CDN** for static assets
- Enable **compression** in App Service
- Minimize API response sizes

### 4. Development

- Use **Azurite** for local storage emulation (free)
- Leverage **GitHub free tier** for CI/CD
- Use **free tier databases** during development

## Scaling Architecture

### Current (Small Scale)

- **Concurrent Users**: 10-50
- **Scrape Frequency**: 1/hour
- **Storage**: < 10 GB

### Medium Scale

```text

Add:
- Azure Traffic Manager for load balancing
- Auto-scale App Service (2-5 instances)
- Azure Database for structured queries
- Azure CDN for static assets
- Application Insights for monitoring

```text

### Enterprise Scale

```text

Add:
- Azure Front Door (global distribution)
- API Management for versioning
- Event Grid for event-driven architecture
- Service Bus for async processing
- Azure DevOps for advanced CI/CD
- Policy enforcement via Azure Policy

```text

## Disaster Recovery

### Backup Strategy

1. **Blob Storage**: Geographically redundant (GRS) enabled

2. **Configuration**: Infrastructure as Code (Bicep) version controlled

3. **Code**: Git repository with branching strategy

### Recovery RTO/RPO

- **RTO (Recovery Time Objective)**: 1 hour
  - Redeploy infrastructure from Bicep
  - Redeploy containers from registry
- **RPO (Recovery Point Objective)**: 1 hour
  - Blob storage GRS replication
  - Last hourly crawl data

### Failover Procedure

```bash

# 1. Switch to secondary region

az config set defaults.group=<secondary-rg>

# 2. Redeploy infrastructure

./azure/deploy.sh

# 3. Restore data from geo-redundant storage

az storage account show-connection-string \
  --account-name <storage-account> \
  --resource-group <secondary-rg>

# 4. Deploy containers and restart services

# (same as initial deployment)

```text

## Monitoring & Observability

### Key Metrics

- **Web App**: Response time, error rate, CPU, memory
- **Crawler**: Scrape success rate, duration, frequency
- **Storage**: Read/write latency, capacity used
- **Blobs**: Most recent update timestamp

### Logging

- **Application**: Flask logs to stdout → App Service → Log Analytics
- **Crawler**: Python logging to blob storage + stdout
- **Infrastructure**: Azure Activity Log → Log Analytics

### Alerting

- Crawler hasn't run in 2 hours
- API error rate > 5%
- Storage capacity > 80%
- Response time > 5 seconds (p95)

## Configuration Management

### Environment Variables

Managed via:

1. **Local Development**: `.env` file

2. **Docker**: `Dockerfile` ENV directives

3. **App Service**: Configuration → Application settings

4. **Container Instance**: Environment variables in deployment

### Secrets

- **Local**: `.env` file (NOT committed)
- **Azure**: Azure Key Vault (optional)
- **CI/CD**: GitHub Secrets

## Code Organization

```text

src/
├── api/                    # Flask REST API

│   ├── app.py             # Flask application

│   └── static/            # Frontend assets

├── azure_storage/         # Azure integration

│   ├── blob_adapter.py    # Low-level blob operations

│   └── repository.py      # Business logic layer

├── services/              # Application services

│   └── crawler_service.py # Crawling logic

├── scraper/               # Web scraping

│   ├── fetcher.py        # HTTP requests

│   └── parser.py         # HTML parsing

├── db/                    # Database models (legacy)

├── utils/                 # Utilities

└── tests/                 # Unit tests

```text

## Future Enhancements

1. **Real-time Updates**: WebSocket for live data

2. **Notifications**: Email/SMS alerts for availability

3. **Analytics**: Occupancy trends, peak hours analysis

4. **Mobile App**: Native iOS/Android apps

5. **Multi-pool Support**: Track multiple facilities

6. **User Accounts**: Personalized preferences, bookmarks

7. **Predictions**: ML-based occupancy predictions

8. **Integration**: Calendar integration, facility booking
