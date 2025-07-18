# ⚓ Lab 6A: AKS Cluster Setup & Load Balancing

## 🎯 Objective
Create an Azure Kubernetes Service (AKS) cluster and deploy two Flask applications with load balancing.

- Create Azure Container Registry (ACR) and AKS cluster
- Build and push two simple Flask applications to ACR
- Deploy applications to AKS with load balancer
- Test load balancing between multiple app instances
- Use kubectl for basic cluster management

## 🗂 Structure
```
lab6a/
├── scripts/
│   ├── env_setup.sh
│   ├── create-acr.sh
│   └── create-aks.sh
├── app1/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── app2/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── manifests/
│   ├── app1-deployment.yaml
│   ├── app2-deployment.yaml
│   └── loadbalancer-service.yaml
├── deploy.sh
└── cleanup.sh
```

## ✅ Step 1: Environment Setup

### `scripts/env_setup.sh`
```bash
#!/bin/bash
set -e

echo "🔧 Lab 6A Environment Setup"

# Check if logged into Azure, if not login
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

# Generate unique names
ACR_NAME="acr6a$(openssl rand -hex 4)"
AKS_NAME="aks6a$(openssl rand -hex 4)"

cat > .env << EOF
export RG_NAME=lab6a-rg
export LOCATION=australiaeast
export ACR_NAME=$ACR_NAME
export AKS_NAME=$AKS_NAME
EOF

# Create resource group
az group create --name lab6a-rg --location australiaeast

echo "✅ Environment ready"
```

### `scripts/create-acr.sh`
```bash
#!/bin/bash
set -e

echo "🐳 Creating ACR"
source .env

az acr create \
  --resource-group $RG_NAME \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

echo "✅ ACR created: $ACR_NAME"
```

### `scripts/create-aks.sh`
```bash
#!/bin/bash
set -e

echo "⚓ Creating AKS cluster"
source .env

az aks create \
  --resource-group $RG_NAME \
  --name $AKS_NAME \
  --location $LOCATION \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --attach-acr $ACR_NAME \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_NAME \
  --overwrite-existing

echo "✅ AKS cluster created: $AKS_NAME"
kubectl get nodes
```

### Run Setup
```bash
chmod +x scripts/*.sh
./scripts/env_setup.sh
./scripts/create-acr.sh
./scripts/create-aks.sh
```

## ✅ Step 2: Create Flask Applications

### `app1/app.py`
```python
from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        "app": "Flask App 1", 
        "hostname": socket.gethostname(),
        "timestamp": str(datetime.datetime.now())
    })

@app.route("/health")
def health():
    return jsonify(status="healthy", app="app1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `app1/requirements.txt`
```
Flask==2.3.3
```

### `app1/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

### `app2/app.py`
```python
from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        "app": "Flask App 2", 
        "hostname": socket.gethostname(),
        "timestamp": str(datetime.datetime.now())
    })

@app.route("/health")
def health():
    return jsonify(status="healthy", app="app2")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `app2/requirements.txt`
```
Flask==2.3.3
```

### `app2/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

## ✅ Step 3: Create Deployment Script

### `deploy.sh`
```bash
#!/bin/bash

# Lab 6A - Simple AKS Deployment Script
echo "🚀 Starting AKS deployment..."

# Check if kubectl is configured
if ! kubectl cluster-info > /dev/null 2>&1; then
    echo "❌ kubectl not configured. Run 'az aks get-credentials' first"
    exit 1
fi

# Replace ACR name in manifests
ACR_NAME=$(az acr list --resource-group lab-rg --query "[0].name" -o tsv)
if [ -z "$ACR_NAME" ]; then
    echo "❌ No ACR found in resource group lab-rg"
    exit 1
fi

echo "� Using ACR: $ACR_NAME"
sed "s/__ACR_NAME__/$ACR_NAME/g" manifests/deployment.yaml > deployment-final.yaml

# Deploy to Kubernetes
echo "⚓ Deploying to AKS..."
kubectl apply -f deployment-final.yaml
kubectl apply -f manifests/service.yaml

# Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/flask-app

# Get service external IP
echo "🌐 Getting service external IP..."
kubectl get service flask-app-service --watch

echo "✅ Deployment complete!"
echo "💡 Access your app at the EXTERNAL-IP shown above"
```

