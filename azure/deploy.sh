#!/bin/bash

# Azure Deployment Script for BADI Oerlikon Attendance Tracker
# This script deploys the infrastructure to Azure

set -e

# Configuration
RESOURCE_GROUP_NAME="${RESOURCE_GROUP_NAME:-badi-oerlikon-rg}"
LOCATION="${LOCATION:-eastus}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

echo "🚀 Starting Azure deployment..."
echo "Resource Group: $RESOURCE_GROUP_NAME"
echo "Location: $LOCATION"
echo "Environment: $ENVIRONMENT"

# Create resource group if it doesn't exist
echo "📦 Creating resource group..."
az group create \
  --name "$RESOURCE_GROUP_NAME" \
  --location "$LOCATION"

# Deploy bicep template
echo "🔧 Deploying infrastructure..."
az deployment group create \
  --resource-group "$RESOURCE_GROUP_NAME" \
  --template-file azure/main.bicep \
  --parameters azure/parameters.bicepparam \
  --parameters environment="$ENVIRONMENT"

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 To get resource information, run:"
echo "  az deployment group show -g $RESOURCE_GROUP_NAME -n main --query properties.outputs"
