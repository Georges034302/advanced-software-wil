# ☁️ Lab 5A: ACR + GitHub Actions

## 🎯 Objective
Set up Azure Container Registry and automate Docker builds with GitHub Actions.

- Create Azure Container Registry with automated setup scripts
- Configure GitHub Actions for CI/CD pipeline automation
- Build and containerize a Flask API application
- Implement secure authentication using Azure Service Principal
- Store and manage Docker images in Azure cloud registry

## 🗂 Structure
```
lab5a/
├── scripts/
│   ├── env_setup.sh
│   └── create-acr.sh
├── src/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── .github/workflows/build-push.yml
```

## ✅ Step 1: Setup Scripts

### Get GitHub PAT
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with scopes: `repo`, `workflow`
3. Copy token for script setup

### `scripts/env_setup.sh`
```bash
#!/bin/bash
set -e

echo "🔧 Lab 5A Environment Setup"

if [[ -z "$GITHUB_TOKEN" ]]; then
    read -s -p "Enter GitHub PAT: " GITHUB_TOKEN
    echo "export GITHUB_TOKEN=$GITHUB_TOKEN" > .env
fi

echo "$GITHUB_TOKEN" | gh auth login --with-token

# Check if logged into Azure, if not login
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)
SP_NAME="sp-lab5a-$RANDOM"
ACR_NAME="acr$(openssl rand -hex 4)"

SP_JSON=$(az ad sp create-for-rbac --name "$SP_NAME" --role Contributor --sdk-auth)
APP_ID=$(echo "$SP_JSON" | jq -r .clientId)

cat >> .env << EOF
export RG_NAME=lab5-rg
export LOCATION=australiaeast
export ACR_NAME=$ACR_NAME
export APP_ID=$APP_ID
EOF

az group create --name lab5-rg --location australiaeast
echo "$SP_JSON" | gh secret set AZURE_CREDENTIALS
echo "$ACR_NAME" | gh secret set ACR_NAME

# Add .gitignore for Environment Security
# Create .gitignore if it doesn't exist and add .env to it
if [ ! -f .gitignore ]; then
    echo ".env" > .gitignore
else
    grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
fi

echo "✅ Environment ready"
```

### `scripts/create-acr.sh`
```bash
#!/bin/bash
set -e

echo "🐳 Creating ACR"
source .env

az acr create --resource-group $RG_NAME --name $ACR_NAME --sku Basic --admin-enabled true

ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

echo "$ACR_LOGIN_SERVER" | gh secret set ACR_LOGIN_SERVER
echo "$ACR_USERNAME" | gh secret set ACR_USERNAME
echo "$ACR_PASSWORD" | gh secret set ACR_PASSWORD

echo "✅ ACR created: $ACR_NAME"
```

### Run Setup
```bash
chmod +x scripts/*.sh
./scripts/env_setup.sh
./scripts/create-acr.sh
```

## ✅ Step 2: Flask App

### `src/app.py`
```python
from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify(message="ACR Lab", timestamp=str(datetime.datetime.now()))

@app.route("/health")
def health():
    return jsonify(status="healthy", version="1.0.0")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `src/requirements.txt`
```
Flask==2.3.3
```

### `src/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

## ✅ Step 3: GitHub Actions

### `.github/workflows/build-push.yml`
```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    - run: |
        az acr build \
          --registry ${{ secrets.ACR_NAME }} \
          --image acr-lab:${{ github.sha }} \
          --file src/Dockerfile src/
```

## ✅ Step 4: Test & Deploy

### Local Test
```bash
cd src && python app.py
curl http://localhost:5000/
```

### Deploy
```bash
git add . && git commit -m "ACR lab" && git push
```

### Verify
```bash
az acr repository list --name $ACR_NAME
```

## 🎓 Complete

### What You Built
✅ Azure Container Registry - Secure Docker image storage  
✅ Service Principal - Automated Azure authentication  
✅ Flask API - Simple containerized web service  
✅ GitHub Actions - CI/CD pipeline for automatic builds  
✅ Docker Integration - Multi-stage container deployment  

### Key Skills Learned
- Azure CLI automation and scripting
- GitHub secrets management for secure CI/CD
- Container registry operations and image versioning
- Infrastructure as Code with bash scripts
- End-to-end containerized application deployment

### Next Steps
- Lab 5B: Deploy to Azure Container Instances (ACI)
- Lab 5C: Scale with Azure Container Apps
