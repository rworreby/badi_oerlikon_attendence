# Architecture Documentation

System design, WebSocket implementation, and architectural decisions.

## 📚 Documents in This Directory

- **ARCHITECTURE.md** - Overall system architecture and components
- **ARCHITECTURE_DECISION_SUMMARY.md** - Why we chose this design
- **WEBSOCKET_REDESIGN.md** - Evolution from scraping to WebSocket listening
- **WEBSOCKET_IMPLEMENTATION.md** - Technical details of WebSocket implementation
- **WEBSOCKET_SUMMARY.md** - Quick reference for WebSocket setup
- **WEBSOCKET_VISUAL_GUIDE.md** - Diagrams and visual representations

## 🎯 Quick Navigation

**Want to understand the system?**
→ Start with `ARCHITECTURE.md`

**Want to know why WebSocket?**
→ Read `ARCHITECTURE_DECISION_SUMMARY.md`

**Want implementation details?**
→ Dive into `WEBSOCKET_IMPLEMENTATION.md`

**Want a visual overview?**
→ Check `WEBSOCKET_VISUAL_GUIDE.md`

## 🔑 Key Concepts

### System Architecture
- CrowdMonitor WebSocket API as data source
- Azure Functions as serverless executor
- 5-minute collection windows
- Statistics aggregation and storage
- Timer-triggered every 5 minutes

### WebSocket Approach
- Replaces hourly scraping
- 720x more data points
- Collects real-time updates every 5 seconds
- Aggregates into 5-minute windows

### Data Flow
```
CrowdMonitor API
    ↓
WebSocket Listener (Azure Function)
    ↓
5-minute collection window
    ↓
Statistics calculation
    ↓
Blob Storage (JSON)
```

## 📖 Related Documents

- Deployment: See [../deployment/](../deployment/README.md)
- Technical details: See [../technical/](../technical/README.md)
- Quick start: See [../../QUICKSTART.md](../../QUICKSTART.md)

---

**Last Updated:** February 17, 2026
