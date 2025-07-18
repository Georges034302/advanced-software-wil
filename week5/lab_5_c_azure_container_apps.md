# ☁️ Lab 5C: Scale with Azure Container Apps

## 🎯 Objective
Deploy and scale containerized Flask app using Azure Container Apps for production-ready hosting.

- Deploy containers to Azure Container Apps with auto-scaling
- Configure ingress and traffic management
- Implement zero-downtime deployments with revisions
- Monitor application performance and scaling events
- Set up environment variables and secrets

## 🗂 Structure
```
lab5c/
├── scripts/
│   ├── deploy-containerapp.sh
│   ├── scale-containerapp.sh
│   └── cleanup-containerapp.sh
└── .env (from Lab 5A)
```

## ✅ Step 1: Container Apps Environment

### `scripts/deploy-containerapp.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying to Azure Container Apps"
source .env

# Container Apps environment name
CONTAINERAPP_ENV="containerapp-env-lab5c"
CONTAINERAPP_NAME="containerapp-lab5c-$(date +%s)"

# Create Container Apps environment
echo "📦 Creating Container Apps environment..."
az containerapp env create \
  --name $CONTAINERAPP_ENV \
  --resource-group $RG_NAME \
  --location $LOCATION

# Create the container app
echo "🐳 Creating Container App..."
az containerapp create \
  --name $CONTAINERAPP_NAME \
  --resource-group $RG_NAME \
  --environment $CONTAINERAPP_ENV \
  --image $ACR_NAME.azurecr.io/acr-lab:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 5000 \
  --ingress external \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 10

