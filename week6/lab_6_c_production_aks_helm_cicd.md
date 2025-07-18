# 🚀 Lab 6C: Production AKS with Helm & CI/CD

## 🎯 Objective
Deploy production-ready applications on AKS using advanced Helm features, ingress controllers, monitoring, and automated CI/CD pipelines with GitHub Actions.

- Implement NGINX Ingress Controller with TLS termination
- Set up monitoring with Prometheus and Grafana
- Create blue-green and canary deployment strategies
- Build automated CI/CD pipelines with Helm and GitHub Actions
- Implement security best practices and resource management

## 🗂 Structure
```
lab6c/
├── helm-charts/
│   └── production-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-staging.yaml
│       ├── values-production.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── ingress.yaml
│           ├── networkpolicy.yaml
│           ├── pdb.yaml
│           ├── serviceaccount.yaml
│           └── monitoring/
│               ├── servicemonitor.yaml
│               └── grafana-dashboard.yaml
├── infrastructure/
│   ├── nginx-ingress/
│   │   └── values.yaml
│   ├── monitoring/
│   │   ├── prometheus-values.yaml
│   │   └── grafana-values.yaml
│   └── cert-manager/
│       └── values.yaml
├── scripts/
│   ├── setup-infrastructure.sh
│   ├── deploy-production.sh
│   ├── blue-green-deploy.sh
│   └── monitoring-setup.sh
├── .github/
│   └── workflows/
│       ├── helm-ci.yml
│       └── production-deploy.yml
└── .env (from Lab 6B)
```

## ✅ Step 1: Infrastructure Setup

### `scripts/setup-infrastructure.sh`
```bash
#!/bin/bash
set -e

echo "🏗️ Setting up production infrastructure"
source .env

# Ensure we're connected to AKS
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_CLUSTER_NAME \
  --overwrite-existing

echo "📦 Adding Helm repositories..."
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add jetstack https://charts.jetstack.io
helm repo update

echo "🌐 Installing NGINX Ingress Controller..."
kubectl create namespace ingress-nginx --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --values infrastructure/nginx-ingress/values.yaml \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz \
  --wait

echo "🔒 Installing Cert-Manager..."
kubectl create namespace cert-manager --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v1.13.0 \
  --set installCRDs=true \
  --wait

echo "📊 Installing Prometheus & Grafana..."
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Install Prometheus
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values infrastructure/monitoring/prometheus-values.yaml \
  --wait

echo "⏳ Waiting for ingress controller to get external IP..."
timeout=300
while [ $timeout -gt 0 ]; do
    INGRESS_IP=$(kubectl get service ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [ -n "$INGRESS_IP" ] && [ "$INGRESS_IP" != "null" ]; then
        echo "✅ Ingress Controller IP: $INGRESS_IP"
        break
    fi
    echo "Waiting for ingress IP..."
    sleep 10
    ((timeout-=10))
done

# Save ingress IP to environment
echo "export INGRESS_IP=$INGRESS_IP" >> .env

echo ""
echo "✅ Infrastructure setup complete!"
echo "🌐 Ingress IP: $INGRESS_IP"
echo "📊 Grafana: http://$INGRESS_IP/grafana (admin/prom-operator)"
echo "📈 Prometheus: http://$INGRESS_IP/prometheus"
```

### `infrastructure/nginx-ingress/values.yaml`
```yaml
controller:
  replicaCount: 2
  
  service:
    type: LoadBalancer
    externalTrafficPolicy: Local
    annotations:
      service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: /healthz
  
  config:
    use-forwarded-headers: "true"
    compute-full-forwarded-for: "true"
    use-proxy-protocol: "false"
    
  metrics:
    enabled: true
    serviceMonitor:
      enabled: true
      namespace: monitoring
      
  resources:
    requests:
      cpu: 100m
      memory: 90Mi
    limits:
      cpu: 200m
      memory: 256Mi
      
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
    
  podDisruptionBudget:
    enabled: true
    minAvailable: 1
```

### `infrastructure/monitoring/prometheus-values.yaml`
```yaml
prometheus:
  prometheusSpec:
    retention: 30d
    resources:
      requests:
        memory: 512Mi
        cpu: 200m
      limits:
        memory: 2Gi
        cpu: 1000m
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: managed-premium
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 50Gi

grafana:
  adminPassword: "admin123"
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - grafana.local
    path: /grafana
    pathType: Prefix
  
  persistence:
    enabled: true
    size: 10Gi
    storageClassName: managed-premium
    
  resources:
    requests:
      memory: 128Mi
      cpu: 100m
    limits:
      memory: 256Mi
      cpu: 200m

alertmanager:
  alertmanagerSpec:
    resources:
      requests:
        memory: 128Mi
        cpu: 50m
      limits:
        memory: 256Mi
        cpu: 100m
```

