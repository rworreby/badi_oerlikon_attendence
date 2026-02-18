# WebSocket Architecture - Final Design

## Key Facts Confirmed

✅ **WebSocket exists** that publishes BADI Oerlikon attendance data
✅ **Updates every 5 seconds** (high frequency)
✅ **WebSocket is the smartest approach** (most efficient)
⚠️ **GET request/scraping also possible** (but less efficient)

---

## Why WebSocket is Best

| Method | Latency | Efficiency | CPU | Best For |
|--------|---------|-----------|-----|----------|
| **WebSocket** | Real-time (~5s) | ✅ Best | Low | Always |
| **GET polling** | Variable (1-10s) | Medium | Medium | Fallback |
| **HTML scraping** | Slow (10-30s) | Poor | High | Last resort |

**Decision:** Use WebSocket as primary ✅

---

## Proposed Solution

### High-Level Flow

```text

Timer: Every 5 minutes
  ├─ Start Azure Function
  ├─ Connect to WebSocket
  ├─ Listen for exactly 5 minutes
  │  └─ Collect one update every 5 seconds (60 updates expected)
  ├─ Store all 60 occupancy readings + timestamps
  ├─ Calculate 5-min window statistics
  ├─ Save aggregated data to blob
  └─ Exit function

Next cycle starts 5 minutes later

```text

### Data You'll Capture Per Window

```text

5-minute window: 10:00 - 10:05
├─ Update 1: 10:00:00 → occupancy: 45
├─ Update 2: 10:00:05 → occupancy: 45
├─ Update 3: 10:00:10 → occupancy: 46
├─ Update 4: 10:00:15 → occupancy: 46
├─ Update 5: 10:00:20 → occupancy: 45
├─ Update 6: 10:00:25 → occupancy: 47
├─ Update 7: 10:00:30 → occupancy: 47
├─ Update 8: 10:00:35 → occupancy: 48
├─ Update 9: 10:00:40 → occupancy: 48
├─ Update 10: 10:00:45 → occupancy: 49
├─ Update 11: 10:00:50 → occupancy: 49
├─ Update 12: 10:00:55 → occupancy: 50
├─ Update 13: 10:01:00 → occupancy: 50
├─ ... (47 more updates)
└─ Update 60: 10:04:55 → occupancy: 52

Statistics:
├─ Count: 60 updates
├─ Min: 45
├─ Max: 52
├─ Average: 48.3
├─ Trend: Steady increase
└─ Duration: Exactly 5 min

```text

### Implementation Architecture

```text

src/functions/
├── websocket_listener/                    ← NEW
│   ├── **init**.py                        (Main handler)
│   ├── function.json                      (Timer config: every 5 min)
│   ├── websocket_handler.py               (WebSocket logic)
│   ├── requirements.txt                   (Dependencies)
│   └── local.settings.json                (Local testing)
│
├── crawler_timer/                         ← OLD (can be deprecated)
│   └── ... (keep for now or delete)
│
└── shared_utils.py                        (Optional: shared code)

```text

---

## Code Implementation

### 1. Main Function Handler

```python

# src/functions/websocket_listener/**init**.py

import azure.functions as func
import asyncio
import json
import logging
import os
from datetime import datetime
from .websocket_handler import WebSocketListener
from azure_storage.repository import AzureBlobRepository


async def main(mytimer: func.TimerRequest) -> None:
    """
    Azure Function: Listen to BADI Oerlikon WebSocket for 5 minutes.

    Timer: Runs every 5 minutes (cron: */5 * * * * *)
    Expected: ~60 updates per window (one every 5 seconds)

    Args:
        mytimer: Timer trigger
    """
    logger = logging.getLogger("websocket_listener")

    if mytimer.past_due:
        logger.warning("Timer is past due")

    window_start = datetime.utcnow()
    logger.info(f"WebSocket listener started at {window_start}")

    try:
        # Get configuration

        websocket_url = os.getenv(
            'WEBSOCKET_URL',
            'wss://your-websocket-endpoint'  # Set in Azure Function settings

        )
        connection*string = os.getenv('AZURE*STORAGE*CONNECTION*STRING')

        # Listen to WebSocket for exactly 5 minutes

        listener = WebSocketListener(url=websocket*url, duration*seconds=300)
        updates = await listener.collect_updates()

        logger.info(f"Collected {len(updates)} updates in 5-minute window")

        if updates:
            # Calculate statistics

            occupancies = [u['occupancy'] for u in updates]
            stats = {
                'count': len(updates),
                'min': min(occupancies),
                'max': max(occupancies),
                'avg': sum(occupancies) / len(occupancies),
                'median': sorted(occupancies)[len(occupancies) // 2]
            }

            # Save to blob storage

            window_end = datetime.utcnow()
            repo = AzureBlobRepository(connection_string)

            data = {
                'window': {
                    'start': window_start.isoformat(),
                    'end': window_end.isoformat(),
                    'duration_seconds': 300
                },
                'updates': updates,
                'statistics': stats
            }

            blob*name = repo.save*data(data)
            logger.info(f"Saved data to blob: {blob_name}")
            logger.info(f"Stats: min={stats['min']}, max={stats['max']}, avg={stats['avg']:.1f}")
        else:
            logger.warning("No updates received in 5-minute window")

    except Exception as e:
        logger.error(f"Error in websocket listener: {e}", exc_info=True)
        raise

```text

