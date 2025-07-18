# 📄 Lab 5E: ARM Template Deployment to Azure Container Apps

## 🎯 Objective
Deploy a simple Flask application to Azure Container Apps using ARM (Azure Resource Manager) templates for Infrastructure as Code provisioning.

- Create ARM templates for Azure Container Registry and Container Apps
- Build a simple Flask "Hello World" application
- Deploy infrastructure and application using ARM templates
- Learn Infrastructure as Code principles and deployment patterns
- Compare ARM template deployment vs manual/CLI deployment

## 🗂 Structure
```
lab5e/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── templates/
│   ├── main.json (main ARM template)
│   ├── parameters.json (parameters file)
│   └── nested/
│       ├── acr.json (ACR template)
│       └── containerapp.json (Container App template)
├── scripts/
│   ├── build-image.sh
│   ├── deploy-arm.sh
│   └── cleanup.sh
└── README.md
```

## 🧭 Prerequisites

- Azure CLI installed and authenticated (`az login`)
- Docker installed locally
- Basic understanding of JSON and ARM template syntax
- **Register Container Apps provider:**

```bash
# Register required providers
az provider register --namespace Microsoft.ContainerService
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# Verify registration
az provider show --namespace Microsoft.App --query registrationState
```

## ✅ Step 1: Create Simple Flask Application

### `app/app.py`
```python
from flask import Flask, jsonify
import os
import datetime
import socket

app = Flask(__name__)

# Configuration
VERSION = os.environ.get('APP_VERSION', '1.0.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Azure Container Apps!",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now().isoformat(),
        "deployed_via": "ARM Template"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-hello-world",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "uptime": "running"
    })

@app.route('/info')
def info():
    return jsonify({
        "application": {
            "name": "Flask Hello World",
            "version": VERSION,
            "environment": ENVIRONMENT,
            "deployment_method": "ARM Template",
            "platform": "Azure Container Apps"
        },
        "server": {
            "hostname": socket.gethostname(),
            "python_version": os.sys.version,
            "timestamp": datetime.datetime.now().isoformat()
        },
        "endpoints": [
            {"path": "/", "description": "Main hello endpoint"},
            {"path": "/health", "description": "Health check"},
            {"path": "/info", "description": "Application information"},
            {"path": "/env", "description": "Environment variables"}
        ]
    })

@app.route('/env')
def env_vars():
    # Show safe environment variables
    safe_env = {
        "APP_VERSION": os.environ.get('APP_VERSION', 'Not set'),
        "ENVIRONMENT": os.environ.get('ENVIRONMENT', 'Not set'),
        "PORT": os.environ.get('PORT', 'Not set'),
        "PYTHONPATH": os.environ.get('PYTHONPATH', 'Not set')
    }
    
    return jsonify({
        "environment_variables": safe_env,
        "total_env_vars": len(os.environ),
        "note": "Only showing safe environment variables"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(ENVIRONMENT == 'development'))
```

### `app/requirements.txt`
```
Flask==2.3.3
gunicorn==21.2.0
```