## ✅ Step 2: Production Helm Chart

### `helm-charts/production-app/Chart.yaml`
```yaml
apiVersion: v2
name: production-app
description: Production-ready microservices application
type: application
version: 2.0.0
appVersion: "2.0.0"
home: https://github.com/your-org/production-app
maintainers:
  - name: DevOps Team
    email: devops@company.com
keywords:
  - microservices
  - production
  - kubernetes
  - azure
  - monitoring
dependencies:
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

### `helm-charts/production-app/values.yaml`
```yaml
# Global settings
global:
  registry: __ACR_NAME__.azurecr.io
  pullPolicy: IfNotPresent
  domain: production.local

# Application metadata
app:
  name: production-app
  version: "2.0.0"
  environment: production

# Redis dependency
redis:
  enabled: true
  auth:
    enabled: true
    password: "redis-secret-password"
  master:
    persistence:
      enabled: true
      size: 8Gi

# API Gateway Service
apiGateway:
  name: api-gateway
  image:
    repository: api-gateway
    tag: latest
  replicaCount: 3
  port: 8080
  resources:
    requests:
      memory: "256Mi"
      cpu: "200m"
    limits:
      memory: "512Mi"
      cpu: "400m"
  service:
    type: ClusterIP
    port: 80
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80

# User Service
userService:
  name: user-service
  image:
    repository: user-service
    tag: latest
  replicaCount: 3
  port: 5000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  service:
    type: ClusterIP
    port: 80
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 15

# Order Service
orderService:
  name: order-service
  image:
    repository: order-service
    tag: latest
  replicaCount: 2
  port: 5000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  service:
    type: ClusterIP
    port: 80
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10

# Frontend
frontend:
  name: frontend
  image:
    repository: frontend
    tag: latest
  replicaCount: 3
  port: 80
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"
    limits:
      memory: "128Mi"
      cpu: "100m"
  service:
    type: ClusterIP
    port: 80

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-rps: "10"
  hosts:
    - host: app.production.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: api-gateway
  tls:
    - secretName: production-app-tls
      hosts:
        - app.production.local

# Security
security:
  podSecurityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  
  containerSecurityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities:
      drop:
        - ALL
  
  networkPolicy:
    enabled: true

# Pod Disruption Budget
podDisruptionBudget:
  enabled: true
  minAvailable: 50%

# Monitoring
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
  prometheusRule:
    enabled: true

# Blue-Green Deployment
blueGreen:
  enabled: false
  productionSlot: blue
  
# Canary Deployment
canary:
  enabled: false
  weight: 10
```

### `helm-charts/production-app/values-staging.yaml`
```yaml
app:
  environment: staging

global:
  domain: staging.local

# Reduced resources for staging
apiGateway:
  replicaCount: 2
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  autoscaling:
    enabled: false

userService:
  replicaCount: 2
  autoscaling:
    enabled: false

orderService:
  replicaCount: 1
  autoscaling:
    enabled: false

frontend:
  replicaCount: 2

# Staging ingress
ingress:
  hosts:
    - host: app.staging.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: api-gateway
  tls:
    - secretName: staging-app-tls
      hosts:
        - app.staging.local

# Disable Redis for staging (use in-memory)
redis:
  enabled: false
```

## ✅ Step 3: Advanced Templates

### `helm-charts/production-app/templates/deployment.yaml`
```yaml
{{- range $service := list "apiGateway" "userService" "orderService" "frontend" }}
{{- $serviceConfig := index $.Values $service }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "production-app.fullname" $ }}-{{ $serviceConfig.name }}
  namespace: {{ $.Release.Namespace }}
  labels:
    {{- include "production-app.labels" $ | nindent 4 }}
    app.kubernetes.io/component: {{ $serviceConfig.name }}
    {{- if $.Values.blueGreen.enabled }}
    deployment-slot: {{ $.Values.blueGreen.productionSlot }}
    {{- end }}