### 2. WebSocket Handler

```python

# src/functions/websocket*listener/websocket*handler.py

import asyncio
import json
import logging
from datetime import datetime
import websockets


class WebSocketListener:
    """Connects to WebSocket and collects occupancy updates."""

    def **init**(self, url, duration*seconds=300, timeout*per_message=1.0):
        """
        Initialize WebSocket listener.

        Args:
            url: WebSocket URL (e.g., wss://api.example.com/occupancy)
            duration_seconds: How long to listen (default 5 min)
            timeout*per*message: Max wait for each message (default 1 sec)
        """
        self.url = url
        self.duration*seconds = duration*seconds
        self.timeout*per*message = timeout*per*message
        self.logger = logging.getLogger(**name**)

    async def collect_updates(self):
        """
        Connect to WebSocket and collect updates for duration.

        Returns:
            List of {'occupancy': int, 'timestamp': str} dicts
        """
        updates = []
        start_time = datetime.utcnow()

        try:
            async with websockets.connect(self.url) as websocket:
                self.logger.info(f"Connected to WebSocket: {self.url}")

                while True:
                    elapsed = (datetime.utcnow() - start*time).total*seconds()

                    if elapsed >= self.duration_seconds:
                        self.logger.info(f"5-minute window complete. Collected {len(updates)} updates.")
                        break

                    try:
                        # Wait for next message (with timeout)

                        message = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=self.timeout*per*message
                        )

                        # Parse message

                        data = self.*parse*message(message)

                        if data:
                            updates.append(data)
                            self.logger.debug(
                                f"Update {len(updates)}: occupancy={data['occupancy']} "
                                f"at {data['timestamp']}"
                            )

                    except asyncio.TimeoutError:
                        # No message in 1 second, keep listening

                        continue

                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to parse message: {message[:100]}")
                        continue

                    except Exception as e:
                        self.logger.warning(f"Error processing message: {e}")
                        continue

        except asyncio.TimeoutError:
            self.logger.error("WebSocket connection timeout")
            raise
        except ConnectionRefusedError:
            self.logger.error(f"Failed to connect to {self.url}")
            raise
        except Exception as e:
            self.logger.error(f"WebSocket error: {e}")
            raise

        return updates

    def *parse*message(self, message):
        """
        Parse WebSocket message and extract occupancy.

        Expected message format (adjust based on actual API):
        {
            "anzahl_gaeste": 45,
            "timestamp": "2026-02-17T10:00:05Z",
            "last_updated": "2026-02-17T10:00:05Z"
        }

        Args:
            message: Raw WebSocket message (JSON string)

        Returns:
            {'occupancy': int, 'timestamp': str} or None if invalid
        """
        try:
            data = json.loads(message)

            # Extract occupancy (adjust field name as needed)

            occupancy = data.get('anzahl_gaeste') or data.get('occupancy')

            if occupancy is None:
                self.logger.warning(f"No occupancy field in message: {data}")
                return None

            return {
                'occupancy': int(occupancy),
                'timestamp': datetime.utcnow().isoformat()
            }

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            self.logger.warning(f"Error parsing message: {e}")
            return None

```text

### 3. Timer Configuration

```json
// src/functions/websocket_listener/function.json

{
  "scriptFile": "**init**.py",
  "bindings": [
    {
      "name": "mytimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "*/5 * * * * *"
    }
  ]
}

```text

### Cron Schedule Breakdown

```text

*/5 * * * * *
│   │ │ │ │ │
│   │ │ │ │ Day of week (0-6, Sunday=0)
│   │ │ │ Month (1-12)
│   │ │ Day of month (1-31)
│   │ Hour (0-23)
│   Minute (0-59)
Second (0-59)

*/5 = Every 5 seconds

```text

Wait, that's wrong for 5 minutes. Should be:

```json
{
  "schedule": "0 */5 * * * *"
}

```text

### Correct explanation

```text

0 */5 * * * *
│ │   │ │ │ │
│ │   │ │ │ Day of week
│ │   │ │ Month
│ │   │ Day of month
│ │   Hour
│ Minute (*/5 = every 5 minutes)
Second (0 = at :00 second)

```text

### 4. Requirements

```txt

# src/functions/websocket_listener/requirements.txt

azure-functions==1.13.0
websockets==11.0.3
azure-storage-blob==12.18.0
azure-identity==1.14.0
python-dotenv==1.0.0

```text

### 5. Local Testing Configuration

