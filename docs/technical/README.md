# Technical Documentation

Technical implementation details, troubleshooting, and local development guides.

## 📚 Documents in This Directory

- **LOCAL_TESTING_GUIDE.md** - Set up and run locally with Docker Compose
- **LOCAL_TESTING_COMPLETE.md** - Local testing status and next steps
- **DOCKER_FIX_SUMMARY.md** - Docker Compose issues and fixes
- **TIMEOUT_CONSIDERATIONS.md** - Azure Functions timeout analysis
- **TIMEOUT_QUICK_REF.md** - Timeout constraints quick reference
- **CHANGES_MADE.md** - Summary of changes made to the project
- **FILES_CREATED.md** - List of all created files
- **DOCUMENTATION_REORGANIZATION.md** - Documentation organization history
- **REORGANIZATION_SUMMARY.md** - Reorganization summary and cleanup notes

## 🎯 Common Tasks

**Setting up locally?**
→ Read [LOCAL_TESTING_GUIDE.md](./LOCAL_TESTING_GUIDE.md)

**Docker not working?**
→ Check [DOCKER_FIX_SUMMARY.md](./DOCKER_FIX_SUMMARY.md)

**Worried about timeouts?**
→ See [TIMEOUT_QUICK_REF.md](./TIMEOUT_QUICK_REF.md)

**Want to understand changes?**
→ Read [CHANGES_MADE.md](./CHANGES_MADE.md)

**Need file list?**
→ Check [FILES_CREATED.md](./FILES_CREATED.md)

## 🔧 Local Development Setup

**Requirements:**
- Docker & Docker Compose
- Python 3.9+
- Ports: 7071, 10000-10002

**Quick Start:**
```bash
docker-compose -f docker-compose.functions.yml up
docker logs -f badi_oerlikon_attendence_functions_1
```

## ⏱️ Timeout Information

Azure Functions Consumption Plan timeout: **10 minutes**
Our function execution: **~2-4 seconds** (with 5-minute collection window)
Safety buffer: **150-300x**

See [TIMEOUT_CONSIDERATIONS.md](./TIMEOUT_CONSIDERATIONS.md) for details.

## 📖 Related Documents

- Architecture: See [../architecture/](../architecture/README.md)
- Deployment: See [../deployment/](../deployment/README.md)
- Quick start: See [../../QUICKSTART.md](../../QUICKSTART.md)

---

**Last Updated:** February 17, 2026
