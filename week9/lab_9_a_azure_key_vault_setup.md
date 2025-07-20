# 🔐 Lab 9A: Azure Key Vault Setup and Secret Management

## 🎯 Objective
Set up Azure Key Vault using ARM templates and manage database secrets securely. Replace hardcoded credentials with Key Vault references.

- Create Azure Key Vault with ARM template
- Store database connection secrets in Key Vault
- Retrieve secrets using Azure CLI
- Test secret rotation and access policies

## 🗂 Structure
```
lab9a/
├── infrastructure/
│   ├── keyvault-template.json
│   ├── keyvault-parameters.json
│   └── setup-keyvault.sh
├── scripts/
│   ├── store-secrets.sh
│   └── test-secrets.sh
└── README.md
```

## ✅ Step 1: Key Vault ARM Template

### `infrastructure/keyvault-template.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "keyVaultName": {
            "type": "string",
            "defaultValue": "[concat('kv-lab9a-', uniqueString(resourceGroup().id))]",
            "metadata": {
                "description": "Name of the Key Vault"
            }
        },
        "tenantId": {
            "type": "string",
            "defaultValue": "[subscription().tenantId]",
            "metadata": {
                "description": "Tenant ID for Key Vault access"
            }
        },
        "objectId": {
            "type": "string",
            "metadata": {
                "description": "Object ID of the user or service principal for Key Vault access"
            }
        }
    },
    "variables": {
        "location": "[resourceGroup().location]"
    },
    "resources": [
        {
            "type": "Microsoft.KeyVault/vaults",
            "apiVersion": "2022-07-01",
            "name": "[parameters('keyVaultName')]",
            "location": "[variables('location')]",
            "properties": {
                "tenantId": "[parameters('tenantId')]",
                "sku": {
                    "family": "A",
                    "name": "standard"
                },
                "accessPolicies": [
                    {
                        "tenantId": "[parameters('tenantId')]",
                        "objectId": "[parameters('objectId')]",
                        "permissions": {
                            "keys": [
                                "get",
                                "list",
                                "create",
                                "update"
                            ],
                            "secrets": [
                                "get",
                                "list",
                                "set",
                                "delete"
                            ]
                        }
                    }
                ],
                "enabledForDeployment": false,
                "enabledForDiskEncryption": false,
                "enabledForTemplateDeployment": true,
                "enableSoftDelete": true,
                "softDeleteRetentionInDays": 7,
                "enableRbacAuthorization": false,
                "publicNetworkAccess": "Enabled"
            }
        }
    ],
    "outputs": {
        "keyVaultName": {
            "type": "string",
            "value": "[parameters('keyVaultName')]"
        },
        "keyVaultUri": {
            "type": "string",
            "value": "[reference(parameters('keyVaultName')).vaultUri]"
        }
    }
}
```

### `infrastructure/keyvault-parameters.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "keyVaultName": {
            "value": "lab9a-keyvault"
        },
        "objectId": {
            "value": "YOUR_OBJECT_ID_HERE"
        }
    }
}
```

## ✅ Step 2: Key Vault Setup Script

### `infrastructure/setup-keyvault.sh`
```bash
#!/bin/bash
set -e

# Configuration
RG_NAME="lab9a-rg"
LOCATION="australiaeast"

echo "🔐 Setting up Azure Key Vault..."

# Get current user object ID
echo "🔍 Getting current user object ID..."
OBJECT_ID=$(az ad signed-in-user show --query id -o tsv)
echo "Object ID: $OBJECT_ID"

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RG_NAME --location $LOCATION

# Update parameters file with actual object ID
echo "📝 Updating parameters file..."
cat > infrastructure/keyvault-parameters.json << EOF
{
    "\$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "keyVaultName": {
            "value": "lab9a-kv-$(openssl rand -hex 4)"
        },
        "objectId": {
            "value": "$OBJECT_ID"
        }
    }
}
EOF

# Deploy ARM template
echo "🚀 Deploying Key Vault ARM template..."
az deployment group create \
  --resource-group $RG_NAME \
  --template-file infrastructure/keyvault-template.json \
  --parameters infrastructure/keyvault-parameters.json

# Get Key Vault name from deployment
KV_NAME=$(az deployment group show \
  --resource-group $RG_NAME \
  --name keyvault-template \
  --query properties.outputs.keyVaultName.value -o tsv)

KV_URI=$(az deployment group show \
  --resource-group $RG_NAME \
  --name keyvault-template \
  --query properties.outputs.keyVaultUri.value -o tsv)

echo "✅ Key Vault created successfully!"
echo "🔗 Key Vault Name: $KV_NAME"
echo "🔗 Key Vault URI: $KV_URI"

# Save to environment file
cat > .env << EOF
KV_NAME=$KV_NAME
KV_URI=$KV_URI
RG_NAME=$RG_NAME
EOF

echo "💾 Configuration saved to .env file"
```

## ✅ Step 3: Store Database Secrets

### `scripts/store-secrets.sh`
```bash
#!/bin/bash
set -e

# Load environment variables
source .env

echo "🗄️ Storing database secrets in Key Vault..."

# Database connection secrets (from Week 8)
read -p "Enter SQL Server name: " SQL_SERVER
read -p "Enter SQL Database name: " SQL_DATABASE
read -p "Enter SQL Username: " SQL_USERNAME
read -s -p "Enter SQL Password: " SQL_PASSWORD
echo

# Store secrets in Key Vault
echo "🔐 Storing SQL Server secret..."
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "sql-server" \
  --value "$SQL_SERVER"

echo "🔐 Storing SQL Database secret..."
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "sql-database" \
  --value "$SQL_DATABASE"

