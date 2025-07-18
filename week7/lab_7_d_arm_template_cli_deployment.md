# 📄 Lab 7D: ARM Template + CLI App Service Deployment

## 🎯 Objective
Deploy a super simple Flask app to Azure App Service using ARM templates and Azure CLI. Learn Infrastructure as Code for App Service.

- Create ARM template for App Service
- Deploy using Azure CLI
- Simple Flask app deployment
- Compare ARM vs manual deployment

## 🗂 Structure
```
lab7d/
├── app/
│   ├── app.py
│   └── requirements.txt
├── templates/
│   ├── main.json
│   └── parameters.json
└── deploy.sh
```

## ✅ Step 1: Simple Flask App

### `app/app.py`
```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from ARM Template!",
        "deployed_via": "ARM + CLI",
        "app_service": True
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
```

### `app/requirements.txt`
```
Flask==2.3.3
```

## ✅ Step 2: ARM Template

### `templates/main.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "appName": {
            "type": "string",
            "metadata": {
                "description": "Name of the web app"
            }
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]",
            "metadata": {
                "description": "Location for all resources"
            }
        }
    },
    "variables": {
        "appServicePlanName": "[concat(parameters('appName'), '-plan')]",
        "webAppName": "[parameters('appName')]"
    },
    "resources": [
        {
            "type": "Microsoft.Web/serverfarms",
            "apiVersion": "2022-03-01",
            "name": "[variables('appServicePlanName')]",
            "location": "[parameters('location')]",
            "sku": {
                "name": "B1",
                "tier": "Basic"
            },
            "kind": "linux",
            "properties": {
                "reserved": true
            }
        },
        {
            "type": "Microsoft.Web/sites",
            "apiVersion": "2022-03-01",
            "name": "[variables('webAppName')]",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]"
            ],
            "kind": "app,linux",
            "properties": {
                "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]",
                "siteConfig": {
                    "linuxFxVersion": "PYTHON|3.11",
                    "appCommandLine": "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
                }
            }
        }
    ],
    "outputs": {
        "webAppUrl": {
            "type": "string",
            "value": "[concat('https://', reference(resourceId('Microsoft.Web/sites', variables('webAppName'))).defaultHostName)]"
        },
        "webAppName": {
            "type": "string",
            "value": "[variables('webAppName')]"
        }
    }
}
```

### `templates/parameters.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "appName": {
            "value": "lab7d-app"
        },
        "location": {
            "value": "australiaeast"
        }
    }
}
```

## ✅ Step 3: Deploy Script

### `deploy.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Lab 7D: ARM Template + CLI Deployment"

# Variables
RG_NAME="lab7d-rg"
UNIQUE_ID=$(openssl rand -hex 4)
APP_NAME="lab7d-app-$UNIQUE_ID"

# Check Azure CLI
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RG_NAME --location australiaeast

# Update parameters with unique app name
echo "📝 Updating parameters..."
sed "s/lab7d-app/$APP_NAME/g" templates/parameters.json > parameters-temp.json

# Deploy ARM template
echo "🏗️ Deploying ARM template..."
OUTPUTS=$(az deployment group create \
  --resource-group $RG_NAME \
  --template-file templates/main.json \
  --parameters parameters-temp.json \
  --output json)

# Extract outputs
WEB_APP_URL=$(echo $OUTPUTS | jq -r '.properties.outputs.webAppUrl.value')
WEB_APP_NAME=$(echo $OUTPUTS | jq -r '.properties.outputs.webAppName.value')

echo "✅ Infrastructure deployed!"
echo "🌐 App Name: $WEB_APP_NAME"
echo "🔗 URL: $WEB_APP_URL"

# Deploy app code using CLI
echo "📦 Deploying application code..."
cd app

# Create deployment package
zip -r ../app.zip . -x "*.pyc" "__pycache__/*"
cd ..

# Deploy using CLI
az webapp deployment source config-zip \
  --resource-group $RG_NAME \
  --name $WEB_APP_NAME \
  --src app.zip

echo "⏳ Waiting for deployment..."
sleep 30

# Test deployment
echo "🧪 Testing deployment..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $WEB_APP_URL/ || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ App is running!"
else
    echo "⚠️ App might still be starting (Status: $HTTP_STATUS)"
fi

# Cleanup temp files
rm -f parameters-temp.json app.zip

echo ""
echo "🎉 Deployment complete!"
echo "🌐 App URL: $WEB_APP_URL"
echo ""
echo "🧪 Test endpoints:"
echo "  curl $WEB_APP_URL/"
echo "  curl $WEB_APP_URL/health"
echo ""
echo "📊 Monitor deployment:"
echo "  az webapp log tail --name $WEB_APP_NAME --resource-group $RG_NAME"
echo ""
echo "🧹 Cleanup:"
echo "  az group delete --name $RG_NAME --yes --no-wait"
```

## ✅ Step 4: Deploy and Test

### Run Deployment
```bash
chmod +x deploy.sh
./deploy.sh
```

### Test Application
```bash
# Get app URL from deployment output
APP_URL="<your-app-url-from-output>"

# Test endpoints
curl $APP_URL/
curl $APP_URL/health

# View logs
az webapp log tail --name <your-app-name> --resource-group lab7d-rg
```

### Expected Response
```json
{
  "message": "Hello from ARM Template!",
  "deployed_via": "ARM + CLI",
  "app_service": true
}
```

## ✅ Step 5: Monitor and Manage

### Check Deployment Status
```bash
# List web apps
az webapp list --resource-group lab7d-rg --output table

# Get app details
az webapp show --name <your-app-name> --resource-group lab7d-rg --query "{name:name, state:state, defaultHostName:defaultHostName}"

# View deployment logs
az webapp log download --name <your-app-name> --resource-group lab7d-rg
```

### Update Application
```bash
# Make changes to app/app.py
# Then redeploy code only:
cd app
zip -r ../app-update.zip . -x "*.pyc" "__pycache__/*"
cd ..

az webapp deployment source config-zip \
  --resource-group lab7d-rg \
  --name <your-app-name> \
  --src app-update.zip
```

## ✅ Step 6: Cleanup

```bash
# Delete resource group
az group delete --name lab7d-rg --yes --no-wait

# Verify cleanup
az group list --query "[?name=='lab7d-rg']"
```

## 🎓 Lab Complete

### What You Built
✅ **ARM Template** - Infrastructure as Code for App Service  
✅ **App Service Plan** - Linux-based hosting plan  
✅ **Web App** - Python Flask application  
✅ **CLI Deployment** - Code deployment using Azure CLI  

### Key Skills Learned
- ARM template creation for App Service
- Infrastructure and application deployment separation
- Azure CLI code deployment techniques
- App Service configuration for Python apps
- Infrastructure as Code principles

### ARM Template Benefits
- **Reproducible**: Same infrastructure every time
- **Version Controlled**: Template changes tracked in Git
- **Parameterized**: Different environments with same template
- **Dependencies**: Automatic resource ordering

### Deployment Pattern
1. **Infrastructure**: ARM template creates App Service
2. **Application**: CLI deploys code to existing service
3. **Testing**: Automated health checks
4. **Monitoring**: Built-in App Service logging

### Comparison with Previous Labs
- **Lab 7A**: Manual CLI deployment
- **Lab 7B**: Container-based deployment
- **Lab 7C**: Full CI/CD pipeline
- **Lab 7D**: ARM template + CLI hybrid approach

This pattern is ideal for scenarios where infrastructure changes less frequently than application code!
