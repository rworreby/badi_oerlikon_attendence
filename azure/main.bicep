param location string = resourceGroup().location
param environment string = 'dev'
param projectName string = 'badi-oerlikon'

// Storage Account for blob storage
var storageAccountName = '${replace(projectName, '-', '')}${environment}sa'

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-06-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
  }
}

// Blob Services for the storage account
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2021-06-01' = {
  parent: storageAccount
  name: 'default'
}

// Blob Containers
resource scrapedDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-06-01' = {
  parent: blobService
  name: 'scraped-data'
  properties: {
    publicAccess: 'None'
  }
}

resource logsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-06-01' = {
  parent: blobService
  name: 'logs'
  properties: {
    publicAccess: 'None'
  }
}

// App Service Plan
var appServicePlanName = '${projectName}-${environment}-plan'

resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Web App
var webAppName = '${projectName}-${environment}-app'

resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      alwaysOn: true
      linuxFxVersion: 'PYTHON|3.9'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT_NAME'
          value: storageAccount.name
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT_KEY'
          value: listKeys(storageAccount.id, '2021-06-01').keys[0].value
        }
        {
          name: 'BLOB_CONTAINER_NAME'
          value: 'scraped-data'
        }
      ]
    }
  }
}

// Azure Functions for crawler service
var functionAppName = '${projectName}-${environment}-func'
var functionStorageAccountName = '${replace(projectName, '-', '')}${environment}funcsa'
var appInsightsName = '${projectName}-${environment}-insights'

// Storage account for function app
resource functionStorageAccount 'Microsoft.Storage/storageAccounts@2021-06-01' = {
  name: functionStorageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
  }
}

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 30
  }
}

// App Service Plan for Functions (Consumption)
var functionPlanName = '${projectName}-${environment}-func-plan'

resource functionPlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: functionPlanName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {}
}

// Function App
resource functionApp 'Microsoft.Web/sites@2021-02-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: functionPlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.9'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${functionStorageAccount.name};AccountKey=${listKeys(functionStorageAccount.id, '2021-06-01').keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.instrumentationKey
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT_NAME'
          value: storageAccount.name
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT_KEY'
          value: listKeys(storageAccount.id, '2021-06-01').keys[0].value
        }
        {
          name: 'BLOB_CONTAINER_NAME'
          value: 'scraped-data'
        }
        {
          name: 'SCRAPE_URL'
          value: 'https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder/oerlikon.html'
        }
      ]
    }
  }
}

// Outputs
output storageAccountName string = storageAccount.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output functionAppName string = functionApp.name
output appInsightsKey string = appInsights.properties.instrumentationKey
output storageAccountKey string = listKeys(storageAccount.id, '2021-06-01').keys[0].value
