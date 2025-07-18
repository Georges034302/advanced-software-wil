# ⚓ Lab 6D: Bicep AKS Provisioning + Helm Deployment

## 🎯 Objective
Use Bicep templates to provision AKS and Helm to deploy a simple application. Learn Infrastructure as Code with Bicep.

- Create Bicep templates for AKS cluster
- Deploy AKS using Bicep
- Deploy simple app using Helm
- Compare Bicep vs ARM templates

## 🗂 Structure
```
lab6d/
├── bicep/
│   ├── main.bicep
│   └── parameters.json
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── deploy.sh
```

## ✅ Step 1: Simple Flask App

### `app/app.py`
```python
from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Bicep AKS!",
        "hostname": socket.gethostname(),
        "deployed_via": "Bicep + Helm"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### `app/requirements.txt`
```
Flask==2.3.3
```

### `app/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

## ✅ Step 2: Bicep Templates

### `bicep/main.bicep`
```bicep
@description('Project name for resource naming')
param projectName string = 'lab6d'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Kubernetes version')
param kubernetesVersion string = '1.28.5'

var uniqueSuffix = substring(uniqueString(resourceGroup().id), 0, 6)
var acrName = 'acr${projectName}${uniqueSuffix}'
var aksName = 'aks${projectName}${uniqueSuffix}'

// Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// AKS Cluster
resource aks 'Microsoft.ContainerService/managedClusters@2023-08-01' = {
  name: aksName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    kubernetesVersion: kubernetesVersion
    dnsPrefix: '${aksName}-dns'
    agentPoolProfiles: [
      {
        name: 'nodepool1'
        count: 2
        vmSize: 'Standard_B2s'
        osType: 'Linux'
        mode: 'System'
      }
    ]
    networkProfile: {
      networkPlugin: 'kubenet'
      loadBalancerSku: 'standard'
    }
  }
}

// ACR role assignment for AKS
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, aks.id, acr.id)
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: aks.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
  }
}

// Outputs
output acrName string = acr.name
output acrLoginServer string = acr.properties.loginServer
output aksName string = aks.name
output resourceGroupName string = resourceGroup().name
```

### `bicep/parameters.json`
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "projectName": {
      "value": "lab6d"
    },
    "location": {
      "value": "australiaeast"
    }
  }
}
```

## ✅ Step 3: Helm Chart

### `helm-chart/Chart.yaml`
```yaml
apiVersion: v2
name: simple-app
description: Simple Flask app for Bicep AKS demo
type: application
version: 1.0.0
appVersion: "1.0.0"
```

### `helm-chart/values.yaml`
```yaml
# Default values
replicaCount: 2

image:
  repository: __ACR_NAME__.azurecr.io/simple-app
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 5000

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### `helm-chart/templates/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Chart.Name }}
  labels:
    app: {{ .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        ports:
        - containerPort: {{ .Values.service.targetPort }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        livenessProbe:
          httpGet:
            path: /health
            port: {{ .Values.service.targetPort }}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: {{ .Values.service.targetPort }}
          initialDelaySeconds: 5
          periodSeconds: 5
```

### `helm-chart/templates/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Chart.Name }}-service
  labels:
    app: {{ .Chart.Name }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: {{ .Values.service.targetPort }}
    protocol: TCP
  selector:
    app: {{ .Chart.Name }}
```

## ✅ Step 4: Deployment Script

### `deploy.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Lab 6D: Bicep AKS + Helm Deployment"

# Variables
RG_NAME="lab6d-rg"
LOCATION="australiaeast"
DEPLOYMENT_NAME="lab6d-$(date +%H%M%S)"

# Check Azure CLI
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RG_NAME --location $LOCATION

# Deploy Bicep template
echo "🏗️ Deploying Bicep template..."
OUTPUTS=$(az deployment group create \
  --resource-group $RG_NAME \
  --template-file bicep/main.bicep \
  --parameters bicep/parameters.json \
  --name $DEPLOYMENT_NAME \
  --output json)

# Extract outputs
ACR_NAME=$(echo $OUTPUTS | jq -r '.properties.outputs.acrName.value')
AKS_NAME=$(echo $OUTPUTS | jq -r '.properties.outputs.aksName.value')

echo "✅ Infrastructure deployed!"
echo "🐳 ACR: $ACR_NAME"
echo "⚓ AKS: $AKS_NAME"

# Build and push image
echo "📦 Building container image..."
az acr build \
  --registry $ACR_NAME \
  --image simple-app:latest \
  --file app/Dockerfile \
  app/

# Get AKS credentials
echo "🔑 Getting AKS credentials..."
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_NAME \
  --overwrite-existing

# Wait for nodes
echo "⏳ Waiting for AKS nodes..."
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Update Helm chart with ACR name
echo "📝 Updating Helm chart..."
sed -i "s/__ACR_NAME__/$ACR_NAME/g" helm-chart/values.yaml

# Deploy with Helm
echo "⚓ Deploying with Helm..."
helm upgrade --install simple-app helm-chart/ \
  --wait \
  --timeout 300s

# Get service external IP
echo "🌐 Getting service URL..."
sleep 30
EXTERNAL_IP=$(kubectl get service simple-app-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo ""
echo "🎉 Deployment complete!"
echo "🌐 App URL: http://$EXTERNAL_IP"
echo ""
echo "🧪 Test the app:"
echo "  curl http://$EXTERNAL_IP/"
echo "  curl http://$EXTERNAL_IP/health"
echo ""
echo "📊 Check status:"
echo "  kubectl get all"
echo ""
echo "🧹 Cleanup:"
echo "  az group delete --name $RG_NAME --yes --no-wait"
```

## ✅ Step 5: Deploy and Test

### Run Deployment
```bash
chmod +x deploy.sh
./deploy.sh
```

### Test Application
```bash
# Get external IP
EXTERNAL_IP=$(kubectl get service simple-app-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Test endpoints
curl http://$EXTERNAL_IP/
curl http://$EXTERNAL_IP/health

# Check pods
kubectl get pods
kubectl get service
```

### Monitor with Helm
```bash
# List Helm releases
helm list

# Check release status
helm status simple-app

# View Helm values
helm get values simple-app
```

## ✅ Step 6: Cleanup

```bash
# Delete resource group
az group delete --name lab6d-rg --yes --no-wait

# Verify cleanup
az group list --query "[?name=='lab6d-rg']"
```

## 🎓 Lab Complete

### What You Built
✅ **Bicep Infrastructure** - Modern ARM template alternative  
✅ **AKS Cluster** - Managed Kubernetes with ACR integration  
✅ **Helm Deployment** - Templated Kubernetes application  
✅ **Simple Flask App** - Containerized web application  

### Key Skills Learned
- Bicep template creation and deployment
- AKS provisioning with Infrastructure as Code
- Helm chart creation and deployment
- Azure Container Registry integration
- Kubernetes health checks and load balancing

### Bicep vs ARM Benefits
- **Cleaner Syntax**: More readable than JSON
- **Type Safety**: Better validation and IntelliSense
- **Modularity**: Easy to split into modules
- **Transpilation**: Converts to ARM templates

### Production Ready Features
- Health checks (liveness/readiness probes)
- Resource limits and requests
- LoadBalancer service for external access
- ACR integration with managed identity
- Proper Helm templating

This lab demonstrates Infrastructure as Code with Bicep and application deployment with Helm in a simple, production-ready pattern!