echo "🔐 Storing SQL Username secret..."
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "sql-username" \
  --value "$SQL_USERNAME"

echo "🔐 Storing SQL Password secret..."
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "sql-password" \
  --value "$SQL_PASSWORD"

# Create connection string secret
CONNECTION_STRING="Server=tcp:$SQL_SERVER,1433;Initial Catalog=$SQL_DATABASE;Persist Security Info=False;User ID=$SQL_USERNAME;Password=$SQL_PASSWORD;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"

echo "🔐 Storing connection string secret..."
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "sql-connection-string" \
  --value "$CONNECTION_STRING"

echo "✅ All database secrets stored successfully!"

# List secrets
echo "📋 Secrets in Key Vault:"
az keyvault secret list --vault-name $KV_NAME --query "[].name" -o table
```

## ✅ Step 4: Test Secret Retrieval

### `scripts/test-secrets.sh`
```bash
#!/bin/bash
set -e

# Load environment variables
source .env

echo "🧪 Testing secret retrieval from Key Vault..."

# Test retrieving individual secrets
echo "🔍 Testing individual secret retrieval..."

SQL_SERVER=$(az keyvault secret show --vault-name $KV_NAME --name "sql-server" --query value -o tsv)
SQL_DATABASE=$(az keyvault secret show --vault-name $KV_NAME --name "sql-database" --query value -o tsv)
SQL_USERNAME=$(az keyvault secret show --vault-name $KV_NAME --name "sql-username" --query value -o tsv)

echo "✅ SQL Server: $SQL_SERVER"
echo "✅ SQL Database: $SQL_DATABASE"
echo "✅ SQL Username: $SQL_USERNAME"
echo "✅ Password: [HIDDEN FOR SECURITY]"

# Test connection string retrieval
echo "🔗 Testing connection string retrieval..."
CONNECTION_STRING=$(az keyvault secret show --vault-name $KV_NAME --name "sql-connection-string" --query value -o tsv)

if [[ -n "$CONNECTION_STRING" ]]; then
    echo "✅ Connection string retrieved successfully (length: ${#CONNECTION_STRING} characters)"
else
    echo "❌ Failed to retrieve connection string"
    exit 1
fi

# Test secret versions
echo "📦 Testing secret versions..."
az keyvault secret list-versions --vault-name $KV_NAME --name "sql-server" --query "[].{Version:id,Created:attributes.created}" -o table

# Test secret permissions
echo "🔒 Testing secret permissions..."
az keyvault secret list --vault-name $KV_NAME --query "length(@)" -o tsv
SECRET_COUNT=$(az keyvault secret list --vault-name $KV_NAME --query "length(@)" -o tsv)
echo "✅ Can access $SECRET_COUNT secrets in Key Vault"

echo "✅ All secret tests passed!"
```

## ✅ Step 5: Deploy and Test

### Run Setup
```bash
# Make scripts executable
chmod +x infrastructure/*.sh scripts/*.sh

# Deploy Key Vault
./infrastructure/setup-keyvault.sh

# Store secrets
./scripts/store-secrets.sh

# Test secret retrieval
./scripts/test-secrets.sh
```

### Verify in Azure Portal
1. Go to Azure Portal → Key vaults
2. Find your Key Vault (lab9a-kv-xxxx)
3. Go to **Secrets** → verify all 5 secrets exist
4. Click on any secret to see versions and values

### Test Secret Rotation
```bash
# Update a secret (simulate rotation)
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "sql-password" \
  --value "NewSecurePassword123!"

# Check versions
az keyvault secret list-versions \
  --vault-name $KV_NAME \
  --name "sql-password" \
  --query "[].{Version:id,Created:attributes.created}" -o table
```

## ✅ Step 6: Integration Example

### Simple Python Script to Access Secrets
```python
# test-keyvault-access.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

# Key Vault URL from environment
key_vault_url = os.environ.get('KV_URI')

if not key_vault_url:
    print("❌ KV_URI environment variable not set")
    exit(1)

# Create credential and client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

try:
    # Retrieve database secrets
    sql_server = client.get_secret("sql-server").value
    sql_database = client.get_secret("sql-database").value
    sql_username = client.get_secret("sql-username").value
    
    print("✅ Successfully retrieved secrets from Key Vault")
    print(f"📊 SQL Server: {sql_server}")
    print(f"📊 SQL Database: {sql_database}")
    print(f"📊 SQL Username: {sql_username}")
    print("🔐 Password: [HIDDEN]")
    
except Exception as e:
    print(f"❌ Error accessing Key Vault: {e}")
```

## ✅ Step 7: Cleanup

### Delete Resources
```bash
# Delete the resource group
az group delete --name lab9a-rg --yes --no-wait
```

## 🎓 Lab Complete

### What You Built
✅ **Azure Key Vault** - Secure secret storage with ARM template  
✅ **Database Secrets** - Stored all SQL connection details securely  
✅ **Access Policies** - Configured proper permissions for secret access  
✅ **Secret Management** - Created, retrieved, and rotated secrets  
✅ **Integration Ready** - Prepared for Managed Identity in Lab 9B  

### Key Skills Learned
- Azure Key Vault provisioning with ARM templates
- Secret storage and retrieval using Azure CLI
- Access policy configuration and management
- Secret versioning and rotation practices
- Secure credential management best practices

### Security Benefits
- **No Hardcoded Secrets**: All credentials stored securely in Key Vault
- **Access Control**: Granular permissions for secret access
- **Audit Trail**: All secret access is logged and monitored
- **Secret Rotation**: Easy credential updates without code changes
- **Encryption**: All secrets encrypted at rest and in transit

Your secrets are now securely managed and ready for integration with Managed Identity in Lab 9B!