spec:
  {{- if not $serviceConfig.autoscaling.enabled }}
  replicas: {{ $serviceConfig.replicaCount }}
  {{- end }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25%
      maxSurge: 25%
  selector:
    matchLabels:
      {{- include "production-app.selectorLabels" $ | nindent 6 }}
      app.kubernetes.io/component: {{ $serviceConfig.name }}
      {{- if $.Values.blueGreen.enabled }}
      deployment-slot: {{ $.Values.blueGreen.productionSlot }}
      {{- end }}
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "{{ $serviceConfig.port }}"
        prometheus.io/path: "/metrics"
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") $ | sha256sum }}
      labels:
        {{- include "production-app.selectorLabels" $ | nindent 8 }}
        app.kubernetes.io/component: {{ $serviceConfig.name }}
        {{- if $.Values.blueGreen.enabled }}
        deployment-slot: {{ $.Values.blueGreen.productionSlot }}
        {{- end }}
    spec:
      serviceAccountName: {{ include "production-app.serviceAccountName" $ }}
      {{- with $.Values.security.podSecurityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
      - name: {{ $serviceConfig.name }}
        {{- with $.Values.security.containerSecurityContext }}
        securityContext:
          {{- toYaml . | nindent 10 }}
        {{- end }}
        image: {{ include "production-app.image" (dict "Values" $.Values "repository" $serviceConfig.image.repository "tag" $serviceConfig.image.tag) }}
        imagePullPolicy: {{ $.Values.global.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ $serviceConfig.port }}
          protocol: TCP
        {{- if ne $service "frontend" }}
        - name: metrics
          containerPort: 9090
          protocol: TCP
        {{- end }}
        env:
        - name: APP_NAME
          value: {{ $.Values.app.name }}
        - name: APP_VERSION
          value: {{ $.Values.app.version }}
        - name: APP_ENVIRONMENT
          value: {{ $.Values.app.environment }}
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        {{- if and $.Values.redis.enabled (ne $service "frontend") }}
        - name: REDIS_HOST
          value: {{ $.Release.Name }}-redis-master
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ $.Release.Name }}-redis
              key: redis-password
        {{- end }}
        {{- if eq $service "frontend" }}
        - name: API_GATEWAY_URL
          value: "http://{{ include "production-app.fullname" $ }}-{{ $.Values.apiGateway.name }}:{{ $.Values.apiGateway.service.port }}"
        {{- end }}
        {{- if ne $service "frontend" }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        {{- end }}
        resources:
          {{- toYaml $serviceConfig.resources | nindent 10 }}
        {{- if $.Values.security.containerSecurityContext.readOnlyRootFilesystem }}
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: var-cache
          mountPath: /var/cache
        - name: var-run
          mountPath: /var/run
        {{- end }}
      {{- if $.Values.security.containerSecurityContext.readOnlyRootFilesystem }}
      volumes:
      - name: tmp
        emptyDir: {}
      - name: var-cache
        emptyDir: {}
      - name: var-run
        emptyDir: {}
      {{- end }}
      {{- with $.Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with $.Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with $.Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
```

### `helm-charts/production-app/templates/networkpolicy.yaml`
```yaml
{{- if .Values.security.networkPolicy.enabled }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "production-app.fullname" . }}-netpol
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "production-app.labels" . | nindent 4 }}
spec:
  podSelector:
    matchLabels:
      {{- include "production-app.selectorLabels" . | nindent 6 }}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow ingress from ingress controller
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
  # Allow inter-service communication
  - from:
    - podSelector:
        matchLabels:
          {{- include "production-app.selectorLabels" . | nindent 10 }}
  # Allow monitoring
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9090
  egress:
  # Allow DNS
  - to: []
    ports:
    - protocol: UDP
      port: 53
  # Allow HTTPS to external services
  - to: []
    ports:
    - protocol: TCP
      port: 443
  # Allow Redis communication
  {{- if .Values.redis.enabled }}
  - to:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: redis
    ports:
    - protocol: TCP
      port: 6379
  {{- end }}
{{- end }}
```

### `helm-charts/production-app/templates/pdb.yaml`
```yaml
{{- if .Values.podDisruptionBudget.enabled }}
{{- range $service := list "apiGateway" "userService" "orderService" "frontend" }}
{{- $serviceConfig := index $.Values $service }}
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ include "production-app.fullname" $ }}-{{ $serviceConfig.name }}-pdb
  namespace: {{ $.Release.Namespace }}
  labels:
    {{- include "production-app.labels" $ | nindent 4 }}
    app.kubernetes.io/component: {{ $serviceConfig.name }}
