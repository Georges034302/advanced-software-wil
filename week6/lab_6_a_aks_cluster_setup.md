# ⚓ Lab 6A: AKS Cluster Setup & Basic Deployments

## 🎯 Objective
Create an Azure Kubernetes Service (AKS) cluster and deploy containerized applications using kubectl and basic Kubernetes manifests.

- Set up AKS cluster with Azure CLI
- Understand Kubernetes fundamentals (pods, deployments, services)
- Deploy applications from Azure Container Registry
- Use kubectl for cluster management and debugging
- Implement basic load balancing and scaling

## 🗂 Structure
```
lab6a/
├── manifests/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── scripts/
│   ├── create-aks.sh
│   ├── deploy-app.sh
│   └── cleanup-aks.sh
└── .env (from Lab 5A)
```

## ✅ Step 1: Create AKS Cluster

### `scripts/create-aks.sh`
```bash
#!/bin/bash
set -e

echo "⚓ Creating AKS cluster"
source .env

# AKS cluster configuration
AKS_CLUSTER_NAME="aks-cluster-lab6a"
AKS_NODE_COUNT=2
AKS_NODE_SIZE="Standard_B2s"

echo "📦 Creating AKS cluster..."
az aks create \
  --resource-group $RG_NAME \
  --name $AKS_CLUSTER_NAME \
  --location $LOCATION \
  --node-count $AKS_NODE_COUNT \
  --node-vm-size $AKS_NODE_SIZE \
  --attach-acr $ACR_NAME \
  --enable-managed-identity \
  --generate-ssh-keys \
  --network-plugin azure \
  --load-balancer-sku standard

echo "🔑 Getting AKS credentials..."
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_CLUSTER_NAME \
  --overwrite-existing

# Verify cluster connection
echo "✅ Verifying cluster connection..."
kubectl cluster-info
kubectl get nodes

# Save cluster info to environment
echo "export AKS_CLUSTER_NAME=$AKS_CLUSTER_NAME" >> .env
echo "export AKS_NODE_COUNT=$AKS_NODE_COUNT" >> .env

# Store in GitHub secrets
if command -v gh &> /dev/null; then
    gh auth logout --hostname github.com || true
    
    if [[ -n "$GITHUB_TOKEN" ]]; then
        echo "$GITHUB_TOKEN" | gh auth login --with-token --hostname github.com
        echo "$AKS_CLUSTER_NAME" | gh secret set AKS_CLUSTER_NAME
        echo "✅ AKS cluster info stored in GitHub secrets"
    else
        echo "⚠️ GITHUB_TOKEN not found - skipping secret storage"
    fi
fi

echo ""
echo "✅ AKS cluster created successfully!"
echo "🏷️ Cluster Name: $AKS_CLUSTER_NAME"
echo "📍 Location: $LOCATION"
echo "🖥️ Nodes: $AKS_NODE_COUNT x $AKS_NODE_SIZE"
```

## ✅ Step 2: Create Kubernetes Manifests

### `manifests/namespace.yaml`
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: lab6a-app
  labels:
    name: lab6a-app
    environment: development
```

### `manifests/configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: lab6a-app
data:
  app.name: "Lab 6A Flask App"
  app.version: "1.0.0"
  app.environment: "development"
  database.url: "sqlite:///app.db"
  log.level: "INFO"
```

### `manifests/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  namespace: lab6a-app
  labels:
    app: flask-app
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
        version: v1
    spec:
      containers:
      - name: flask-app
        image: __ACR_NAME__.azurecr.io/acr-lab:latest
        ports:
        - containerPort: 5000
          name: http
        env:
        - name: APP_NAME
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: app.name
        - name: APP_VERSION
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: app.version
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: app.environment
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
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-frontend
  namespace: lab6a-app
  labels:
    app: nginx-frontend
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-frontend
  template:
    metadata:
      labels:
        app: nginx-frontend
        version: v1
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
          name: http
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: html-content
          mountPath: /usr/share/nginx/html/index.html
          subPath: index.html
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config
      - name: html-content
        configMap:
          name: html-content
```

### `manifests/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
  namespace: lab6a-app
  labels:
    app: flask-app
spec:
  selector:
    app: flask-app
  ports:
  - port: 80
    targetPort: 5000
    protocol: TCP
    name: http
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-frontend-service
  namespace: lab6a-app
  labels:
    app: nginx-frontend
