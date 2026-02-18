# Azure Tools Installation Guide

**Date:** February 17, 2026  
**Status:** ✅ Installation Complete

---

## ✅ Installed Tools

| Tool | Version | Purpose |
|------|---------|---------|
| **Azure CLI** | 2.0.81 | Command-line interface for Azure management |
| **Node.js** | 18.20.8 | JavaScript runtime (required for Azure Functions Core Tools) |
| **npm** | 10.8.2 | Node package manager |
| **Azure Functions Core Tools** | 4.7.0 | Local development and debugging of Azure Functions |

---

## 🚀 Quick Start

### 1. Set Up Shell Environment

The installation added nvm to your shell configuration. To use the new Node.js version immediately:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

Or close and reopen your terminal.

### 2. Log In to Azure

```bash
az login
```

This will open a browser for authentication.

### 3. Set Your Subscription

```bash
az account set --subscription cc569079-9e12-412d-8dfb-a5d60a028f75
```

### 4. Verify Setup

```bash
az account show
```

Should display your subscription details.

---

## 📋 Common Commands

### Azure CLI Commands

```bash
# Show current subscription
az account show

# List all subscriptions
az account list --output table

# Switch subscription
az account set --subscription <subscription-id>

# Login to Azure
az login

# Logout
az logout

# Deploy resource group
az group create --name mygroup --location eastus

# List resources
az resource list --output table
```

### Azure Functions Core Tools Commands

```bash
# Check version
func --version

# Create a new function project
func init MyFunctionProject

# Start function locally (with debugging)
func start

# Create a new function
func new --name MyFunction --template "Timer trigger"

# Publish to Azure
func azure functionapp publish <function-app-name>

# List function apps
func list
```

### npm Commands

```bash
# Check version
npm --version

# Install package globally
npm install -g <package-name>

# Install package locally
npm install <package-name>

# Update npm
npm install -g npm@latest
```

---

## 📁 Project-Specific Setup

### 1. Deploy WebSocket Listener to Azure

```bash
# Read the deployment guide
cat DEPLOYMENT_GUIDE_WEBSOCKET.md

# Follow the steps in the guide
```

### 2. Test Locally with Functions Core Tools

```bash
# Navigate to the functions directory
cd src/functions/websocket_listener

# Start the local Functions runtime
func start
```

Expected output:
```
Azure Functions Core Tools (4.7.0)
Function Runtime Version: 4.x
...
Now listening on: http://0.0.0.0:7071
```

### 3. Deploy to Azure

```bash
# Publish the function
func azure functionapp publish badi-oerlikon-listener

# Monitor execution
az functionapp logs tail --resource-group badi-oerlikon-rg \
  --name badi-oerlikon-listener
```

---

## 🔧 Troubleshooting

### Issue: `func` command not found

**Solution:**
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
func --version
```

### Issue: Azure CLI not found

**Solution:**
```bash
az --version
```

If not found, ensure it was installed via apt-get.

### Issue: Node.js version too old

**Solution:**
```bash
# Check current version
node --version

# If less than v14, upgrade with nvm
nvm install 18
nvm use 18
nvm alias default 18
```

### Issue: Permission denied during npm install

**Solution:**
```bash
# Use sudo or nvm's global installation
sudo npm install -g azure-functions-core-tools@4
```

---

## 📚 Documentation Links

**Azure CLI Documentation:**
https://docs.microsoft.com/cli/azure/

**Azure Functions Core Tools:**
https://github.com/Azure/azure-functions-core-tools

**Azure Functions Documentation:**
https://docs.microsoft.com/azure/azure-functions/

**Node.js Version Manager (nvm):**
https://github.com/nvm-sh/nvm

---

## 🎯 Next Steps

1. **Authenticate with Azure:**
   ```bash
   az login
   az account set --subscription cc569079-9e12-412d-8dfb-a5d60a028f75
   ```

2. **Deploy infrastructure (see DEPLOYMENT_GUIDE_WEBSOCKET.md):**
   ```bash
   # Create resource group
   az group create --name badi-oerlikon-rg --location eastus
   
   # Deploy Bicep templates
   az deployment group create \
     --resource-group badi-oerlikon-rg \
     --template-file infra/main.bicep
   ```

3. **Deploy function:**
   ```bash
   cd src/functions/websocket_listener
   func azure functionapp publish badi-oerlikon-listener
   ```

4. **Monitor execution:**
   ```bash
   func azure functionapp logs tail \
     --resource-group badi-oerlikon-rg \
     --name badi-oerlikon-listener
   ```

---

## 📖 Additional Resources

- [Main README](./README.md)
- [Quick Start Guide](./QUICKSTART.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE_WEBSOCKET.md)
- [Azure Documentation](https://docs.microsoft.com/azure/)

---

**Installation Date:** February 17, 2026  
**Status:** ✅ All tools successfully installed and verified
