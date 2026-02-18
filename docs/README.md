# Documentation Index

Complete documentation organized by topic.

## 🚀 Quick Navigation

**New to the project?** Start here:
1. Read the main [README.md](../README.md)
2. Follow [QUICKSTART.md](../QUICKSTART.md) (5 minutes)
3. Deploy using [DEPLOYMENT_GUIDE_WEBSOCKET.md](../DEPLOYMENT_GUIDE_WEBSOCKET.md)

## 📂 Documentation Structure

### 🏗️ [architecture/](./architecture/)
System design, architecture decisions, and WebSocket implementation details.

**Key documents:**
- `ARCHITECTURE.md` - Overall system architecture
- `ARCHITECTURE_DECISION_SUMMARY.md` - Why we chose WebSocket listening
- `WEBSOCKET_REDESIGN.md` - Evolution from scraping to WebSocket
- `WEBSOCKET_IMPLEMENTATION.md` - Detailed WebSocket implementation
- `WEBSOCKET_SUMMARY.md` - Quick reference for WebSocket setup
- `WEBSOCKET_VISUAL_GUIDE.md` - Visual diagrams and flows

### 🚀 [deployment/](./deployment/)
Azure deployment guides, checklists, and infrastructure setup.

**Key documents:**
- `DEPLOYMENT_GUIDE_WEBSOCKET.md` - **Main deployment guide** (in parent dir)
- `AZURE_DEPLOYMENT.md` - Azure-specific setup details
- `AZURE_FUNCTIONS_GUIDE.md` - Functions configuration guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment verification
- `READY_TO_DEPLOY.md` - Final readiness check
- `GITHUB_SECRETS.md` - CI/CD secrets configuration

### 🔧 [technical/](./technical/)
Technical details, troubleshooting, local testing, and implementation notes.

**Key documents:**
- `LOCAL_TESTING_GUIDE.md` - Local Docker Compose setup
- `LOCAL_TESTING_COMPLETE.md` - Completion status & next steps
- `DOCKER_FIX_SUMMARY.md` - Docker Compose issues & fixes
- `TIMEOUT_CONSIDERATIONS.md` - Azure Functions timeout analysis
- `TIMEOUT_QUICK_REF.md` - Timeout quick reference
- `CHANGES_MADE.md` - Summary of all changes made
- `FILES_CREATED.md` - List of all created files

### 📜 [migration/](./migration/)
Migration history from local scrapers to Azure Functions with WebSocket.

**Key documents:**
- `MIGRATION_CONTAINER_TO_FUNCTIONS.md` - Container → Functions migration
- `MIGRATION_COMPLETE.md` - Migration completion report
- `CLEANUP_SUMMARY.md` - Cleanup & removed files
- `TRANSFORMATION_SUMMARY.md` - Complete transformation overview

## 🎯 Common Tasks

### I want to...

**Get started locally**
→ Read: [QUICKSTART.md](../QUICKSTART.md) → [technical/LOCAL_TESTING_GUIDE.md](./technical/LOCAL_TESTING_GUIDE.md)

**Deploy to Azure**
→ Read: [DEPLOYMENT_GUIDE_WEBSOCKET.md](../DEPLOYMENT_GUIDE_WEBSOCKET.md) → [deployment/DEPLOYMENT_CHECKLIST.md](./deployment/DEPLOYMENT_CHECKLIST.md)

**Understand the system**
→ Read: [README.md](../README.md) → [architecture/ARCHITECTURE.md](./architecture/ARCHITECTURE.md)

**Troubleshoot issues**
→ Read: [technical/LOCAL_TESTING_COMPLETE.md](./technical/LOCAL_TESTING_COMPLETE.md) → [technical/DOCKER_FIX_SUMMARY.md](./technical/DOCKER_FIX_SUMMARY.md)

**Learn about WebSocket implementation**
→ Read: [architecture/WEBSOCKET_SUMMARY.md](./architecture/WEBSOCKET_SUMMARY.md) → [architecture/WEBSOCKET_IMPLEMENTATION.md](./architecture/WEBSOCKET_IMPLEMENTATION.md)

