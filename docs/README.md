# Documentation Index

Complete documentation organized by topic.

## 🚀 Quick Navigation

**New to the project?** Start here:

1. Read the main [README.md](../README.md)

2. Follow [QUICKSTART.md](../QUICKSTART.md) (5 minutes)

3. Deploy using [deployment/DEPLOYMENT*GUIDE*WEBSOCKET.md](./deployment/DEPLOYMENT*GUIDE*WEBSOCKET.md)

## 📂 Documentation Structure

### 🏗️ [architecture/](./architecture/)

System design, architecture decisions, and WebSocket implementation details.

### Key documents
- `ARCHITECTURE.md` - Overall system architecture
- `ARCHITECTURE*DECISION*SUMMARY.md` - Why we chose WebSocket listening
- `WEBSOCKET_REDESIGN.md` - Evolution from scraping to WebSocket
- `WEBSOCKET_IMPLEMENTATION.md` - Detailed WebSocket implementation
- `WEBSOCKET_SUMMARY.md` - Quick reference for WebSocket setup
- `WEBSOCKET*VISUAL*GUIDE.md` - Visual diagrams and flows

### 🚀 [deployment/](./deployment/)

Azure deployment guides, checklists, and infrastructure setup.

### Key documents
- `DEPLOYMENT*GUIDE*WEBSOCKET.md` - **Main deployment guide**
- `AZURE*INSTALLATION*SUMMARY.md` - Azure tool setup summary
- `AZURE*SETUP*COMPLETE.md` - Quick reference for setup
- `AZURE*TOOLS*SETUP.md` - Detailed tool installation
- `AZURE_DEPLOYMENT.md` - Azure-specific setup details
- `AZURE*FUNCTIONS*GUIDE.md` - Functions configuration guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment verification
- `READY*TO*DEPLOY.md` - Final readiness check
- `GITHUB_SECRETS.md` - CI/CD secrets configuration

### 🔧 [technical/](./technical/)

Technical details, troubleshooting, local testing, and implementation notes.

### Key documents
- `LOCAL*TESTING*GUIDE.md` - Local Docker Compose setup
- `LOCAL*TESTING*COMPLETE.md` - Completion status & next steps
- `DOCKER*FIX*SUMMARY.md` - Docker Compose issues & fixes
- `TIMEOUT_CONSIDERATIONS.md` - Azure Functions timeout analysis
- `TIMEOUT*QUICK*REF.md` - Timeout quick reference
- `CHANGES_MADE.md` - Summary of all changes made
- `FILES_CREATED.md` - List of all created files
- `DOCUMENTATION_REORGANIZATION.md` - Documentation cleanup history
- `REORGANIZATION_SUMMARY.md` - Reorganization summary

### 📜 [migration/](./migration/)

Migration history from local scrapers to Azure Functions with WebSocket.

### Key documents
- `MIGRATION*CONTAINER*TO_FUNCTIONS.md` - Container → Functions migration
- `MIGRATION_COMPLETE.md` - Migration completion report
- `CLEANUP_SUMMARY.md` - Cleanup & removed files
- `TRANSFORMATION_SUMMARY.md` - Complete transformation overview

## 🎯 Common Tasks

### I want to

**Get started locally**
→ Read: [QUICKSTART.md](../QUICKSTART.md) → [technical/LOCAL*TESTING*GUIDE.md](./technical/LOCAL*TESTING*GUIDE.md)

**Deploy to Azure**
→ Read: [DEPLOYMENT*GUIDE*WEBSOCKET.md](../DEPLOYMENT*GUIDE*WEBSOCKET.md) → [deployment/DEPLOYMENT*CHECKLIST.md](./deployment/DEPLOYMENT*CHECKLIST.md)

**Understand the system**
→ Read: [README.md](../README.md) → [architecture/ARCHITECTURE.md](./architecture/ARCHITECTURE.md)

**Troubleshoot issues**
→ Read: [technical/LOCAL*TESTING*COMPLETE.md](./technical/LOCAL*TESTING*COMPLETE.md) → [technical/DOCKER*FIX*SUMMARY.md](./technical/DOCKER*FIX*SUMMARY.md)