spec:
  selector:
    app: nginx-frontend
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  type: LoadBalancer
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: lab6a-app
data:
  nginx.conf: |
    events {
        worker_connections 1024;
    }
    http {
        upstream flask-backend {
            server flask-app-service:80;
        }
        
        server {
            listen 80;
            location /api/ {
                proxy_pass http://flask-backend/;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
            location / {
                root /usr/share/nginx/html;
                index index.html;
                try_files $uri $uri/ /index.html;
            }
        }
    }
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: html-content
  namespace: lab6a-app
data:
  index.html: |
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lab 6A - AKS Deployment</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
            button { background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; margin: 10px; }
            button:hover { background: #45a049; }
            #result { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚓ Lab 6A: AKS Deployment</h1>
            <div class="card">
                <h2>🚀 Kubernetes Application</h2>
                <p>This frontend is running in a Kubernetes pod, making API calls to a Flask backend service.</p>
                <button onclick="testAPI()">Test API Connection</button>
                <button onclick="getClusterInfo()">Get Cluster Info</button>
                <div id="result"></div>
            </div>
        </div>
        <script>
            async function testAPI() {
                try {
                    const response = await fetch('/api/');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = `
                        <h3>✅ API Response</h3>
                        <p><strong>Message:</strong> ${data.message}</p>
                        <p><strong>Timestamp:</strong> ${data.timestamp}</p>
                        <p><strong>Environment:</strong> Kubernetes</p>
                    `;
                } catch (error) {
                    document.getElementById('result').innerHTML = `
                        <h3>❌ API Error</h3>
                        <p>Error: ${error.message}</p>
                    `;
                }
            }
            
            function getClusterInfo() {
                document.getElementById('result').innerHTML = `
                    <h3>⚓ Cluster Information</h3>
                    <p><strong>Platform:</strong> Azure Kubernetes Service (AKS)</p>
                    <p><strong>Frontend:</strong> Nginx Pod (LoadBalancer Service)</p>
                    <p><strong>Backend:</strong> Flask Pods (ClusterIP Service)</p>
                    <p><strong>Scaling:</strong> 3 Flask replicas, 2 Nginx replicas</p>
                `;
            }
        </script>
    </body>
    </html>
```

## ✅ Step 3: Deployment Scripts

### `scripts/deploy-app.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying application to AKS"
source .env

# Ensure we're connected to the right cluster
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_CLUSTER_NAME \
  --overwrite-existing

echo "📝 Updating manifest with ACR name..."
sed "s/__ACR_NAME__/$ACR_NAME/g" manifests/deployment.yaml > /tmp/deployment.yaml

echo "📦 Creating namespace..."
kubectl apply -f manifests/namespace.yaml

echo "🔧 Applying ConfigMaps..."
kubectl apply -f manifests/configmap.yaml

echo "🚀 Deploying applications..."
kubectl apply -f /tmp/deployment.yaml
kubectl apply -f manifests/service.yaml

echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/flask-app -n lab6a-app
kubectl wait --for=condition=available --timeout=300s deployment/nginx-frontend -n lab6a-app

echo "🌐 Getting external IP..."
echo "Waiting for LoadBalancer IP (this may take a few minutes)..."

# Wait for external IP
timeout=300
while [ $timeout -gt 0 ]; do
    EXTERNAL_IP=$(kubectl get service nginx-frontend-service -n lab6a-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [ -n "$EXTERNAL_IP" ] && [ "$EXTERNAL_IP" != "null" ]; then
        echo "✅ External IP obtained: $EXTERNAL_IP"
        break
    fi
    echo "Still waiting for external IP..."
    sleep 10
    ((timeout-=10))
done

if [ -z "$EXTERNAL_IP" ] || [ "$EXTERNAL_IP" = "null" ]; then
    echo "⚠️ External IP not ready yet. Check with: kubectl get service -n lab6a-app"
    EXTERNAL_IP="<pending>"
fi

# Save to environment
echo "export EXTERNAL_IP=$EXTERNAL_IP" >> .env

# Store in GitHub secrets
if command -v gh &> /dev/null; then
    gh auth logout --hostname github.com || true
    
    if [[ -n "$GITHUB_TOKEN" ]]; then
        echo "$GITHUB_TOKEN" | gh auth login --with-token --hostname github.com
        echo "$EXTERNAL_IP" | gh secret set AKS_EXTERNAL_IP
        echo "✅ External IP stored in GitHub secrets"
    else
        echo "⚠️ GITHUB_TOKEN not found - skipping secret storage"
    fi
fi

echo ""
echo "✅ Deployment complete!"
echo "🌐 Frontend URL: http://$EXTERNAL_IP"
echo "📊 Check status: kubectl get all -n lab6a-app"
```

### `scripts/cleanup-aks.sh`
```bash
#!/bin/bash
set -e

echo "🧹 Cleaning up AKS resources"
source .env

# Delete namespace (this removes all resources in the namespace)
kubectl delete namespace lab6a-app --ignore-not-found=true

# Delete AKS cluster
if [[ -n "$AKS_CLUSTER_NAME" ]]; then
    echo "🗑️ Deleting AKS cluster..."
    az aks delete \
      --resource-group $RG_NAME \
      --name $AKS_CLUSTER_NAME \
      --yes \
      --no-wait
    echo "✅ AKS cluster deletion initiated"
fi

echo "✅ Cleanup complete"
```

## ✅ Step 4: Deploy & Test

### Setup AKS Cluster
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Create AKS cluster
./scripts/create-aks.sh
```

### Deploy Application
```bash
# Deploy to AKS
./scripts/deploy-app.sh
```

### Verify Deployment
```bash
# Check cluster status
kubectl get nodes
kubectl get namespaces

# Check application status
kubectl get all -n lab6a-app

# Check pod logs
kubectl logs -l app=flask-app -n lab6a-app
kubectl logs -l app=nginx-frontend -n lab6a-app

# Get service details
kubectl describe service nginx-frontend-service -n lab6a-app
```

## ✅ Step 5: Kubernetes Operations

### Scaling Applications
```bash
# Scale Flask backend
kubectl scale deployment flask-app --replicas=5 -n lab6a-app

# Scale Nginx frontend
kubectl scale deployment nginx-frontend --replicas=3 -n lab6a-app

# Check scaling
kubectl get deployment -n lab6a-app
kubectl get pods -n lab6a-app
```

### Port Forwarding (for testing)
```bash
# Forward Flask service to local port
kubectl port-forward service/flask-app-service 8080:80 -n lab6a-app &

# Test Flask API directly
curl http://localhost:8080/
curl http://localhost:8080/health

# Kill port forward
kill %1
```

### Debugging and Monitoring
```bash
# Get detailed pod information
kubectl describe pods -l app=flask-app -n lab6a-app

# Execute commands in pods
kubectl exec -it deployment/flask-app -n lab6a-app -- /bin/bash

# View resource usage
kubectl top nodes
kubectl top pods -n lab6a-app

# View events
kubectl get events -n lab6a-app --sort-by='.lastTimestamp'
```

### Update Deployment
```bash
# Update Flask app image (example)
kubectl set image deployment/flask-app flask-app=$ACR_NAME.azurecr.io/acr-lab:v2 -n lab6a-app

# Check rollout status
kubectl rollout status deployment/flask-app -n lab6a-app

# View rollout history
kubectl rollout history deployment/flask-app -n lab6a-app

# Rollback if needed
kubectl rollout undo deployment/flask-app -n lab6a-app
```

## ✅ Step 6: Testing & Validation

### Test Application
```bash
source .env

# Test frontend
curl http://$EXTERNAL_IP/

# Test API through nginx proxy
curl http://$EXTERNAL_IP/api/
curl http://$EXTERNAL_IP/api/health

# Load test to verify scaling
for i in {1..20}; do
  curl http://$EXTERNAL_IP/api/ &
done
wait

# Check if pods scaled
kubectl get pods -n lab6a-app
```

### Cleanup
```bash
./scripts/cleanup-aks.sh
```

## 🎓 Complete

### What You Built
✅ **AKS Cluster** - Managed Kubernetes cluster with 2 nodes
✅ **Multi-tier Application** - Frontend (Nginx) + Backend (Flask) architecture
✅ **Kubernetes Resources** - Deployments, Services, ConfigMaps, Namespaces
✅ **Load Balancing** - External LoadBalancer for public access
✅ **Auto-scaling** - Multiple pod replicas with resource limits
✅ **Health Monitoring** - Liveness and readiness probes

### Key Skills Learned
- AKS cluster creation and management with Azure CLI
- Kubernetes fundamentals: pods, deployments, services, configmaps
- kubectl command-line operations and debugging
- Container resource management and scaling
- Load balancing and service discovery in Kubernetes
- Application deployment patterns and best practices

### Next Steps (Lab 6B Preview)
- Package applications using Helm charts
- Template management with values.yaml
- Helm installation and upgrade workflows
- Multi-environment deployment strategies