### `cleanup.sh`
```bash
#!/bin/bash

# Lab 6A - Cleanup Script
echo "🧹 Cleaning up AKS resources..."

kubectl delete deployment flask-app
kubectl delete service flask-app-service
rm -f deployment-final.yaml

echo "✅ Cleanup complete!"
```

## ✅ Step 3: Build and Push Images

### Build Script
```bash
# Build and push images to ACR
source .env

echo "📦 Building and pushing app1..."
az acr build --registry $ACR_NAME --image app1:latest app1/

echo "📦 Building and pushing app2..."
az acr build --registry $ACR_NAME --image app2:latest app2/

echo "✅ Images built and pushed to ACR"
az acr repository list --name $ACR_NAME
```

## ✅ Step 4: Create Kubernetes Manifests

### `manifests/app1-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deployment
  labels:
    app: flask-apps
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-apps
      version: app1
  template:
    metadata:
      labels:
        app: flask-apps
        version: app1
    spec:
      containers:
      - name: app1
        image: __ACR_NAME__.azurecr.io/app1:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### `manifests/app2-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-deployment
  labels:
    app: flask-apps
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-apps
      version: app2
  template:
    metadata:
      labels:
        app: flask-apps
        version: app2
    spec:
      containers:
      - name: app2
        image: __ACR_NAME__.azurecr.io/app2:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### `manifests/loadbalancer-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-loadbalancer
  labels:
    app: flask-apps
spec:
  selector:
    app: flask-apps  # Selects both app1 and app2 pods
  ports:
  - port: 80
    targetPort: 5000
    protocol: TCP
  type: LoadBalancer
```

---

## ✅ Step 4: Deploy & Test

### Deploy to AKS
```bash
# Make script executable
chmod +x deploy.sh cleanup.sh

# Deploy the application
./deploy.sh
```

## ✅ Step 6: Test Load Balancing

### Verify Deployment
```bash
# Check all pods are running
kubectl get pods -l app=flask-apps

# Check service
kubectl get service flask-loadbalancer

# Get external IP
EXTERNAL_IP=$(kubectl get service flask-loadbalancer -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "External IP: $EXTERNAL_IP"
```

### Test Load Balancing
```bash
# Test multiple requests to see load balancing in action
for i in {1..10}; do
  echo "Request $i:"
  curl -s http://$EXTERNAL_IP/ | jq .
  echo "---"
done
```

You should see responses alternating between "Flask App 1" and "Flask App 2" with different hostnames, proving load balancing is working.

### Monitor Pods
```bash
# Watch pod status
kubectl get pods -l app=flask-apps -w

# Check logs from both apps
kubectl logs -l app=flask-apps

# Scale individual deployments
kubectl scale deployment app1-deployment --replicas=3
kubectl scale deployment app2-deployment --replicas=1
```

## ✅ Step 7: Cleanup

When you're done testing:
```bash
# Clean up applications
./cleanup.sh

# Clean up infrastructure (optional)
az group delete --name lab6a-rg --yes --no-wait
```

## 🎓 Lab Complete

### What You Built
✅ **ACR + AKS** - Complete container platform  
✅ **Two Flask Apps** - Different applications with hostname identification  
✅ **Load Balancer** - Kubernetes service distributing traffic  
✅ **Auto-scaling** - Multiple replicas of each application  
✅ **Health Monitoring** - Liveness and readiness probes  

### Key Skills Learned
- Azure Container Registry creation and image management
- AKS cluster setup and kubectl configuration  
- Multi-application deployment with shared load balancer
- Kubernetes service discovery and load balancing
- Container resource management and scaling
- Basic Kubernetes operations and troubleshooting

### Load Balancing Concepts
- **Service Selector**: `app: flask-apps` selects pods from both deployments
- **Round-robin**: Kubernetes distributes requests evenly across healthy pods
- **Health Checks**: Only healthy pods receive traffic via readiness probes
- **Scaling**: Add/remove replicas to handle traffic changes

### Next Steps (Lab 6B Preview)
In the next lab, you'll learn Helm charts to package and template these deployments for multiple environments and easier management.
