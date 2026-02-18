# Technical Documentation

Technical implementation details, troubleshooting, and local development guides.

## 📚 Documents in This Directory

- **LOCAL*TESTING*GUIDE.md** - Set up and run locally with Docker Compose
- **LOCAL*TESTING*COMPLETE.md** - Local testing status and next steps
- **DOCKER*FIX*SUMMARY.md** - Docker Compose issues and fixes
- **TIMEOUT_CONSIDERATIONS.md** - Azure Functions timeout analysis
- **TIMEOUT*QUICK*REF.md** - Timeout constraints quick reference
- **CHANGES_MADE.md** - Summary of changes made to the project
- **FILES_CREATED.md** - List of all created files
- **DOCUMENTATION_REORGANIZATION.md** - Documentation organization history
- **REORGANIZATION_SUMMARY.md** - Reorganization summary and cleanup notes

## 🎯 Common Tasks

**Setting up locally?**
→ Read [LOCAL*TESTING*GUIDE.md](./LOCAL*TESTING*GUIDE.md)

**Docker not working?**
→ Check [DOCKER*FIX*SUMMARY.md](./DOCKER*FIX*SUMMARY.md)

**Worried about timeouts?**
→ See [TIMEOUT*QUICK*REF.md](./TIMEOUT*QUICK*REF.md)

**Want to understand changes?**
→ Read [CHANGES*MADE.md](./CHANGES*MADE.md)

**Need file list?**
→ Check [FILES*CREATED.md](./FILES*CREATED.md)

## 🔧 Local Development Setup

### Requirements
- Docker & Docker Compose
- Python 3.9+
- Ports: 7071, 10000-10002

### Quick Start

```bash
docker-compose -f docker-compose.functions.yml up
docker logs -f badi*oerlikon*attendence*functions*1

```text

## ⏱️ Timeout Information

Azure Functions Consumption Plan timeout: **10 minutes**
Our function execution: **~2-4 seconds** (with 5-minute collection window)
Safety buffer: **150-300x**

See [TIMEOUT*CONSIDERATIONS.md](./TIMEOUT*CONSIDERATIONS.md) for details.

## 📖 Related Documents

- Architecture: See [../architecture/](../architecture/README.md)
- Deployment: See [../deployment/](../deployment/README.md)
- Quick start: See [../../QUICKSTART.md](../../QUICKSTART.md)

---

**Last Updated:** February 17, 2026