**Learn about WebSocket implementation**
→ Read: [architecture/WEBSOCKET*SUMMARY.md](./architecture/WEBSOCKET*SUMMARY.md) → [architecture/WEBSOCKET*IMPLEMENTATION.md](./architecture/WEBSOCKET*IMPLEMENTATION.md)

**Understand timeout constraints**
→ Read: [technical/TIMEOUT*QUICK*REF.md](./technical/TIMEOUT*QUICK*REF.md) → [technical/TIMEOUT*CONSIDERATIONS.md](./technical/TIMEOUT*CONSIDERATIONS.md)

**See what changed recently**
→ Read: [technical/CHANGES*MADE.md](./technical/CHANGES*MADE.md) → [technical/FILES*CREATED.md](./technical/FILES*CREATED.md)

## 📊 Document Map

```text

Root Level (Essential):
├── README.md .......................... Project overview & quick start
├── QUICKSTART.md ....................... 5-minute getting started guide
└── DEPLOYMENT*GUIDE*WEBSOCKET.md ....... Azure deployment instructions

docs/architecture/ (System Design):
├── ARCHITECTURE.md ..................... System overview
├── ARCHITECTURE*DECISION*SUMMARY.md .... Design decisions
├── WEBSOCKET_REDESIGN.md ............... Evolution process
├── WEBSOCKET_IMPLEMENTATION.md ......... Technical implementation
├── WEBSOCKET_SUMMARY.md ................ Quick reference
└── WEBSOCKET*VISUAL*GUIDE.md ........... Diagrams & flows

docs/deployment/ (Azure Setup):
├── AZURE_DEPLOYMENT.md ................. Azure configuration
├── AZURE*FUNCTIONS*GUIDE.md ............ Functions setup
├── DEPLOYMENT_CHECKLIST.md ............. Pre-deployment checks
├── READY*TO*DEPLOY.md .................. Final verification
└── GITHUB_SECRETS.md ................... CI/CD configuration

docs/technical/ (Implementation):
├── LOCAL*TESTING*GUIDE.md .............. Docker Compose setup
├── LOCAL*TESTING*COMPLETE.md ........... Status & next steps
├── DOCKER*FIX*SUMMARY.md ............... Issues & fixes
├── TIMEOUT_CONSIDERATIONS.md ........... Timeout analysis
├── TIMEOUT*QUICK*REF.md ................ Quick reference
├── CHANGES_MADE.md ..................... Change summary
└── FILES_CREATED.md .................... Created files list

docs/migration/ (History):
├── MIGRATION*CONTAINER*TO_FUNCTIONS.md  Container migration
├── MIGRATION_COMPLETE.md ............... Completion report
├── CLEANUP_SUMMARY.md .................. Cleanup actions
└── TRANSFORMATION_SUMMARY.md ........... Overall transformation

```text

## 🔍 Key Sections Explained

### Architecture Documents

- **ARCHITECTURE.md**: Understand the overall system design
- **WEBSOCKET_IMPLEMENTATION.md**: Deep dive into how WebSocket listening works
- **ARCHITECTURE*DECISION*SUMMARY.md**: Why we chose this approach

### Deployment Documents

- **DEPLOYMENT*GUIDE*WEBSOCKET.md**: Step-by-step Azure deployment
- **DEPLOYMENT_CHECKLIST.md**: Verify everything before deployment
- **AZURE*FUNCTIONS*GUIDE.md**: Specific Functions configuration

### Technical Documents

- **LOCAL*TESTING*GUIDE.md**: Set up and run locally
- **TIMEOUT_CONSIDERATIONS.md**: Understand timeout constraints
- **CHANGES_MADE.md**: See what was recently changed

### Migration Documents

- **TRANSFORMATION_SUMMARY.md**: Complete overview of all changes
- **MIGRATION*CONTAINER*TO_FUNCTIONS.md**: Why we migrated to Functions
- **CLEANUP_SUMMARY.md**: What was removed

## 💡 Pro Tips

1. **Start with the overview** - Read README.md first

2. **Follow the deployment guide** - Use DEPLOYMENT*GUIDE*WEBSOCKET.md step-by-step

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
