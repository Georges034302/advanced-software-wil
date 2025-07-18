# ⛵ Lab 6B: Helm Chart Creation & Templating

## 🎯 Objective
Create a simple Helm chart to package and deploy the Flask applications from Lab 6A with templating and environment-specific values.

- Convert Lab 6A deployments to Helm chart
- Use Helm templating for configuration management
- Deploy with different environment values (dev/prod)
- Understand Helm chart structure and operations

## 🗂 Structure
```
lab6b/
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── _helpers.tpl
├── deploy-helm.sh
└── .env (from Lab 6A)
```

## ✅ Step 1: Create Helm Chart Structure

### Create Chart Directory
```bash
mkdir -p helm-chart/templates
cd helm-chart
```

### `Chart.yaml`
```yaml
apiVersion: v2
name: flask-apps
description: Simple Flask applications Helm chart
type: application
version: 1.0.0
appVersion: "1.0.0"
```

### `values.yaml`
```yaml
# Default values
global:
  registry: __ACR_NAME__.azurecr.io

app1:
  name: app1
  image: app1:latest
  replicas: 2
  port: 5000

app2:
  name: app2
  image: app2:latest
  replicas: 2
  port: 5000

service:
  type: LoadBalancer
  port: 80

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### `values-dev.yaml`
```yaml
# Development environment
app1:
  replicas: 1
app2:
  replicas: 1

resources:
  requests:
    memory: "64Mi"
    cpu: "50m"
  limits:
    memory: "128Mi"
    cpu: "100m"
```

### `values-prod.yaml`
```yaml
# Production environment
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
```

## ✅ Step 2: Create Helm Templates

### `templates/_helpers.tpl`
```yaml
{{/*
Chart name
*/}}
{{- define "flask-apps.name" -}}
{{- .Chart.Name }}
{{- end }}

{{/*
Full name
*/}}
{{- define "flask-apps.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "flask-apps.labels" -}}
app.kubernetes.io/name: {{ include "flask-apps.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

### `templates/deployment.yaml`
```yaml
{{- range $app := list "app1" "app2" }}
{{- $config := index $.Values $app }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "flask-apps.fullname" $ }}-{{ $config.name }}
  labels:
    {{- include "flask-apps.labels" $ | nindent 4 }}
    app: {{ $config.name }}
spec:
  replicas: {{ $config.replicas }}
  selector:
    matchLabels:
      app: {{ $config.name }}
  template:
    metadata:
      labels:
        app: {{ $config.name }}
    spec:
      containers:
      - name: {{ $config.name }}
        image: {{ $.Values.global.registry }}/{{ $config.image }}
        ports:
        - containerPort: {{ $config.port }}
        resources:
          {{- toYaml $.Values.resources | nindent 10 }}
        livenessProbe:
          httpGet:
            path: /health
            port: {{ $config.port }}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: {{ $config.port }}
          initialDelaySeconds: 5
          periodSeconds: 5
{{- end }}
```

### `templates/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "flask-apps.fullname" . }}-service
  labels:
    {{- include "flask-apps.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: {{ .Values.app1.port }}
    protocol: TCP
  selector:
    app: app1  # Load balances to both apps via shared label
---
apiVersion: v1
kind: Service
metadata:
  name: {{ include "flask-apps.fullname" . }}-service-lb
  labels:
    {{- include "flask-apps.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: {{ .Values.app1.port }}
    protocol: TCP
  selector:
    app.kubernetes.io/name: {{ include "flask-apps.name" . }}
```

## ✅ Step 3: Deploy with Helm

### `deploy-helm.sh`
```bash
#!/bin/bash

echo "⛵ Deploying Flask apps with Helm..."
source .env

ENV=${1:-dev}
RELEASE_NAME="flask-apps-$ENV"

# Replace ACR name in values
sed -i "s/__ACR_NAME__/$ACR_NAME/g" helm-chart/values.yaml

# Deploy with Helm
helm upgrade --install $RELEASE_NAME helm-chart/ \
  --values helm-chart/values.yaml \
  --values helm-chart/values-$ENV.yaml \
  --wait \
  --timeout 300s

# Get service info
kubectl get all -l app.kubernetes.io/instance=$RELEASE_NAME

echo "✅ Helm deployment complete!"
echo "📋 Status: helm status $RELEASE_NAME"
```

### Deploy & Test
```bash
# Make script executable
chmod +x deploy-helm.sh

# Deploy to development
./deploy-helm.sh dev

# Check Helm release
helm list
helm status flask-apps-dev

# Test the application
kubectl get service
EXTERNAL_IP=$(kubectl get service flask-apps-dev-flask-apps-service-lb -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl http://$EXTERNAL_IP/
```

## ✅ Step 4: Helm Operations

### Environment Switching
```bash
# Deploy to production
./deploy-helm.sh prod

# Compare environments
helm get values flask-apps-dev
helm get values flask-apps-prod

# Check resource differences
kubectl get pods -l app.kubernetes.io/name=flask-apps
```

### Upgrade & Rollback
```bash
# Modify values and upgrade
helm upgrade flask-apps-dev helm-chart/ \
  --values helm-chart/values.yaml \
  --values helm-chart/values-dev.yaml

# Check history
helm history flask-apps-dev

# Rollback if needed
helm rollback flask-apps-dev 1

# Verify rollback
helm history flask-apps-dev
```

### Cleanup
```bash
# Uninstall Helm releases
helm uninstall flask-apps-dev
helm uninstall flask-apps-prod

# Verify cleanup
helm list
kubectl get all
```

## 🎓 Lab Complete

### What You Built
✅ **Simple Helm Chart** - Templated Flask app deployments  
✅ **Environment Values** - Dev/prod configurations with different resources  
✅ **Helm Operations** - Install, upgrade, rollback, and uninstall  
✅ **Template Functions** - Basic Helm templating with helpers  
✅ **Configuration Management** - Values-driven deployment customization  

### Key Skills Learned
- Helm chart structure and templating basics
- Values.yaml hierarchy and environment overrides
- Helm CLI operations for deployment management
- Template debugging and chart development
- Multi-environment deployment with shared charts

### Helm Benefits Over Raw YAML
- **Templating**: One chart, multiple environments
- **Values Management**: Configuration without changing templates
- **Release Management**: Track deployments, upgrades, rollbacks
- **Package Management**: Reusable, shareable charts

### Next Steps (Lab 6C Preview)
In the next lab, you'll add production features like ingress controllers, monitoring, and CI/CD pipelines to your Helm deployments.