### `app/Dockerfile`
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
```

## ✅ Step 2: Create ARM Templates

### `templates/main.json` (Main Template)
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "metadata": {
        "description": "Deploy Flask Hello World app to Azure Container Apps using ARM templates"
    },
    "parameters": {
        "projectName": {
            "type": "string",
            "minLength": 3,
            "maxLength": 10,
            "metadata": {
                "description": "Project name used for resource naming"
            }
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]",
            "metadata": {
                "description": "Location for all resources"
            }
        },
        "environment": {
            "type": "string",
            "defaultValue": "development",
            "allowedValues": [
                "development",
                "staging",
                "production"
            ],
            "metadata": {
                "description": "Environment type"
            }
        },
        "appVersion": {
            "type": "string",
            "defaultValue": "1.0.0",
            "metadata": {
                "description": "Application version"
            }
        },
        "containerImage": {
            "type": "string",
            "metadata": {
                "description": "Container image name (will be built and pushed to ACR)"
            }
        }
    },
    "variables": {
        "uniqueSuffix": "[substring(uniqueString(resourceGroup().id), 0, 6)]",
        "acrName": "[concat('acr', parameters('projectName'), variables('uniqueSuffix'))]",
        "logAnalyticsWorkspaceName": "[concat('law-', parameters('projectName'), '-', variables('uniqueSuffix'))]",
        "containerAppEnvironmentName": "[concat('cae-', parameters('projectName'), '-', variables('uniqueSuffix'))]",
        "containerAppName": "[concat('ca-', parameters('projectName'), '-', variables('uniqueSuffix'))]"
    },
    "resources": [
        {
            "type": "Microsoft.OperationalInsights/workspaces",
            "apiVersion": "2022-10-01",
            "name": "[variables('logAnalyticsWorkspaceName')]",
            "location": "[parameters('location')]",
            "properties": {
                "sku": {
                    "name": "PerGB2018"
                },
                "retentionInDays": 30
            }
        },
        {
            "type": "Microsoft.ContainerRegistry/registries",
            "apiVersion": "2023-01-01-preview",
            "name": "[variables('acrName')]",
            "location": "[parameters('location')]",
            "sku": {
                "name": "Basic"
            },
            "properties": {
                "adminUserEnabled": true,
                "publicNetworkAccess": "Enabled"
            }
        },
        {
            "type": "Microsoft.App/managedEnvironments",
            "apiVersion": "2023-05-01",
            "name": "[variables('containerAppEnvironmentName')]",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName'))]"
            ],
            "properties": {
                "appLogsConfiguration": {
                    "destination": "log-analytics",
                    "logAnalyticsConfiguration": {
                        "customerId": "[reference(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName'))).customerId]",
                        "sharedKey": "[listKeys(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').primarySharedKey]"
                    }
                }
            }
        },
        {
            "type": "Microsoft.App/containerApps",
            "apiVersion": "2023-05-01",
            "name": "[variables('containerAppName')]",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[resourceId('Microsoft.App/managedEnvironments', variables('containerAppEnvironmentName'))]",
                "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]"
            ],
            "properties": {
                "managedEnvironmentId": "[resourceId('Microsoft.App/managedEnvironments', variables('containerAppEnvironmentName'))]",
                "configuration": {
                    "ingress": {
                        "external": true,
                        "targetPort": 5000,
                        "allowInsecure": false,
                        "traffic": [
                            {
                                "weight": 100,
                                "latestRevision": true
                            }
                        ]
                    },
                    "registries": [
                        {
                            "server": "[concat(variables('acrName'), '.azurecr.io')]",
                            "username": "[variables('acrName')]",
                            "passwordSecretRef": "acr-password"
                        }
                    ],
                    "secrets": [
                        {
                            "name": "acr-password",
                            "value": "[listCredentials(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName')), '2023-01-01-preview').passwords[0].value]"
                        }
                    ]
                },
                "template": {
                    "containers": [
                        {
                            "name": "flask-hello-world",
                            "image": "[concat(variables('acrName'), '.azurecr.io/', parameters('containerImage'))]",
                            "env": [
                                {
                                    "name": "APP_VERSION",
                                    "value": "[parameters('appVersion')]"
                                },
                                {
                                    "name": "ENVIRONMENT",
                                    "value": "[parameters('environment')]"
                                },
                                {
                                    "name": "PORT",
                                    "value": "5000"
                                }
                            ],
                            "resources": {
                                "cpu": 0.25,
                                "memory": "0.5Gi"
                            },
                            "probes": [
                                {
                                    "type": "Liveness",
                                    "httpGet": {
                                        "path": "/health",
                                        "port": 5000
                                    },
                                    "initialDelaySeconds": 30,
                                    "periodSeconds": 10,
                                    "timeoutSeconds": 5,
                                    "failureThreshold": 3
                                },
                                {
                                    "type": "Readiness",
                                    "httpGet": {
                                        "path": "/health",
                                        "port": 5000
                                    },
                                    "initialDelaySeconds": 10,
                                    "periodSeconds": 5,
                                    "timeoutSeconds": 3,
                                    "failureThreshold": 3
                                }
                            ]
                        }
                    ],
                    "scale": {
                        "minReplicas": 1,
                        "maxReplicas": 5,
                        "rules": [
                            {
                                "name": "http-scaling",
                                "http": {
                                    "metadata": {
                                        "concurrentRequests": "10"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    ],
    "outputs": {
        "acrName": {
            "type": "string",
            "value": "[variables('acrName')]"
        },
        "acrLoginServer": {
            "type": "string",
            "value": "[reference(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))).loginServer]"
        },
        "containerAppFqdn": {
            "type": "string",
            "value": "[reference(resourceId('Microsoft.App/containerApps', variables('containerAppName'))).configuration.ingress.fqdn]"
        },
        "containerAppUrl": {
            "type": "string",
            "value": "[concat('https://', reference(resourceId('Microsoft.App/containerApps', variables('containerAppName'))).configuration.ingress.fqdn)]"
        },
        "resourceGroupName": {
            "type": "string",
            "value": "[resourceGroup().name]"
        }
    }
}
```

