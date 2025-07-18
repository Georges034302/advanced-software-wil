# ☁️ Lab 5B: Deploy to Azure Container Instances

## 🎯 Objective
Deploy containerized Flask app from ACR to Azure Container Instances for serverless hosting.

- Deploy Docker containers to Azure Container Instances (ACI)
- Configure public endpoints and environment variables
- Monitor container performance and logs
- Implement health checks and restart policies
- Automate deployment with CI/CD pipelines

## 🗂 Structure
```
lab5b/
├── scripts/
│   ├── deploy-aci.sh
│   └── cleanup-aci.sh
├── .github/workflows/
│   └── deploy-aci.yml
└── .env (from Lab 5A)
```

## ✅ Step 1: Deploy Script

### `scripts/deploy-aci.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying to Azure Container Instances"
source .env

# Use specific image tag if provided (for CI/CD), otherwise latest
IMAGE_TAG=${IMAGE_TAG:-latest}

# Generate unique ACI name only if not already set
if [[ -z "$ACI_NAME" ]]; then
    ACI_NAME="aci-lab5b-$(date +%s)"
    echo "export ACI_NAME=$ACI_NAME" >> .env
fi

# Login to ACR
az acr login --name $ACR_NAME

# Deploy to ACI
az container create \
  --resource-group $RG_NAME \
  --name $ACI_NAME \
  --image $ACR_NAME.azurecr.io/acr-lab:$IMAGE_TAG \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label $ACI_NAME \
  --ports 5000 \
  --cpu 1 \
  --memory 1 \
  --restart-policy Always

# Get public FQDN
ACI_FQDN=$(az container show \
  --resource-group $RG_NAME \
  --name $ACI_NAME \
  --query ipAddress.fqdn \
  -o tsv)

echo "export ACI_FQDN=$ACI_FQDN" >> .env

# Store ACI details in GitHub secrets
if command -v gh &> /dev/null; then
    # Logout from any existing GitHub session
    gh auth logout --hostname github.com || true
    
    # Login with the stored GitHub PAT
    if [[ -n "$GITHUB_TOKEN" ]]; then
        echo "$GITHUB_TOKEN" | gh auth login --with-token --hostname github.com
        echo "$ACI_NAME" | gh secret set ACI_NAME
        echo "$ACI_FQDN" | gh secret set ACI_FQDN
        echo "✅ ACI details stored in GitHub secrets"
    else
        echo "⚠️ GITHUB_TOKEN not found in .env - skipping secret storage"
    fi
fi

echo ""
echo "✅ ACI deployment complete!"
echo "🌐 Access your app: http://$ACI_FQDN:5000"
```

### `scripts/cleanup-aci.sh`
```bash
#!/bin/bash
set -e

echo "🧹 Cleaning up ACI resources"
source .env

if [[ -n "$ACI_NAME" ]]; then
    az container delete \
      --resource-group $RG_NAME \
      --name $ACI_NAME \
      --yes
    echo "✅ ACI instance deleted: $ACI_NAME"
else
    echo "ℹ️ No ACI instance found in .env"
fi
```

### Run Deployment
```bash
chmod +x scripts/*.sh
./scripts/deploy-aci.sh
```

## ✅ Step 2: Monitor & Test

### Check Status
```bash
# View container status
az container show --resource-group $RG_NAME --name $ACI_NAME --query instanceView.state

# Get logs
az container logs --resource-group $RG_NAME --name $ACI_NAME

# Monitor resources
az container show --resource-group $RG_NAME --name $ACI_NAME --query containers[0].instanceView
```

### Test Endpoints
```bash
source .env

# Test root endpoint
curl http://$ACI_FQDN:5000/

# Test health endpoint
curl http://$ACI_FQDN:5000/health
```

## ✅ Step 3: CI/CD Deployment

### `.github/workflows/deploy-aci.yml`
```yaml
name: Deploy to ACI

on:
  workflow_run:
    workflows: ["Build and Push"]
    types:
      - completed

jobs:
  deploy-aci:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
    - uses: actions/checkout@v4
    
    - name: Login to GitHub CLI
      run: echo "${{ secrets.GITHUB_TOKEN }}" | gh auth login --with-token
    
    - uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Pull latest image from ACR
      run: |
        az acr login --name ${{ secrets.ACR_NAME }}
        docker pull ${{ secrets.ACR_NAME }}.azurecr.io/acr-lab:${{ github.event.workflow_run.head_sha }}
    
    - name: Deploy to ACI
      run: |
        source .env || true
        export IMAGE_TAG=${{ github.event.workflow_run.head_sha }}
        chmod +x scripts/deploy-aci.sh
        ./scripts/deploy-aci.sh
    
    - name: Verify Deployment
      run: |
        source .env
        echo "🔍 Verifying deployment at: http://$ACI_FQDN:5000"
        sleep 30
        curl -f http://$ACI_FQDN:5000/health || exit 1
        echo "✅ Deployment verified successfully!"
```

### Test Auto-Deployment
```bash
# Push changes to trigger Lab 5A build, then auto-deploy to ACI
git add .
git commit -m "Update app"
git push origin main
```

### Verify CI/CD Deployment
```bash
# Check GitHub Actions workflow status
gh run list --workflow="Deploy to ACI"

# Get ACI details from secrets
gh secret list | grep ACI

# Test the deployed endpoint
curl http://$(gh secret get ACI_FQDN):5000/
curl http://$(gh secret get ACI_FQDN):5000/health
```

### Cleanup
```bash
./scripts/cleanup-aci.sh
```

## 🎓 Complete

### What You Built
✅ Azure Container Instance - Serverless container hosting
✅ Public endpoints - Direct internet access to your app
✅ Health monitoring - Automated container health checks
✅ CI/CD deployment - Automated deployment pipeline
✅ GitHub integration - Secret management and workflow automation

### Key Skills Learned
- Container orchestration with Azure Container Instances
- Public endpoint configuration and DNS management
- Container health monitoring and restart policies
- CI/CD pipeline automation with GitHub Actions
- GitHub CLI secret management and authentication

### Next Steps
- Lab 5C: Scale with Azure Container Apps