spec:
  {{- if $.Values.podDisruptionBudget.minAvailable }}
  minAvailable: {{ $.Values.podDisruptionBudget.minAvailable }}
  {{- end }}
  {{- if $.Values.podDisruptionBudget.maxUnavailable }}
  maxUnavailable: {{ $.Values.podDisruptionBudget.maxUnavailable }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "production-app.selectorLabels" $ | nindent 6 }}
      app.kubernetes.io/component: {{ $serviceConfig.name }}
{{- end }}
{{- end }}
```

## ✅ Step 4: CI/CD Pipeline

### `.github/workflows/helm-ci.yml`
```yaml
name: Helm CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    paths: ['helm-charts/**', 'src/**']
  pull_request:
    branches: [ main ]
    paths: ['helm-charts/**', 'src/**']

env:
  REGISTRY: ${{ secrets.ACR_NAME }}.azurecr.io
  AKS_CLUSTER: ${{ secrets.AKS_CLUSTER_NAME }}
  RESOURCE_GROUP: ${{ secrets.RG_NAME }}

jobs:
  helm-lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Helm
      uses: azure/setup-helm@v3
      with:
        version: '3.12.0'
    
    - name: Helm Lint
      run: |
        helm lint helm-charts/production-app
        echo "✅ Helm chart validation passed"
    
    - name: Helm Template Test
      run: |
        helm template production-app helm-charts/production-app \
          --values helm-charts/production-app/values.yaml \
          --values helm-charts/production-app/values-staging.yaml \
          --output-dir /tmp/helm-test
        
        echo "✅ Helm template rendering successful"
        ls -la /tmp/helm-test/production-app/templates/

  build-images:
    needs: helm-lint
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    strategy:
      matrix:
        service: [api-gateway, user-service, order-service, frontend]
    
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
        docker build -t ${{ env.REGISTRY }}/${{ matrix.service }}:$IMAGE_TAG \
          -t ${{ env.REGISTRY }}/${{ matrix.service }}:latest \
          ./src/${{ matrix.service }}
        
        docker push ${{ env.REGISTRY }}/${{ matrix.service }}:$IMAGE_TAG
        docker push ${{ env.REGISTRY }}/${{ matrix.service }}:latest
        
        echo "IMAGE_TAG=$IMAGE_TAG" >> $GITHUB_ENV
        echo "✅ Built and pushed ${{ matrix.service }}:$IMAGE_TAG"

  deploy-staging:
    needs: [helm-lint, build-images]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
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
    
    - name: Deploy to Staging
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        
        # Update values with new image tags
        sed -i "s/__ACR_NAME__/${{ secrets.ACR_NAME }}/g" helm-charts/production-app/values*.yaml
        
        helm upgrade --install production-app-staging \
          helm-charts/production-app \
          --namespace staging \
          --create-namespace \
          --values helm-charts/production-app/values.yaml \
          --values helm-charts/production-app/values-staging.yaml \
          --set global.imageTag=$IMAGE_TAG \
          --wait \
          --timeout 600s
        
        echo "✅ Deployed to staging with image tag: $IMAGE_TAG"
    
    - name: Run Staging Tests
      run: |
        # Wait for deployment to be ready
        kubectl wait --for=condition=available --timeout=300s \
          deployment -l app.kubernetes.io/instance=production-app-staging -n staging
        
        # Run smoke tests
        echo "🧪 Running staging smoke tests..."
        STAGING_URL=$(kubectl get ingress production-app-staging -n staging -o jsonpath='{.spec.rules[0].host}')
        
        # Test health endpoints
        for service in api-gateway user-service order-service; do
          kubectl port-forward service/production-app-staging-$service 8080:80 -n staging &
          PF_PID=$!
          sleep 5
          
          if curl -f http://localhost:8080/health; then
            echo "✅ $service health check passed"
          else
            echo "❌ $service health check failed"
            exit 1
          fi
          
          kill $PF_PID
        done

  deploy-production:
    needs: deploy-staging
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
    
    - name: Blue-Green Production Deployment
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        
        # Determine current production slot
        CURRENT_SLOT=$(kubectl get deployment -l app.kubernetes.io/instance=production-app-prod -n production -o jsonpath='{.items[0].metadata.labels.deployment-slot}' || echo "blue")
        
        if [ "$CURRENT_SLOT" = "blue" ]; then
          NEW_SLOT="green"
        else
          NEW_SLOT="blue"
        fi
        
        echo "Current slot: $CURRENT_SLOT, Deploying to: $NEW_SLOT"
        
        # Update values with new image tags and slot
        sed -i "s/__ACR_NAME__/${{ secrets.ACR_NAME }}/g" helm-charts/production-app/values*.yaml
        
        # Deploy to new slot
        helm upgrade --install production-app-prod-$NEW_SLOT \
          helm-charts/production-app \
          --namespace production \
          --create-namespace \
          --values helm-charts/production-app/values.yaml \
          --values helm-charts/production-app/values-production.yaml \
          --set global.imageTag=$IMAGE_TAG \
          --set blueGreen.enabled=true \
          --set blueGreen.productionSlot=$NEW_SLOT \
          --wait \
          --timeout 600s
        
        echo "✅ Deployed to production $NEW_SLOT slot"
    
    - name: Production Health Check
      run: |
        # Wait for new deployment
        kubectl wait --for=condition=available --timeout=300s \
          deployment -l deployment-slot=$NEW_SLOT -n production
        
        # Run production smoke tests
        echo "🧪 Running production health checks..."
        
        # Test each service health
        for service in api-gateway user-service order-service; do
          kubectl port-forward service/production-app-prod-$NEW_SLOT-$service 8080:80 -n production &
          PF_PID=$!
          sleep 5
          
          if curl -f http://localhost:8080/health; then
            echo "✅ $service health check passed"
          else
            echo "❌ $service health check failed"
            exit 1
          fi
          
          kill $PF_PID
        done
    
    - name: Switch Traffic to New Slot
      run: |
        # Update ingress to point to new slot
        kubectl patch ingress production-app-prod -n production --type='merge' \
          -p='{"metadata":{"annotations":{"nginx.ingress.kubernetes.io/service-upstream":"production-app-prod-'$NEW_SLOT'-frontend"}}}'
        
        echo "✅ Traffic switched to $NEW_SLOT slot"
        
        # Clean up old slot after successful deployment
        sleep 60
        helm uninstall production-app-prod-$CURRENT_SLOT -n production || true
        
        echo "✅ Blue-green deployment completed successfully"
