# Migration Documentation

Historical migration records from local scrapers to Azure Functions with WebSocket.

## 📚 Documents in This Directory

- **MIGRATION*CONTAINER*TO_FUNCTIONS.md** - Migration from Container Instance to Azure Functions
- **MIGRATION_COMPLETE.md** - Migration completion report
- **CLEANUP_SUMMARY.md** - Cleanup actions and removed files
- **TRANSFORMATION_SUMMARY.md** - Complete transformation overview

## 📜 Migration Timeline

**Phase 1: Local Scraper**
- Initial HTML scraping setup
- Local database storage

**Phase 2: Azure Container Instance**
- Moved to cloud
- Used Container Instance for continuous running
- Cost: ~$113/month

**Phase 3: Azure Functions**
- Migrated to serverless Functions
- Consumption Plan pricing
- Cost reduced to ~$15/month (85% savings)

**Phase 4: WebSocket Redesign**
- Recognized mismatch between scraping (hourly) and data (every 5 sec)
- Implemented WebSocket listening
- 720x more data points with minimal cost increase

## 🎯 Key Changes

### Migration Benefits
- Cost reduction: 85% ($98/month saved)
- Data improvement: 720x more readings
- Reliability: Serverless auto-scaling
- Maintenance: No infrastructure to manage

### Architecture Evolution
- Hourly scraping → 5-second WebSocket updates
- 1 data point/hour → 12,000+ data points/day
- Manual triggering → Automatic timer-based

## 📖 Related Documents

- Architecture: See [../architecture/](../architecture/README.md)
- Deployment: See [../deployment/](../deployment/README.md)
- Technical: See [../technical/](../technical/README.md)

## 💡 Why WebSocket

Traditional scraping (hourly):
- ~24 data points per day
- Misses intermediate changes
- Inefficient

WebSocket listening (5-minute windows):
- ~17,280 data points per day (every 5 minutes)
- Captures all changes (every 5 seconds)
- Cost-effective with Functions

---

**Last Updated:** February 17, 2026
**Status:** ✅ Migration Complete
