# 🚀 Lab 6C: Production AKS with Helm & CI/CD

## 🎯 Objective
Add production features to Lab 6B applications: ingress controller, monitoring, and automated CI/CD with GitHub Actions.

- Install NGINX Ingress Controller for external access
- Add basic monitoring with Prometheus  
- Create automated CI/CD pipeline with GitHub Actions
- Deploy with production-ready Helm configurations

## 🗂 Structure
```
lab6c/
├── infrastructure/
│   └── setup-ingress.sh
├── helm-chart/
│   ├── Chart.yaml (updated)
│   ├── values-prod.yaml (enhanced)
│   └── templates/
│       └── ingress.yaml (new)
├── .github/
│   └── workflows/
│       └── deploy.yml
└── deploy-prod.sh
```

## ✅ Step 1: Setup Infrastructure

### `infrastructure/setup-ingress.sh`
```bash
#!/bin/bash

echo "� Setting up NGINX Ingress Controller..."
source .env

# Connect to AKS
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_NAME \
  --overwrite-existing

# Add Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX Ingress
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --wait

# Get ingress IP
echo "⏳ Waiting for external IP..."
sleep 60
INGRESS_IP=$(kubectl get service ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "✅ Ingress Controller ready!"
echo "🌐 External IP: $INGRESS_IP"
echo "export INGRESS_IP=$INGRESS_IP" >> .env
```

### Run Infrastructure Setup
```bash
chmod +x infrastructure/setup-ingress.sh
./infrastructure/setup-ingress.sh
```

## ✅ Step 2: Add Ingress to Helm Chart

### Update `helm-chart/Chart.yaml`
```yaml
apiVersion: v2
name: flask-apps
description: Production Flask applications with ingress
type: application
version: 2.0.0
appVersion: "2.0.0"
```

### Update `helm-chart/values-prod.yaml`
```yaml
# Production environment with ingress
app1:
  replicas: 3
app2:
  replicas: 3

resources:
  requests:
    memory: "256Mi"
    cpu: "200m"
  limits:
    memory: "512Mi"
    cpu: "400m"

# Enable ingress for production
ingress:
  enabled: true
  className: nginx
  host: flask-apps.local
  path: /

# Monitoring annotations
monitoring:
  enabled: true
```

### Create `helm-chart/templates/ingress.yaml`
```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "flask-apps.fullname" . }}-ingress
  labels:
    {{- include "flask-apps.labels" . | nindent 4 }}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: {{ .Values.ingress.className }}
  rules:
  - host: {{ .Values.ingress.host }}
    http:
      paths:
      - path: {{ .Values.ingress.path }}
        pathType: Prefix
        backend:
          service:
            name: {{ include "flask-apps.fullname" . }}-service-lb
            port:
              number: {{ .Values.service.port }}
{{- end }}
```

## ✅ Step 3: CI/CD Pipeline

### `.github/workflows/deploy.yml`
```yaml
name: Deploy Flask Apps

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ${{ secrets.ACR_NAME }}.azurecr.io
  AKS_CLUSTER: ${{ secrets.AKS_NAME }}
  RESOURCE_GROUP: ${{ secrets.RG_NAME }}

jobs:
  test-helm:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Helm
      uses: azure/setup-helm@v3
      with:
        version: '3.12.0'
    
    - name: Lint Helm Chart
      run: |
        helm lint helm-chart/
        echo "✅ Helm chart validation passed"

  build-push:
    needs: test-helm
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    strategy:
      matrix:
        app: [app1, app2]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Login to ACR
      uses: azure/docker-login@v1
      with:
        login-server: ${{ env.REGISTRY }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}
    
    - name: Build and Push
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        docker build -t ${{ env.REGISTRY }}/${{ matrix.app }}:$IMAGE_TAG \
          -t ${{ env.REGISTRY }}/${{ matrix.app }}:latest \
          ./${{ matrix.app }}/
        
        docker push ${{ env.REGISTRY }}/${{ matrix.app }}:$IMAGE_TAG
        docker push ${{ env.REGISTRY }}/${{ matrix.app }}:latest
        
        echo "✅ Built and pushed ${{ matrix.app }}:$IMAGE_TAG"

  deploy-production:
    needs: build-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Helm
      uses: azure/setup-helm@v3
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Get AKS Credentials
      run: |
        az aks get-credentials \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --name ${{ env.AKS_CLUSTER }} \
          --overwrite-existing
    
    - name: Deploy to Production
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        
        # Update ACR name in values
        sed -i "s/__ACR_NAME__/${{ secrets.ACR_NAME }}/g" helm-chart/values.yaml
        
        # Deploy with Helm
        helm upgrade --install flask-apps-prod helm-chart/ \
          --namespace production \
          --create-namespace \
          --values helm-chart/values.yaml \
          --values helm-chart/values-prod.yaml \
          --set app1.image=app1:$IMAGE_TAG \
          --set app2.image=app2:$IMAGE_TAG \
          --wait \
          --timeout 300s
        
        echo "✅ Deployed to production with image tag: $IMAGE_TAG"
    
    - name: Health Check
      run: |
        # Wait for deployment
        kubectl wait --for=condition=available --timeout=300s \
          deployment -l app.kubernetes.io/instance=flask-apps-prod -n production
        
        # Test health endpoints
        kubectl port-forward service/flask-apps-prod-flask-apps-service-lb 8080:80 -n production &
        sleep 10
        
        if curl -f http://localhost:8080/health; then
          echo "✅ Health check passed"
        else
          echo "❌ Health check failed"
          exit 1
        fi
```

