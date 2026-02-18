# Local Testing Guide - WebSocket Listener

**Status:** ✅ Docker-compose file fixed and ready

---

## Quick Start (Local Testing)

### 1. Start Docker Containers

```bash
# From project root
docker-compose -f docker-compose.functions.yml up
```

**Expected output:**
```
azurite_1    | Azurite Blob service successfully listening at http://0.0.0.0:10000
functions_1  | Azure Functions Core Tools Version
```

### 2. Start Function in Another Terminal

```bash
# In another terminal, from project root
cd src/functions/websocket_listener
func start
```

**Expected output:**
```
Azure Functions Core Tools Version
...
Now listening on: 127.0.0.1:7071
Http Functions:
    websocket_listener: [TimerTrigger] (Disabled - runs on schedule)

For detailed output, run func with --verbose flag.
```

### 3. Manually Trigger the Function (Optional)

```bash
# In a third terminal
curl -X POST http://127.0.0.1:7071/admin/functions/websocket_listener \
  -H "Content-Type: application/json" \
  -d '{}'
```

Or wait for the automatic trigger (every 5 minutes).

---

## What to Expect

### Success Indicators

**In the functions terminal, you should see:**

```
2026-02-17T23:00:00.000 [Information] WebSocket listener started at 2026-02-17T23:00:00.000000+00:00
2026-02-17T23:00:01.000 [Information] Connecting to: wss://badi-public.crowdmonitor.ch:9591/api, monitoring UID: SSD-7
2026-02-17T23:00:02.000 [Information] Connected to WebSocket: wss://badi-public.crowdmonitor.ch:9591/api
2026-02-17T23:00:02.500 [Information] Sent 'all' command to WebSocket
2026-02-17T23:00:03.000 [Debug] Update 1: occupancy=45
2026-02-17T23:00:08.000 [Debug] Update 2: occupancy=45
2026-02-17T23:00:13.000 [Debug] Update 3: occupancy=46
...
2026-02-17T23:05:00.000 [Information] 5-minute window complete. Collected 60 updates.
2026-02-17T23:05:01.000 [Information] Saved data to blob: 2026-02-17/23-00-to-23-05.json
2026-02-17T23:05:02.000 [Information] Stats: count=60, min=45, max=52, avg=48.3
```

### Troubleshooting

**No connection to WebSocket:**
```
Check firewall rules - port 9591 should be accessible
Test: curl -I https://badi-public.crowdmonitor.ch
```

**Function not triggering:**
```
Timer triggers don't run while function is in development mode
Manually trigger with: curl -X POST http://127.0.0.1:7071/admin/functions/websocket_listener
```

**Azurite not starting:**
```
docker-compose down
docker-compose -f docker-compose.functions.yml up --build
```

---

## Stopping

```bash
# In the docker-compose terminal
Ctrl+C

# In the functions terminal
Ctrl+C

# Clean up (if needed)
docker-compose -f docker-compose.functions.yml down
```

---

## Docker-Compose File Changes

**Fixed issues:**
- ✅ Version changed from 3.8 to 3.3 (compatibility)
- ✅ Environment format updated (key: value instead of key=value)
- ✅ Removed healthcheck (sometimes causes issues locally)
- ✅ Simplified dependencies
- ✅ Added WebSocket configuration

---

## Testing Checklist

After running locally:

- [ ] Docker containers start successfully
- [ ] Functions runtime starts on localhost:7071
- [ ] No errors in either terminal
- [ ] WebSocket connection succeeds (see connection log)
- [ ] Occupancy updates appearing in logs
- [ ] Data saved to blob storage (check local)

---

## Next: Deploy to Azure

Once local testing succeeds:

```bash
# Follow DEPLOYMENT_GUIDE_WEBSOCKET.md
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `docker: command not found` | Install Docker Desktop |
| `compose file version unsupported` | File has been fixed ✅ |
| `port 7071 already in use` | Kill existing process or use different port |
| `WebSocket connection timeout` | Check internet, firewall, or crowdmonitor API status |
| `No occupancy data` | Verify SSD-7 UID is correct in environment |

---

## Full Workflow

```
Step 1: docker-compose up                (Start services)
         ↓
Step 2: func start                        (Start functions)
         ↓
Step 3: Monitor logs                      (Watch terminal)
         ↓
Step 4: Verify data flow                  (Check messages)
         ↓
Step 5: Stop (Ctrl+C)                     (Clean shutdown)
         ↓
Step 6: Deploy to Azure                   (Go live)
```

Ready to test? Run:
```bash
docker-compose -f docker-compose.functions.yml up
```