```

## ✅ Step 5: Deployment Scripts

### `scripts/deploy-production.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Production deployment with Helm"
source .env

ENVIRONMENT=${1:-production}
IMAGE_TAG=${2:-latest}
DEPLOYMENT_STRATEGY=${3:-rolling}

# Connect to AKS
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_CLUSTER_NAME \
  --overwrite-existing

echo "📦 Updating ACR references..."
find helm-charts/production-app -name "*.yaml" -exec sed -i "s/__ACR_NAME__/$ACR_NAME/g" {} \;

echo "🔍 Pre-deployment validation..."
helm lint helm-charts/production-app
helm template production-app-$ENVIRONMENT helm-charts/production-app \
  --values helm-charts/production-app/values.yaml \
  --values helm-charts/production-app/values-$ENVIRONMENT.yaml \
  --set global.imageTag=$IMAGE_TAG > /tmp/production-template.yaml

echo "📊 Creating namespace and deploying..."
kubectl create namespace $ENVIRONMENT --dry-run=client -o yaml | kubectl apply -f -

if [ "$DEPLOYMENT_STRATEGY" = "blue-green" ]; then
  echo "🔄 Blue-Green deployment..."
  ./scripts/blue-green-deploy.sh $ENVIRONMENT $IMAGE_TAG
else
  echo "📈 Rolling deployment..."
  helm upgrade --install production-app-$ENVIRONMENT \
    helm-charts/production-app \
    --namespace $ENVIRONMENT \
    --values helm-charts/production-app/values.yaml \
    --values helm-charts/production-app/values-$ENVIRONMENT.yaml \
    --set global.imageTag=$IMAGE_TAG \
    --wait \
    --timeout 600s
fi

echo "✅ Production deployment completed!"
echo "📊 Status: kubectl get all -n $ENVIRONMENT"
echo "📈 Monitoring: kubectl get servicemonitor -n $ENVIRONMENT"
```

### `scripts/blue-green-deploy.sh`
```bash
#!/bin/bash
set -e

echo "🔄 Blue-Green deployment"
ENVIRONMENT=$1
IMAGE_TAG=$2

# Determine current active slot
CURRENT_SLOT=$(kubectl get deployment -l app.kubernetes.io/instance=production-app-$ENVIRONMENT -n $ENVIRONMENT -o jsonpath='{.items[0].metadata.labels.deployment-slot}' 2>/dev/null || echo "blue")

if [ "$CURRENT_SLOT" = "blue" ]; then
    NEW_SLOT="green"
