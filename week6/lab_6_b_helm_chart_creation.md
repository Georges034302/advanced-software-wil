# ⛵ Lab 6B: Helm Chart Creation & Application Packaging

## 🎯 Objective
Create production-ready Helm charts to package and deploy applications with templating, configuration management, and environment-specific values.

- Understand Helm architecture and templating
- Create custom Helm charts with values.yaml configuration
- Use Helm CLI for chart development and testing
- Implement template functions and conditionals
- Deploy multi-environment applications with Helm

## 🗂 Structure
```
lab6b/
├── helm-charts/
│   └── microservices-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── configmap.yaml
│           ├── ingress.yaml
│           ├── _helpers.tpl
│           └── NOTES.txt
├── scripts/
│   ├── create-helm-chart.sh
│   ├── deploy-with-helm.sh
│   └── test-helm-chart.sh
└── .env (from Lab 6A)
```

## ✅ Step 1: Create Helm Chart Structure

### `scripts/create-helm-chart.sh`
```bash
#!/bin/bash
set -e

echo "⛵ Creating Helm chart structure"
source .env

CHART_NAME="microservices-app"
CHART_VERSION="1.0.0"

echo "📦 Initializing Helm chart..."
mkdir -p helm-charts
cd helm-charts

# Create basic chart structure
helm create $CHART_NAME

# Remove default files we'll replace
rm -f $CHART_NAME/templates/deployment.yaml
rm -f $CHART_NAME/templates/service.yaml
rm -f $CHART_NAME/templates/ingress.yaml
rm -f $CHART_NAME/values.yaml

echo "✅ Helm chart structure created: helm-charts/$CHART_NAME"
```

### `helm-charts/microservices-app/Chart.yaml`
```yaml
apiVersion: v2
name: microservices-app
description: A Helm chart for microservices application deployment
type: application
version: 1.0.0
appVersion: "1.0.0"
home: https://github.com/your-org/microservices-app
sources:
  - https://github.com/your-org/microservices-app
maintainers:
  - name: Lab Student
    email: student@example.com
keywords:
  - microservices
  - flask
  - kubernetes
  - azure
annotations:
  category: Application
dependencies: []
```

### `helm-charts/microservices-app/values.yaml`
```yaml
# Default values for microservices-app
# This is a YAML-formatted file

# Global settings
global:
  registry: __ACR_NAME__.azurecr.io
  pullPolicy: IfNotPresent
  namespace: microservices

# Application configuration
app:
  name: microservices-app
  version: "1.0.0"
  environment: development

# Dice Service configuration
diceService:
  name: dice-service
  image:
    repository: dice-service
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
    targetCPUUtilizationPercentage: 70

# Color Service configuration
colorService:
  name: color-service
  image:
    repository: color-service
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
    maxReplicas: 8
    targetCPUUtilizationPercentage: 70

# Frontend configuration
frontend:
  name: frontend
  image:
    repository: frontend
    tag: latest
  replicaCount: 2
  port: 80
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"
    limits:
      memory: "128Mi"
      cpu: "100m"
  service:
    type: LoadBalancer
    port: 80
  autoscaling:
    enabled: false

# Ingress configuration
ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  hosts:
    - host: microservices.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api/dice
          pathType: Prefix
          service: dice-service
        - path: /api/color
          pathType: Prefix
          service: color-service
  tls: []

# ConfigMap data
config:
  dice:
    maxSides: "100"
    defaultSides: "6"
    enableStats: "true"
  color:
    defaultTheme: "ocean"
    maxPaletteSize: "10"
    enableCustomThemes: "true"
  frontend:
    title: "Microservices Dashboard"
    theme: "dark"
    apiTimeout: "5000"

# Security context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000

# Pod security context
podSecurityContext: {}

# Node selector
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity: {}
```

### `helm-charts/microservices-app/values-dev.yaml`
```yaml
# Development environment values
global:
  namespace: microservices-dev

app:
  environment: development

# Lower resource requirements for dev
diceService:
  replicaCount: 1
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"
    limits:
      memory: "128Mi"
      cpu: "100m"
  autoscaling:
    enabled: false

colorService:
  replicaCount: 1
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"
    limits:
      memory: "128Mi"
      cpu: "100m"
  autoscaling:
    enabled: false

frontend:
  replicaCount: 1
  resources:
    requests:
      memory: "32Mi"
      cpu: "25m"
    limits:
      memory: "64Mi"
      cpu: "50m"

# Development ingress
ingress:
  enabled: true
  hosts:
    - host: microservices-dev.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api/dice
          pathType: Prefix
          service: dice-service
        - path: /api/color
          pathType: Prefix
          service: color-service

# Development config
config:
  dice:
    enableStats: "true"
    debugMode: "true"
  color:
    enableCustomThemes: "true"
    debugMode: "true"
  frontend:
    title: "Microservices Dashboard - DEV"
    theme: "dark"
    debugMode: "true"
```