```json
// src/functions/local.settings.json

{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS*WORKER*RUNTIME": "python",
    "WEBSOCKET_URL": "wss://your-websocket-endpoint",
    "AZURE*STORAGE*CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=..."
  },
  "Host": {
    "LocalHttpPort": 7071,
    "CORS": "*"
  }
}

```text

---

## Deployment Steps

### Step 1: Update Bicep (if needed)

Add environment variable to Function App:

```bicep
resource functionApp 'Microsoft.Web/sites@2021-02-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'

  properties: {
    siteConfig: {
      appSettings: [
        {
          name: 'WEBSOCKET_URL'
          value: 'wss://api.badi-oerlikon.example.com/occupancy'
        }
        // ... other settings
      ]
    }
  }
}

```text

### Step 2: Test Locally

```bash

# With Docker and Azurite

docker-compose -f docker-compose.functions.yml up

# In another terminal

cd src/functions/websocket_listener
func start

```text

### Step 3: Deploy to Azure

```bash
cd src/functions/websocket_listener

# Package

mkdir -p build
cp -r . build/
cd build && zip -r ../websocket-listener.zip . && cd ..

# Deploy

az functionapp deployment source config-zip \
  --resource-group badi-oerlikon-rg \
  --name badi-oerlikon-dev-func \
  --src websocket-listener.zip

```text

### Step 4: Verify

```bash

# View logs

az functionapp log tail \
  --resource-group badi-oerlikon-rg \
  --name badi-oerlikon-dev-func

# Expected output:

# [2026-02-17T10:00:05Z] Connected to WebSocket: wss://

# [2026-02-17T10:00:10Z] Update 1: occupancy=45

# [2026-02-17T10:00:15Z] Update 2: occupancy=45

# 

# [2026-02-17T10:05:00Z] 5-minute window complete. Collected 60 updates

# [2026-02-17T10:05:02Z] Saved data to blob: 2026-02-17/10-00-to-10-05.json

```text

---

## Data Storage Example

Each 5-minute window creates one blob file:

```json
{
  "window": {
    "start": "2026-02-17T10:00:00Z",
    "end": "2026-02-17T10:05:02Z",
    "duration_seconds": 300
  },
  "updates": [
    {"occupancy": 45, "timestamp": "2026-02-17T10:00:00Z"},
    {"occupancy": 45, "timestamp": "2026-02-17T10:00:05Z"},
    {"occupancy": 46, "timestamp": "2026-02-17T10:00:10Z"},
    {"occupancy": 46, "timestamp": "2026-02-17T10:00:15Z"},
    {"occupancy": 45, "timestamp": "2026-02-17T10:00:20Z"},
    ... (55 more updates) ...
    {"occupancy": 52, "timestamp": "2026-02-17T10:04:55Z"}
  ],
  "statistics": {
    "count": 60,
    "min": 45,
    "max": 52,
    "avg": 48.3,
    "median": 48
  }
}

```text

### Blob naming

```text

scraped-data/
├── 2026-02-17/
│   ├── 10-00-to-10-05.json
│   ├── 10-05-to-10-10.json
│   ├── 10-10-to-10-15.json
│   └── ... (288 files per day)
└── 2026-02-18/
    └── ...

```text

---

## Cost Breakdown

```text

Per day:
├─ 288 function invocations = negligible cost
├─ 288 × 300 seconds = 86,400 seconds total
│  └─ But only ~5-10 seconds CPU per function (WebSocket is async)
│  └─ 288 × 7 seconds = ~2,000 seconds CPU per day
│  └─ Cost: 2,000s × $0.000016/s = $0.032
├─ Storage: ~60-100 KB per day = negligible
└─ Total: ~$0.032/day

Per month: ~$0.96/month
Plus: Web App ($12) + Blob Storage ($1) = ~$14/month total

Much better than hourly scraping for 100x more data!

```text

---

## Fallback Strategy

If WebSocket fails:

```python

# Fallback to GET request (simple scraping)

async def fallback*get*request():
    """Fallback: Single GET request instead of WebSocket."""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://api.badi-oerlikon.example.com/current-occupancy',
            timeout=10
        ) as resp:
            data = await resp.json()
            return data['anzahl_gaeste']

# In main function:

try:
    updates = await listener.collect_updates()
except Exception as e:
    logger.warning(f"WebSocket failed, falling back to GET: {e}")
    occupancy = await fallback*get*request()
    updates = [{'occupancy': occupancy, 'timestamp': datetime.utcnow().isoformat()}]

```text

---

## Next Steps

### Questions I need answered

1. **WebSocket URL:** What's the exact endpoint? (e.g., `wss://api.example.com/occupancy`)

2. **Message format:** What does each update look like? (e.g., JSON structure)

3. **Authentication:** Does the WebSocket require authentication? (headers, tokens, etc.)

Once you provide these, I can:
- ✅ Finalize the implementation
- ✅ Test locally with real WebSocket data
- ✅ Deploy to Azure
- ✅ Monitor for data accuracy

**Would you like me to proceed with implementing this?**
