# GitHub Secrets Configuration

To enable automatic deployment via GitHub Actions, configure the following secrets in your GitHub repository.

## Step 1: Access Repository Secrets

1. Go to your repository on GitHub

2. Navigate to **Settings** > **Secrets and variables** > **Actions**

3. Click **New repository secret**

## Step 2: Azure Credentials

### Get Azure Credentials

```bash

# Login to Azure

az login

# Get subscription ID

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Create service principal

az ad sp create-for-rbac --name "GitHub-Actions" \
  --role Contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth

```text

This will output JSON like:

```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.microsoft.com/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}

```text

### Add Secret

Create a new secret called **AZURE_CREDENTIALS** and paste the entire JSON output.

## Step 3: Azure Resource Information

Get these values from your Azure deployment:

```bash

# Set resource group

RESOURCE*GROUP*NAME="badi-oerlikon-rg"

# Get storage account name

STORAGE*ACCOUNT*NAME=$(az deployment group show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name main \
  --query properties.outputs.storageAccountName.value -o tsv)

# Get storage connection string

AZURE*STORAGE*CONNECTION_STRING=$(az storage account show-connection-string \
  --name $STORAGE*ACCOUNT*NAME \
  --resource-group $RESOURCE*GROUP*NAME -o tsv)

# Get container registry info

REGISTRY*LOGIN*SERVER=$(az deployment group show \
  --resource-group $RESOURCE*GROUP*NAME \
  --name main \
  --query properties.outputs.containerRegistryLoginServer.value -o tsv)

# Get registry credentials

REGISTRY_USERNAME=$(az acr credential show \
  --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) \
  --query username -o tsv)

REGISTRY_PASSWORD=$(az acr credential show \
  --name $(echo $REGISTRY*LOGIN*SERVER | cut -d'.' -f1) \
  --query passwords[0].value -o tsv)

# Print for copying

echo "RESOURCE*GROUP*NAME=$RESOURCE*GROUP*NAME"
echo "STORAGE*ACCOUNT*NAME=$STORAGE*ACCOUNT*NAME"
echo "AZURE*STORAGE*CONNECTION*STRING=$AZURE*STORAGE*CONNECTION*STRING"
echo "REGISTRY*LOGIN*SERVER=$REGISTRY*LOGIN*SERVER"
echo "REGISTRY*USERNAME=$REGISTRY*USERNAME"
echo "REGISTRY*PASSWORD=$REGISTRY*PASSWORD"

```text

### Add Secrets

Create the following secrets in GitHub:

| Secret Name | Value |
| --- | --- |
| `RESOURCE*GROUP*NAME` | Your resource group name (e.g., `badi-oerlikon-rg`) |
| `REGISTRY*LOGIN*SERVER` | Container registry URL |
| `REGISTRY_USERNAME` | Container registry username |
| `REGISTRY_PASSWORD` | Container registry password |
| `AZURE*STORAGE*CONNECTION_STRING` | Full storage connection string |
| `WEB*APP*NAME` | Your App Service name (e.g., `badi-oerlikon-dev-app`) |
| `CRAWLER*CONTAINER*NAME` | Crawler container name (e.g., `badi-crawler`) |

## Step 4: Verify Secrets

List configured secrets (names only):

```bash

# In GitHub UI, go to Settings > Secrets and you should see all secrets listed

```text

## Step 5: Test Deployment

1. Make a commit and push to main branch

2. Go to **Actions** tab in GitHub

3. Watch the **Build and Deploy to Azure** workflow

4. Check logs for any errors

## Troubleshooting

### "Pull access denied" error

The service principal needs push access to the container registry:

```bash
REGISTRY*NAME=$(echo $REGISTRY*LOGIN_SERVER | cut -d'.' -f1)
SERVICE*PRINCIPAL*ID=$(az ad sp show --id <your-client-id> --query id -o tsv)

az role assignment create \
  --assignee $SERVICE*PRINCIPAL*ID \
  --role AcrPush \
  --scope /subscriptions/$SUBSCRIPTION*ID/resourceGroups/$RESOURCE*GROUP*NAME/providers/Microsoft.ContainerRegistry/registries/$REGISTRY*NAME

```text

### "Authentication failed" error

Recreate the service principal:

```bash

# Delete old one

az ad sp delete --id <old-client-id>

# Create new one

az ad sp create-for-rbac --name "GitHub-Actions" \
  --role Contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth

```text

Then update the **AZURE_CREDENTIALS** secret.

### "Resource not found" errors

Verify the resource names match exactly:

```bash

# List web apps

az webapp list --resource-group $RESOURCE*GROUP*NAME --query "[].name"

# List containers

az container list --resource-group $RESOURCE*GROUP*NAME --query "[].name"

# List registries

az acr list --resource-group $RESOURCE*GROUP*NAME --query "[].loginServer"

```text

## Security Best Practices

1. **Rotate secrets regularly** (every 90 days)

2. **Use service principals** instead of personal accounts

3. **Limit role scope** to specific resources when possible

4. **Monitor secret access** in Azure Activity Log

5. **Use Azure Key Vault** for sensitive data in production

6. **Never commit secrets** to version control

## Rotating Secrets

To rotate secrets:

```bash

# Get service principal object ID

OBJECT_ID=$(az ad sp show --id <your-client-id> --query id -o tsv)

# Create new credentials

az ad sp credential reset --name "GitHub-Actions" --credential-description "GitHub-Actions-$(date +%s)"

# Update GitHub secrets with new credentials

```text

## Additional Resources

- [GitHub Actions - Azure Login](https://github.com/Azure/login)
- [Azure Service Principal](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