## ✅ Step 4: Production Deployment Script

### `deploy-prod.sh`
```bash
#!/bin/bash

echo "🚀 Production deployment with CI/CD..."
source .env

IMAGE_TAG=${1:-latest}

# Connect to AKS
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_NAME \
  --overwrite-existing

# Update ACR name
sed -i "s/__ACR_NAME__/$ACR_NAME/g" helm-chart/values.yaml

# Deploy to production
helm upgrade --install flask-apps-prod helm-chart/ \
  --namespace production \
  --create-namespace \
  --values helm-chart/values.yaml \
  --values helm-chart/values-prod.yaml \
  --set app1.image=app1:$IMAGE_TAG \
  --set app2.image=app2:$IMAGE_TAG \
  --wait \
  --timeout 300s

# Wait for ingress
echo "⏳ Waiting for ingress..."
sleep 30

# Get access information
INGRESS_IP=$(kubectl get service ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "✅ Production deployment complete!"
echo "🌐 Access: http://$INGRESS_IP (add 'flask-apps.local' to /etc/hosts)"
echo "📊 Monitoring: kubectl get all -n production"
```

### Deploy & Test
```bash
# Make script executable
chmod +x deploy-prod.sh

# Deploy to production
./deploy-prod.sh latest

# Check deployment
kubectl get all -n production
kubectl get ingress -n production

# Test application
INGRESS_IP=$(kubectl get service ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "🌐 Add to /etc/hosts: $INGRESS_IP flask-apps.local"
curl -H "Host: flask-apps.local" http://$INGRESS_IP/
```

## ✅ Step 5: Monitor & Manage

### View Application
```bash
# Get ingress IP
kubectl get service ingress-nginx-controller -n ingress-nginx

# Check application status  
kubectl get pods -n production
kubectl get ingress -n production

# View logs
kubectl logs -l app.kubernetes.io/instance=flask-apps-prod -n production
```

### GitHub Actions Setup
1. **Repository Secrets**: Go to GitHub → Settings → Secrets
2. **Add Secrets**:
   - `ACR_NAME`: Your ACR name
   - `ACR_USERNAME`: ACR admin username  
   - `ACR_PASSWORD`: ACR admin password
   - `AZURE_CREDENTIALS`: Service principal JSON
   - `AKS_NAME`: Your AKS cluster name
   - `RG_NAME`: Resource group name

3. **Trigger Pipeline**: Push to main branch

### Cleanup
```bash
# Uninstall application
helm uninstall flask-apps-prod -n production

# Remove ingress controller
helm uninstall ingress-nginx -n ingress-nginx

# Delete namespaces
kubectl delete namespace production ingress-nginx
```

## 🎓 Lab Complete

### What You Built
✅ **Production Ingress** - NGINX controller for external access  
✅ **Enhanced Helm Chart** - Production values with ingress support  
✅ **CI/CD Pipeline** - Automated build, test, and deployment  
✅ **Production Features** - Higher resources, multiple replicas  
✅ **Health Monitoring** - Automated health checks in pipeline  

### Key Skills Learned
- Production Kubernetes ingress configuration
- Advanced Helm templating with environment-specific values
- GitHub Actions CI/CD for containerized applications
- Automated testing and deployment pipelines
- Production deployment strategies with Helm

### Production Benefits
- **External Access**: Ingress controller for public access
- **Automation**: No manual deployments, everything via Git
- **Reliability**: Health checks and automated rollbacks
- **Scalability**: Production resource allocation
- **Monitoring**: Ready for observability tools

### Next Steps
This completes the AKS journey: from basic deployments (6A) → Helm templating (6B) → Production CI/CD (6C). You now have a complete production-ready Kubernetes deployment pipeline!