else
    NEW_SLOT="blue"
fi

echo "Current active slot: $CURRENT_SLOT"
echo "Deploying to slot: $NEW_SLOT"

# Deploy to new slot
helm upgrade --install production-app-$ENVIRONMENT-$NEW_SLOT \
  helm-charts/production-app \
  --namespace $ENVIRONMENT \
  --values helm-charts/production-app/values.yaml \
  --values helm-charts/production-app/values-$ENVIRONMENT.yaml \
  --set global.imageTag=$IMAGE_TAG \
  --set blueGreen.enabled=true \
  --set blueGreen.productionSlot=$NEW_SLOT \
  --wait \
  --timeout 600s

echo "⏳ Running health checks on new slot..."
sleep 30

# Health check new deployment
kubectl wait --for=condition=available --timeout=300s \
  deployment -l deployment-slot=$NEW_SLOT -n $ENVIRONMENT

# Test new slot health
for service in api-gateway user-service order-service; do
    kubectl port-forward service/production-app-$ENVIRONMENT-$NEW_SLOT-$service 8080:80 -n $ENVIRONMENT &
    PF_PID=$!
    sleep 5
    
    if curl -f http://localhost:8080/health; then
        echo "✅ $service health check passed"
    else
        echo "❌ $service health check failed"
        kill $PF_PID
        exit 1
    fi
    
    kill $PF_PID
done

echo "🔀 Switching traffic to new slot..."
# Update ingress to point to new slot
kubectl patch ingress production-app-$ENVIRONMENT -n $ENVIRONMENT --type='merge' \
  -p='{"spec":{"rules":[{"host":"app.'$ENVIRONMENT'.local","http":{"paths":[{"path":"/","pathType":"Prefix","backend":{"service":{"name":"production-app-'$ENVIRONMENT'-'$NEW_SLOT'-frontend","port":{"number":80}}}}]}}]}}'

echo "⏳ Monitoring new slot for 60 seconds..."
sleep 60

echo "🧹 Cleaning up old slot..."
helm uninstall production-app-$ENVIRONMENT-$CURRENT_SLOT -n $ENVIRONMENT || true

echo "✅ Blue-green deployment completed successfully!"
echo "🎯 Active slot: $NEW_SLOT"
```

## ✅ Step 6: Deploy & Monitor

### Setup Infrastructure
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Setup infrastructure
./scripts/setup-infrastructure.sh
```

### Deploy Application
```bash
# Deploy to staging
./scripts/deploy-production.sh staging v1.0.0

# Deploy to production with blue-green
./scripts/deploy-production.sh production v1.0.0 blue-green
```

### Monitor Deployment
```bash
# Check all resources
kubectl get all -n production

# Check ingress
kubectl get ingress -n production

# Check HPA
kubectl get hpa -n production

# Check PDB
kubectl get pdb -n production

# View logs
kubectl logs -l app.kubernetes.io/instance=production-app-prod -n production
```

### Access Monitoring
```bash
source .env

echo "📊 Grafana: http://$INGRESS_IP/grafana"
echo "📈 Prometheus: http://$INGRESS_IP/prometheus"
echo "🌐 Application: http://$INGRESS_IP"
```

## 🎓 Complete

### What You Built
✅ **Production Infrastructure** - NGINX Ingress, Cert-Manager, Prometheus, Grafana
✅ **Advanced Helm Charts** - Multi-environment, blue-green deployments, monitoring
✅ **Security Hardening** - Network policies, security contexts, PDBs
✅ **CI/CD Pipeline** - Automated testing, building, and deployment
✅ **Monitoring Stack** - Prometheus metrics, Grafana dashboards
✅ **Production Features** - Auto-scaling, health checks, rolling updates

### Key Skills Learned
- Production-ready Kubernetes architecture design
- Advanced Helm templating and deployment strategies
- CI/CD pipeline automation with GitHub Actions
- Blue-green and canary deployment patterns
- Kubernetes security best practices
- Infrastructure as Code with Helm charts
- Monitoring and observability implementation

### Production Readiness Checklist
- ✅ High availability with multiple replicas
- ✅ Auto-scaling based on CPU/memory metrics
- ✅ Rolling updates with zero downtime
- ✅ Health checks and readiness probes
- ✅ Resource limits and requests
- ✅ Security hardening and network policies
- ✅ TLS termination and certificate management
- ✅ Monitoring and alerting
- ✅ Backup and disaster recovery planning