### `templates/parameters.json` (Parameters File)
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "projectName": {
            "value": "lab5e"
        },
        "location": {
            "value": "australiaeast"
        },
        "environment": {
            "value": "development"
        },
        "appVersion": {
            "value": "1.0.0"
        },
        "containerImage": {
            "value": "flask-hello-world:latest"
        }
    }
}
```

## ✅ Step 3: Build and Deploy Scripts

### `scripts/build-image.sh`
```bash
#!/bin/bash
set -e

echo "🐳 Building Flask Hello World container image..."

# Check if ACR name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <acr-name>"
    echo "Example: $0 acrlab5eabc123"
    exit 1
fi

ACR_NAME=$1
IMAGE_NAME="flask-hello-world:latest"

echo "📦 ACR Name: $ACR_NAME"
echo "🏷️ Image Name: $IMAGE_NAME"

# Login to ACR
echo "🔐 Logging into ACR..."
az acr login --name $ACR_NAME

# Build and push image using ACR build
echo "🏗️ Building image in ACR..."
az acr build \
    --registry $ACR_NAME \
    --image $IMAGE_NAME \
    --file app/Dockerfile \
    app/

echo "✅ Image built and pushed successfully!"
echo "📋 Image: $ACR_NAME.azurecr.io/$IMAGE_NAME"

# Verify image exists
echo "🔍 Verifying image in registry..."
az acr repository show \
    --name $ACR_NAME \
    --image $IMAGE_NAME

echo "✅ Build complete!"
```

### `scripts/deploy-arm.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying Flask Hello World using ARM templates..."

# Generate unique deployment name
DEPLOYMENT_NAME="lab5e-deployment-$(date +%Y%m%d-%H%M%S)"
RESOURCE_GROUP_NAME="lab5e-rg"
LOCATION="australiaeast"

# Create resource group
echo "📦 Creating resource group..."
az group create \
    --name $RESOURCE_GROUP_NAME \
    --location $LOCATION

echo "📋 Resource Group: $RESOURCE_GROUP_NAME"
echo "📍 Location: $LOCATION"
echo "🏷️ Deployment: $DEPLOYMENT_NAME"

# Deploy ARM template
echo "🏗️ Deploying ARM template..."
DEPLOYMENT_OUTPUT=$(az deployment group create \
    --resource-group $RESOURCE_GROUP_NAME \
    --template-file templates/main.json \
    --parameters templates/parameters.json \
    --name $DEPLOYMENT_NAME \
    --output json)

# Extract outputs
ACR_NAME=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.acrName.value')
ACR_LOGIN_SERVER=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.acrLoginServer.value')
CONTAINER_APP_URL=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.containerAppUrl.value')

echo ""
echo "✅ Infrastructure deployment complete!"
echo "🐳 ACR Name: $ACR_NAME"
echo "🌐 ACR Login Server: $ACR_LOGIN_SERVER"
echo ""