# Get the app URL
CONTAINERAPP_URL=$(az containerapp show \
  --name $CONTAINERAPP_NAME \
  --resource-group $RG_NAME \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

# Save to environment
echo "export CONTAINERAPP_ENV=$CONTAINERAPP_ENV" >> .env
echo "export CONTAINERAPP_NAME=$CONTAINERAPP_NAME" >> .env
echo "export CONTAINERAPP_URL=$CONTAINERAPP_URL" >> .env

# Store in GitHub secrets
if command -v gh &> /dev/null; then
    gh auth logout --hostname github.com || true
    
    if [[ -n "$GITHUB_TOKEN" ]]; then
        echo "$GITHUB_TOKEN" | gh auth login --with-token --hostname github.com
        echo "$CONTAINERAPP_NAME" | gh secret set CONTAINERAPP_NAME
        echo "$CONTAINERAPP_URL" | gh secret set CONTAINERAPP_URL
        echo "✅ Container App details stored in GitHub secrets"
    else
        echo "⚠️ GITHUB_TOKEN not found - skipping secret storage"
    fi
fi

echo ""
echo "✅ Container App deployment complete!"
echo "🌐 Access your app: https://$CONTAINERAPP_URL"
```

### `scripts/scale-containerapp.sh`
```bash
#!/bin/bash
set -e

echo "📈 Scaling Container App"
source .env

# Update scaling configuration
az containerapp update \
  --name $CONTAINERAPP_NAME \
  --resource-group $RG_NAME \
  --min-replicas 2 \
  --max-replicas 20 \
  --scale-rule-name "http-rule" \
  --scale-rule-type "http" \
  --scale-rule-http-concurrency 10

echo "✅ Container App scaling updated"
echo "📊 Min replicas: 2, Max replicas: 20"
echo "🎯 Scale trigger: 10 concurrent requests per replica"
```

### `scripts/cleanup-containerapp.sh`
```bash
#!/bin/bash
set -e

echo "🧹 Cleaning up Container Apps resources"
source .env

if [[ -n "$CONTAINERAPP_NAME" ]]; then
    az containerapp delete \
      --name $CONTAINERAPP_NAME \
      --resource-group $RG_NAME \
      --yes
    echo "✅ Container App deleted: $CONTAINERAPP_NAME"
fi

if [[ -n "$CONTAINERAPP_ENV" ]]; then
    az containerapp env delete \
      --name $CONTAINERAPP_ENV \
      --resource-group $RG_NAME \
      --yes
    echo "✅ Container Apps environment deleted: $CONTAINERAPP_ENV"
fi
```

### Run Deployment
```bash
chmod +x scripts/*.sh
./scripts/deploy-containerapp.sh
```

## ✅ Step 2: Monitor & Test

### Check Status
```bash
source .env

# View Container App status
az containerapp show --name $CONTAINERAPP_NAME --resource-group $RG_NAME --query properties.provisioningState

# Check revisions
az containerapp revision list --name $CONTAINERAPP_NAME --resource-group $RG_NAME --output table

# Monitor replicas
az containerapp replica list --name $CONTAINERAPP_NAME --resource-group $RG_NAME --output table
```

### Test Endpoints
```bash
source .env

# Test root endpoint
curl https://$CONTAINERAPP_URL/

# Test health endpoint
curl https://$CONTAINERAPP_URL/health

# Load test to trigger scaling
for i in {1..50}; do
  curl https://$CONTAINERAPP_URL/ &
done
wait
```

### Check Scaling
```bash
# Monitor scaling events
az containerapp replica list --name $CONTAINERAPP_NAME --resource-group $RG_NAME

# View logs
az containerapp logs show --name $CONTAINERAPP_NAME --resource-group $RG_NAME
```

## ✅ Step 3: CI/CD Deployment

### `.github/workflows/deploy-containerapp.yml`
```yaml
name: Deploy to Container Apps

on:
  workflow_run:
    workflows: ["Build and Push"]
    types:
      - completed

jobs:
  deploy-containerapp:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
    - uses: actions/checkout@v4
    
    - name: Login to GitHub CLI
      run: echo "${{ secrets.GITHUB_TOKEN }}" | gh auth login --with-token
    
    - uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Update Container App
      run: |
        source .env || true
        
        # Update to new image
        az containerapp update \
          --name ${{ secrets.CONTAINERAPP_NAME }} \
          --resource-group lab5-rg \
          --image ${{ secrets.ACR_NAME }}.azurecr.io/acr-lab:${{ github.event.workflow_run.head_sha }}
        
        echo "✅ Container App updated with new image"
    
    - name: Verify Deployment
      run: |
        sleep 60
        curl -f https://${{ secrets.CONTAINERAPP_URL }}/health || exit 1
        echo "✅ Container App deployment verified!"
```

### Test Auto-Deployment
```bash
# Push changes to trigger full pipeline: Build → Push → Deploy to Container Apps
git add .
git commit -m "Update container app"
git push origin main
```

### Verify CI/CD Deployment
```bash
# Check workflow status
gh run list --workflow="Deploy to Container Apps"

# Test updated deployment
curl https://$(gh secret get CONTAINERAPP_URL)/
```

## ✅ Step 4: Advanced Scaling

### Update Scaling Rules
```bash
# Run advanced scaling configuration
./scripts/scale-containerapp.sh

# Test scaling with load
source .env
echo "🔥 Load testing to trigger auto-scaling..."

# Generate load
for i in {1..100}; do
  curl https://$CONTAINERAPP_URL/ &
  if (( i % 10 == 0 )); then
    echo "Sent $i requests..."
    sleep 1
  fi
done
wait

echo "✅ Load test complete - check replica count"
```

### Monitor Scaling
```bash
# Watch scaling in real-time
watch -n 5 'az containerapp replica list --name $CONTAINERAPP_NAME --resource-group $RG_NAME --output table'

# Check revision history
az containerapp revision list --name $CONTAINERAPP_NAME --resource-group $RG_NAME --output table
```

### Cleanup
```bash
./scripts/cleanup-containerapp.sh
```

## 🎓 Complete

### What You Built
✅ Azure Container Apps - Production-ready container hosting
✅ Auto-scaling - Automatic scaling based on HTTP load
✅ Zero-downtime deployments - Revision-based deployment strategy
✅ External ingress - HTTPS endpoints with custom domains
✅ CI/CD integration - Automated deployments from ACR

### Key Skills Learned
- Container Apps environment and application management
- HTTP-based auto-scaling configuration and monitoring
- Revision management for zero-downtime deployments
- Load testing and scaling verification techniques
- Production container orchestration with Azure Container Apps

### Next Steps (Challenge)
- Production: Add custom domains, SSL certificates, and monitoring
- Advanced: Implement blue-green deployments and A/B testing