**Understand timeout constraints**
→ Read: [technical/TIMEOUT_QUICK_REF.md](./technical/TIMEOUT_QUICK_REF.md) → [technical/TIMEOUT_CONSIDERATIONS.md](./technical/TIMEOUT_CONSIDERATIONS.md)

**See what changed recently**
→ Read: [technical/CHANGES_MADE.md](./technical/CHANGES_MADE.md) → [technical/FILES_CREATED.md](./technical/FILES_CREATED.md)

## 📊 Document Map

```
Root Level (Essential):
├── README.md .......................... Project overview & quick start
├── QUICKSTART.md ....................... 5-minute getting started guide
└── DEPLOYMENT_GUIDE_WEBSOCKET.md ....... Azure deployment instructions

docs/architecture/ (System Design):
├── ARCHITECTURE.md ..................... System overview
├── ARCHITECTURE_DECISION_SUMMARY.md .... Design decisions
├── WEBSOCKET_REDESIGN.md ............... Evolution process
├── WEBSOCKET_IMPLEMENTATION.md ......... Technical implementation
├── WEBSOCKET_SUMMARY.md ................ Quick reference
└── WEBSOCKET_VISUAL_GUIDE.md ........... Diagrams & flows

docs/deployment/ (Azure Setup):
├── AZURE_DEPLOYMENT.md ................. Azure configuration
├── AZURE_FUNCTIONS_GUIDE.md ............ Functions setup
├── DEPLOYMENT_CHECKLIST.md ............. Pre-deployment checks
├── READY_TO_DEPLOY.md .................. Final verification
└── GITHUB_SECRETS.md ................... CI/CD configuration

docs/technical/ (Implementation):
├── LOCAL_TESTING_GUIDE.md .............. Docker Compose setup
├── LOCAL_TESTING_COMPLETE.md ........... Status & next steps
├── DOCKER_FIX_SUMMARY.md ............... Issues & fixes
├── TIMEOUT_CONSIDERATIONS.md ........... Timeout analysis
├── TIMEOUT_QUICK_REF.md ................ Quick reference
├── CHANGES_MADE.md ..................... Change summary
└── FILES_CREATED.md .................... Created files list

docs/migration/ (History):
├── MIGRATION_CONTAINER_TO_FUNCTIONS.md  Container migration
├── MIGRATION_COMPLETE.md ............... Completion report
├── CLEANUP_SUMMARY.md .................. Cleanup actions
└── TRANSFORMATION_SUMMARY.md ........... Overall transformation
```

## 🔍 Key Sections Explained

### Architecture Documents
- **ARCHITECTURE.md**: Understand the overall system design
- **WEBSOCKET_IMPLEMENTATION.md**: Deep dive into how WebSocket listening works
- **ARCHITECTURE_DECISION_SUMMARY.md**: Why we chose this approach

### Deployment Documents
- **DEPLOYMENT_GUIDE_WEBSOCKET.md**: Step-by-step Azure deployment
- **DEPLOYMENT_CHECKLIST.md**: Verify everything before deployment
- **AZURE_FUNCTIONS_GUIDE.md**: Specific Functions configuration

### Technical Documents
- **LOCAL_TESTING_GUIDE.md**: Set up and run locally
- **TIMEOUT_CONSIDERATIONS.md**: Understand timeout constraints
- **CHANGES_MADE.md**: See what was recently changed

### Migration Documents
- **TRANSFORMATION_SUMMARY.md**: Complete overview of all changes
- **MIGRATION_CONTAINER_TO_FUNCTIONS.md**: Why we migrated to Functions
- **CLEANUP_SUMMARY.md**: What was removed

## 💡 Pro Tips

1. **Start with the overview** - Read README.md first
2. **Follow the deployment guide** - Use DEPLOYMENT_GUIDE_WEBSOCKET.md step-by-step
3. **Check the checklist** - Use deployment/DEPLOYMENT_CHECKLIST.md before going live
4. **Reference the architecture** - Understand the system before modifying it
5. **Use search** - Most important info is cross-referenced

## 📝 Version Info

- **Project**: BADI Oerlikon Occupancy Monitor
- **Type**: WebSocket Listener + Azure Functions
- **Last Updated**: February 17, 2026
- **Status**: ✅ Ready for Production

---

**Need help?** Start with the main [README.md](../README.md)