# Save deployment info
cat > deployment-info.json << EOF
{
    "deploymentName": "$DEPLOYMENT_NAME",
    "resourceGroupName": "$RESOURCE_GROUP_NAME",
    "acrName": "$ACR_NAME",
    "acrLoginServer": "$ACR_LOGIN_SERVER",
    "containerAppUrl": "$CONTAINER_APP_URL",
    "deployedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "📝 Deployment info saved to deployment-info.json"

# Build and push container image
echo ""
echo "🐳 Building and pushing container image..."
./scripts/build-image.sh $ACR_NAME

# Update container app with new image
echo ""
echo "🔄 Updating container app..."
az containerapp update \
    --name $(az containerapp list --resource-group $RESOURCE_GROUP_NAME --query "[0].name" -o tsv) \
    --resource-group $RESOURCE_GROUP_NAME \
    --image $ACR_LOGIN_SERVER/flask-hello-world:latest

echo ""
echo "⏳ Waiting for deployment to complete..."
sleep 30

# Get final URL
FINAL_URL=$(az deployment group show \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $DEPLOYMENT_NAME \
    --query 'properties.outputs.containerAppUrl.value' \
    -o tsv)

echo ""
echo "🎉 Deployment complete!"
echo "🌐 Application URL: $FINAL_URL"
echo "🧪 Test endpoints:"
echo "   - Health: $FINAL_URL/health"
echo "   - Info: $FINAL_URL/info"
echo "   - Environment: $FINAL_URL/env"
echo ""
echo "📊 Monitor your deployment:"
echo "   az containerapp list --resource-group $RESOURCE_GROUP_NAME --output table"
echo ""
echo "🧹 Clean up when done:"
echo "   ./scripts/cleanup.sh"
```

### `scripts/cleanup.sh`
```bash
#!/bin/bash
set -e

echo "🧹 Cleaning up Lab 5E resources..."

# Default resource group name
RESOURCE_GROUP_NAME=${1:-"lab5e-rg"}

echo "🗑️ Deleting resource group: $RESOURCE_GROUP_NAME"
echo "⚠️ This will delete ALL resources in the resource group!"

# Confirm deletion
read -p "Are you sure you want to delete resource group '$RESOURCE_GROUP_NAME'? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled"
    exit 1
fi

# Delete resource group
az group delete \
    --name $RESOURCE_GROUP_NAME \
    --yes \
    --no-wait

echo "✅ Cleanup initiated"
echo "🔍 Monitor deletion progress:"
echo "   az group list --query \"[?name=='$RESOURCE_GROUP_NAME']\""
echo ""
echo "📝 Clean up local files:"
echo "   rm -f deployment-info.json"
```

## ✅ Step 4: Deploy Application

### Make Scripts Executable
```bash
chmod +x scripts/*.sh
```

### Deploy Infrastructure and Application
```bash
# Deploy everything with ARM templates
./scripts/deploy-arm.sh
```

The script will:
1. Create a resource group
2. Deploy the ARM template (ACR, Log Analytics, Container App Environment, Container App)
3. Build and push the container image
4. Update the container app with the new image
5. Display the application URL

### Check Deployment Status
```bash
# View deployment details
cat deployment-info.json

# Check container app status
az containerapp list --resource-group lab5e-rg --output table

# View container app details
az containerapp show \
    --name $(az containerapp list --resource-group lab5e-rg --query "[0].name" -o tsv) \
    --resource-group lab5e-rg
```

## ✅ Step 5: Test Application

### Test Endpoints
```bash
# Get the application URL from deployment info
APP_URL=$(cat deployment-info.json | jq -r '.containerAppUrl')

echo "🧪 Testing Flask Hello World application..."
echo "🌐 App URL: $APP_URL"

# Test main endpoint
echo "📍 Testing main endpoint..."
curl $APP_URL/

# Test health endpoint
echo "🏥 Testing health endpoint..."
curl $APP_URL/health

# Test info endpoint
echo "ℹ️ Testing info endpoint..."
curl $APP_URL/info

# Test environment endpoint
echo "🔧 Testing environment endpoint..."
curl $APP_URL/env
```

### Browser Testing
```bash
# Open application in browser
APP_URL=$(cat deployment-info.json | jq -r '.containerAppUrl')
echo "🌐 Open in browser: $APP_URL"

# Test these endpoints:
echo "📋 Test these URLs in your browser:"
echo "   - Main: $APP_URL/"
echo "   - Health: $APP_URL/health"
echo "   - Info: $APP_URL/info"
echo "   - Environment: $APP_URL/env"
```

### Expected Responses

**Main Endpoint (`/`):**
```json
{
  "message": "Hello from Azure Container Apps!",
  "version": "1.0.0",
  "environment": "development",
  "hostname": "ca-lab5e-abc123--xyz",
  "timestamp": "2024-01-15T10:30:00.123456",
  "deployed_via": "ARM Template"
}
```

**Health Endpoint (`/health`):**
```json
{
  "status": "healthy",
  "service": "flask-hello-world",
  "version": "1.0.0",
  "environment": "development",
  "uptime": "running"
}
```

## ✅ Step 6: Monitor and Manage

### View Container App Logs
```bash
# Get container app name
CONTAINER_APP_NAME=$(az containerapp list --resource-group lab5e-rg --query "[0].name" -o tsv)

# View logs
az containerapp logs show \
    --name $CONTAINER_APP_NAME \
    --resource-group lab5e-rg \
    --follow

# View recent logs
az containerapp logs show \
    --name $CONTAINER_APP_NAME \
    --resource-group lab5e-rg \
    --tail 50
```

### Scale Application
```bash
# Scale up manually
az containerapp update \
    --name $CONTAINER_APP_NAME \
    --resource-group lab5e-rg \
    --min-replicas 2 \
    --max-replicas 10

# Check replica status
az containerapp replica list \
    --name $CONTAINER_APP_NAME \
    --resource-group lab5e-rg \
    --output table
```

### Update Application
```bash
# Update to new version
# 1. Modify app/app.py (change VERSION variable)
# 2. Update parameters.json (change appVersion)
# 3. Redeploy

# Update parameters file
sed -i 's/"1.0.0"/"1.1.0"/g' templates/parameters.json

# Redeploy with updated version
./scripts/deploy-arm.sh
```

## ✅ Step 7: ARM Template Analysis

### Template Structure Benefits
✅ **Infrastructure as Code**: Version-controlled infrastructure  
✅ **Repeatability**: Consistent deployments across environments  
✅ **Dependencies**: Automatic resource dependency management  
✅ **Parameterization**: Environment-specific configurations  
✅ **Outputs**: Structured deployment information  

### ARM vs CLI Comparison

| Aspect | ARM Templates | Azure CLI (Previous Labs) |
|--------|---------------|----------------------------|
| **Approach** | Declarative | Imperative |
| **Repeatability** | High | Medium |
| **Version Control** | Easy | Complex |
| **Dependencies** | Automatic | Manual ordering |
| **Rollback** | Template-based | Manual |
| **Environment Parity** | Excellent | Good |
| **Learning Curve** | Steeper | Gentler |

### Production Benefits
- **Environment Consistency**: Same template for dev/staging/prod
- **Change Management**: Template diffs show infrastructure changes
- **Automation**: Easy CI/CD integration
- **Documentation**: Templates serve as infrastructure documentation
- **Compliance**: Enforced standards through templates

## ✅ Step 8: Cleanup

### Remove All Resources
```bash
# Clean up everything
./scripts/cleanup.sh

# Confirm cleanup
az group list --query "[?name=='lab5e-rg']"

# Remove local files
rm -f deployment-info.json
```

## 🎓 Lab Complete

### What You Built
✅ **ARM Template Infrastructure** - Complete IaC deployment  
✅ **Simple Flask Application** - Hello World with health checks  
✅ **Azure Container Registry** - Private container registry  
✅ **Container Apps Environment** - Managed container platform  
✅ **Production Configuration** - Health probes, scaling, logging  

### Key Skills Learned
- ARM template creation and structure
- Infrastructure as Code principles and benefits
- Declarative vs imperative deployment approaches
- Container app configuration in ARM templates
- Azure resource dependencies and relationships
- Production-ready container app deployment
- ARM template parameterization and outputs

### ARM Template Benefits Demonstrated
- **Consistency**: Identical infrastructure every deployment
- **Documentation**: Templates document infrastructure
- **Version Control**: Infrastructure changes tracked in Git
- **Automation**: Easy integration with CI/CD pipelines
- **Dependencies**: Automatic resource ordering
- **Rollback**: Easy revert to previous template versions

### Comparison with Previous Labs
- **Lab 5A-5D**: Imperative CLI-based deployment
- **Lab 5E**: Declarative template-based deployment
- **Production**: ARM templates preferred for repeatability

### Next Steps
- Convert Labs 5A-5D deployments to ARM templates
- Create parameter files for multiple environments
- Integrate ARM templates with CI/CD pipelines
- Explore Bicep as a more readable ARM alternative

This completes the Azure Container deployment track with Infrastructure as Code using ARM templates!