### `helm-charts/microservices-app/values-prod.yaml`
```yaml
# Production environment values
global:
  namespace: microservices-prod

app:
  environment: production

# Higher resource requirements for production
diceService:
  replicaCount: 3
  resources:
    requests:
      memory: "256Mi"
      cpu: "200m"
    limits:
      memory: "512Mi"
      cpu: "400m"
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 15
    targetCPUUtilizationPercentage: 60

colorService:
  replicaCount: 3
  resources:
    requests:
      memory: "256Mi"
      cpu: "200m"
    limits:
      memory: "512Mi"
      cpu: "400m"
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 12
    targetCPUUtilizationPercentage: 60

frontend:
  replicaCount: 3
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"

# Production ingress with TLS
ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: microservices.production.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api/dice
          pathType: Prefix
          service: dice-service
        - path: /api/color
          pathType: Prefix
          service: color-service
  tls:
    - secretName: microservices-tls
      hosts:
        - microservices.production.com

# Production config
config:
  dice:
    enableStats: "true"
    debugMode: "false"
  color:
    enableCustomThemes: "true"
    debugMode: "false"
  frontend:
    title: "Microservices Dashboard"
    theme: "light"
    debugMode: "false"

# Security hardening for production
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  readOnlyRootFilesystem: true

podSecurityContext:
  seccompProfile:
    type: RuntimeDefault
```

## ✅ Step 2: Create Helm Templates

### `helm-charts/microservices-app/templates/_helpers.tpl`
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "microservices-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "microservices-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "microservices-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "microservices-app.labels" -}}
helm.sh/chart: {{ include "microservices-app.chart" . }}
{{ include "microservices-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: {{ include "microservices-app.name" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "microservices-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "microservices-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create image name
*/}}
{{- define "microservices-app.image" -}}
{{- $registry := .Values.global.registry -}}
{{- $repository := .repository -}}
{{- $tag := .tag | default "latest" -}}
{{- printf "%s/%s:%s" $registry $repository $tag }}
{{- end }}

{{/*
Create service name
*/}}
{{- define "microservices-app.serviceName" -}}
{{- printf "%s-%s" (include "microservices-app.fullname" .) .serviceName }}
{{- end }}
```

### `helm-charts/microservices-app/templates/configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "microservices-app.fullname" . }}-config
  namespace: {{ .Values.global.namespace }}
  labels:
    {{- include "microservices-app.labels" . | nindent 4 }}
data:
  # Dice Service Configuration
  dice.max.sides: {{ .Values.config.dice.maxSides | quote }}
  dice.default.sides: {{ .Values.config.dice.defaultSides | quote }}
  dice.enable.stats: {{ .Values.config.dice.enableStats | quote }}
  {{- if .Values.config.dice.debugMode }}
  dice.debug.mode: {{ .Values.config.dice.debugMode | quote }}
  {{- end }}
  
  # Color Service Configuration
  color.default.theme: {{ .Values.config.color.defaultTheme | quote }}
  color.max.palette.size: {{ .Values.config.color.maxPaletteSize | quote }}
  color.enable.custom.themes: {{ .Values.config.color.enableCustomThemes | quote }}
  {{- if .Values.config.color.debugMode }}
  color.debug.mode: {{ .Values.config.color.debugMode | quote }}
  {{- end }}
  
  # Frontend Configuration
  frontend.title: {{ .Values.config.frontend.title | quote }}
  frontend.theme: {{ .Values.config.frontend.theme | quote }}
  frontend.api.timeout: {{ .Values.config.frontend.apiTimeout | quote }}
  {{- if .Values.config.frontend.debugMode }}
  frontend.debug.mode: {{ .Values.config.frontend.debugMode | quote }}
  {{- end }}
  
  # Application Configuration
  app.name: {{ .Values.app.name | quote }}
  app.version: {{ .Values.app.version | quote }}
  app.environment: {{ .Values.app.environment | quote }}
```

### `helm-charts/microservices-app/templates/deployment.yaml`
```yaml
{{- range $service := list "diceService" "colorService" "frontend" }}
{{- $serviceConfig := index $.Values $service }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "microservices-app.fullname" $ }}-{{ $serviceConfig.name }}
  namespace: {{ $.Values.global.namespace }}
  labels:
    {{- include "microservices-app.labels" $ | nindent 4 }}
    app.kubernetes.io/component: {{ $serviceConfig.name }}
spec:
  {{- if not $serviceConfig.autoscaling.enabled }}
  replicas: {{ $serviceConfig.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "microservices-app.selectorLabels" $ | nindent 6 }}
      app.kubernetes.io/component: {{ $serviceConfig.name }}
  template:
    metadata:
      labels:
        {{- include "microservices-app.selectorLabels" $ | nindent 8 }}
        app.kubernetes.io/component: {{ $serviceConfig.name }}
    spec:
      {{- with $.Values.securityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
      - name: {{ $serviceConfig.name }}
        {{- if $.Values.podSecurityContext }}
        securityContext:
          {{- toYaml $.Values.podSecurityContext | nindent 10 }}
        {{- end }}
        image: {{ include "microservices-app.image" (dict "Values" $.Values "repository" $serviceConfig.image.repository "tag" $serviceConfig.image.tag) }}
        imagePullPolicy: {{ $.Values.global.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ $serviceConfig.port }}
          protocol: TCP
        env:
        - name: APP_NAME
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: app.name
        - name: APP_VERSION
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: app.version
        - name: APP_ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: app.environment
        {{- if eq $service "diceService" }}
        - name: MAX_SIDES
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: dice.max.sides
        - name: DEFAULT_SIDES
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: dice.default.sides
        {{- end }}
        {{- if eq $service "colorService" }}
        - name: DEFAULT_THEME
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: color.default.theme
        - name: MAX_PALETTE_SIZE
          valueFrom:
            configMapKeyRef:
              name: {{ include "microservices-app.fullname" $ }}-config
              key: color.max.palette.size
        {{- end }}
        {{- if eq $service "frontend" }}
        - name: DICE_SERVICE_URL
          value: "http://{{ include "microservices-app.fullname" $ }}-{{ $.Values.diceService.name }}:{{ $.Values.diceService.service.port }}"
        - name: COLOR_SERVICE_URL
          value: "http://{{ include "microservices-app.fullname" $ }}-{{ $.Values.colorService.name }}:{{ $.Values.colorService.service.port }}"
        {{- end }}
        {{- if ne $service "frontend" }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        {{- end }}
        resources:
          {{- toYaml $serviceConfig.resources | nindent 10 }}
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

### `helm-charts/microservices-app/templates/service.yaml`
```yaml
{{- range $service := list "diceService" "colorService" "frontend" }}
{{- $serviceConfig := index $.Values $service }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ include "microservices-app.fullname" $ }}-{{ $serviceConfig.name }}
  namespace: {{ $.Values.global.namespace }}
  labels:
    {{- include "microservices-app.labels" $ | nindent 4 }}
    app.kubernetes.io/component: {{ $serviceConfig.name }}
spec:
  type: {{ $serviceConfig.service.type }}
  ports:
  - port: {{ $serviceConfig.service.port }}
    targetPort: http
    protocol: TCP
    name: http
  selector:
    {{- include "microservices-app.selectorLabels" $ | nindent 4 }}
    app.kubernetes.io/component: {{ $serviceConfig.name }}
{{- end }}
```

### `helm-charts/microservices-app/templates/ingress.yaml`
```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "microservices-app.fullname" . }}-ingress
  namespace: {{ .Values.global.namespace }}
  labels:
    {{- include "microservices-app.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "microservices-app.fullname" $ }}-{{ .service }}
                port:
                  number: 80
          {{- end }}
    {{- end }}
{{- end }}
```

### `helm-charts/microservices-app/templates/hpa.yaml`
```yaml
{{- range $service := list "diceService" "colorService" }}
{{- $serviceConfig := index $.Values $service }}
{{- if $serviceConfig.autoscaling.enabled }}
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "microservices-app.fullname" $ }}-{{ $serviceConfig.name }}-hpa
  namespace: {{ $.Values.global.namespace }}
  labels:
    {{- include "microservices-app.labels" $ | nindent 4 }}
    app.kubernetes.io/component: {{ $serviceConfig.name }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "microservices-app.fullname" $ }}-{{ $serviceConfig.name }}
  minReplicas: {{ $serviceConfig.autoscaling.minReplicas }}
  maxReplicas: {{ $serviceConfig.autoscaling.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ $serviceConfig.autoscaling.targetCPUUtilizationPercentage }}
{{- end }}
{{- end }}
```

### `helm-charts/microservices-app/templates/NOTES.txt`
```
🎉 {{ .Chart.Name }} has been deployed successfully!

🏷️  Release Name: {{ .Release.Name }}
📦 Namespace: {{ .Values.global.namespace }}
🌍 Environment: {{ .Values.app.environment }}

📊 Deployed Services:
{{- range $service := list "diceService" "colorService" "frontend" }}
{{- $serviceConfig := index $.Values $service }}
  • {{ $serviceConfig.name }}: {{ $serviceConfig.replicaCount }} replica(s)
{{- end }}

🌐 Access Information:
{{- if .Values.ingress.enabled }}
{{- range $host := .Values.ingress.hosts }}
  External URL: http://{{ $host.host }}
{{- end }}
{{- else }}
{{- if eq .Values.frontend.service.type "LoadBalancer" }}
  Get external IP: kubectl get service {{ include "microservices-app.fullname" . }}-{{ .Values.frontend.name }} -n {{ .Values.global.namespace }}
{{- else }}
  Port forward: kubectl port-forward service/{{ include "microservices-app.fullname" . }}-{{ .Values.frontend.name }} 8080:80 -n {{ .Values.global.namespace }}
  Local URL: http://localhost:8080
{{- end }}
{{- end }}

🔍 Monitoring Commands:
  kubectl get all -n {{ .Values.global.namespace }}
  kubectl logs -l app.kubernetes.io/instance={{ .Release.Name }} -n {{ .Values.global.namespace }}
  
🔧 Management Commands:
  helm status {{ .Release.Name }}
  helm upgrade {{ .Release.Name }} ./helm-charts/microservices-app
  helm rollback {{ .Release.Name }} <revision>
  helm uninstall {{ .Release.Name }}

{{ if .Values.app.environment eq "development" }}
🚧 Development Environment Notes:
  - Lower resource allocation for cost optimization
  - Debug mode enabled for troubleshooting
  - Autoscaling disabled for predictable resource usage
{{- end }}

{{ if .Values.app.environment eq "production" }}
🔒 Production Environment Notes:
  - High availability with multiple replicas
  - Autoscaling enabled for performance
  - Security hardening applied
  - TLS termination configured
{{- end }}
```

## ✅ Step 3: Deployment Scripts

### `scripts/deploy-with-helm.sh`
```bash
#!/bin/bash
set -e

echo "⛵ Deploying with Helm"
source .env

ENVIRONMENT=${1:-dev}
RELEASE_NAME="microservices-$ENVIRONMENT"

# Ensure we're connected to AKS
az aks get-credentials \
  --resource-group $RG_NAME \
  --name $AKS_CLUSTER_NAME \
  --overwrite-existing

echo "📦 Updating ACR name in values..."
find helm-charts/microservices-app -name "*.yaml" -exec sed -i "s/__ACR_NAME__/$ACR_NAME/g" {} \;

echo "📝 Creating namespace..."
kubectl create namespace microservices-$ENVIRONMENT --dry-run=client -o yaml | kubectl apply -f -

echo "🔍 Validating Helm chart..."
helm lint helm-charts/microservices-app

echo "🎯 Installing/upgrading with Helm (Environment: $ENVIRONMENT)..."
helm upgrade --install $RELEASE_NAME \
  helm-charts/microservices-app \
  --namespace microservices-$ENVIRONMENT \
  --values helm-charts/microservices-app/values.yaml \
  --values helm-charts/microservices-app/values-$ENVIRONMENT.yaml \
  --wait \
  --timeout 300s

echo "📊 Checking deployment status..."
kubectl get all -n microservices-$ENVIRONMENT

echo "⏳ Waiting for external IP (if LoadBalancer)..."
timeout=300
while [ $timeout -gt 0 ]; do
    EXTERNAL_IP=$(kubectl get service $RELEASE_NAME-frontend -n microservices-$ENVIRONMENT -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [ -n "$EXTERNAL_IP" ] && [ "$EXTERNAL_IP" != "null" ]; then
        echo "✅ External IP: $EXTERNAL_IP"
        break
    fi
    echo "Waiting for external IP..."
    sleep 10
    ((timeout-=10))
done

echo ""
echo "✅ Helm deployment complete!"
echo "📦 Release: $RELEASE_NAME"
echo "🌍 Environment: $ENVIRONMENT"
echo "📋 Status: helm status $RELEASE_NAME -n microservices-$ENVIRONMENT"
```

### `scripts/test-helm-chart.sh`
```bash
#!/bin/bash
set -e

echo "🧪 Testing Helm chart"
source .env

ENVIRONMENT=${1:-dev}
RELEASE_NAME="microservices-$ENVIRONMENT"

echo "🔍 Chart validation..."
helm lint helm-charts/microservices-app

echo "📋 Dry run installation..."
helm install $RELEASE_NAME-test \
  helm-charts/microservices-app \
  --namespace microservices-$ENVIRONMENT \
  --values helm-charts/microservices-app/values.yaml \
  --values helm-charts/microservices-app/values-$ENVIRONMENT.yaml \
  --dry-run \
  --debug

echo "🎯 Template rendering test..."
helm template $RELEASE_NAME \
  helm-charts/microservices-app \
  --values helm-charts/microservices-app/values.yaml \
  --values helm-charts/microservices-app/values-$ENVIRONMENT.yaml \
  --output-dir /tmp/helm-output

echo "📁 Generated templates saved to: /tmp/helm-output"
echo "🔍 Review templates: ls -la /tmp/helm-output/microservices-app/templates/"

echo ""
echo "✅ Helm chart tests completed!"
echo "📝 Review output and deploy with: ./scripts/deploy-with-helm.sh $ENVIRONMENT"
```

## ✅ Step 4: Deploy & Test

### Create Helm Chart
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Create initial chart structure
./scripts/create-helm-chart.sh
```

### Test Helm Chart
```bash
# Test chart validation and rendering
./scripts/test-helm-chart.sh dev

# Review generated templates
ls -la /tmp/helm-output/microservices-app/templates/
cat /tmp/helm-output/microservices-app/templates/deployment.yaml
```

### Deploy with Helm
```bash
# Deploy to development environment
./scripts/deploy-with-helm.sh dev

# Check Helm releases
helm list -A

# Get release status
helm status microservices-dev -n microservices-dev
```

## ✅ Step 5: Helm Operations

### Upgrade Deployment
```bash
# Modify values and upgrade
helm upgrade microservices-dev \
  helm-charts/microservices-app \
  --namespace microservices-dev \
  --values helm-charts/microservices-app/values.yaml \
  --values helm-charts/microservices-app/values-dev.yaml

# Check upgrade history
helm history microservices-dev -n microservices-dev
```

### Multi-Environment Deployment
```bash
# Deploy to production (if values-prod.yaml is ready)
./scripts/deploy-with-helm.sh prod

# Compare environments
kubectl get all -n microservices-dev
kubectl get all -n microservices-prod
```

### Rollback
```bash
# Rollback to previous version
helm rollback microservices-dev 1 -n microservices-dev

# Verify rollback
helm history microservices-dev -n microservices-dev
```

### Get Values
```bash
# Get current values
helm get values microservices-dev -n microservices-dev

# Get all values (including defaults)
helm get values microservices-dev -n microservices-dev --all
```

## ✅ Step 6: Testing & Validation

### Test Application
```bash
# Get external IP
EXTERNAL_IP=$(kubectl get service microservices-dev-frontend -n microservices-dev -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Test services
curl http://$EXTERNAL_IP/
curl http://$EXTERNAL_IP/api/dice/
curl http://$EXTERNAL_IP/api/color/

# Test autoscaling (if enabled)
kubectl get hpa -n microservices-dev
```

### Cleanup
```bash
# Uninstall Helm release
helm uninstall microservices-dev -n microservices-dev

# Delete namespace
kubectl delete namespace microservices-dev
```

## 🎓 Complete

### What You Built
✅ **Production Helm Chart** - Complete templating with values management
✅ **Multi-Environment Support** - Dev/prod configurations with different resource allocations
✅ **Template Functions** - Advanced Helm templating with helpers and conditionals
✅ **Configuration Management** - Environment-specific ConfigMaps and settings
✅ **Auto-scaling Integration** - HPA templates for production workloads
✅ **Ingress Configuration** - Load balancing and routing templates

### Key Skills Learned
- Helm chart architecture and best practices
- YAML templating with Go template functions
- Values.yaml hierarchy and environment-specific overrides
- Helm CLI operations: install, upgrade, rollback, test
- Template debugging and validation techniques
- Multi-environment deployment strategies

### Next Steps (Lab 6C Preview)
- Production ingress controllers and TLS
- Advanced monitoring and observability
- Blue-green and canary deployments
- GitOps integration with Helm and GitHub Actions
