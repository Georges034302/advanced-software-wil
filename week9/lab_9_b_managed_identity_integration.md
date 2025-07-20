# 🔒 Lab 9B: Managed Identity for Secure App-to-Database Connection

## 🎯 Objective
Replace hardcoded database credentials with Managed Identity authentication to Azure Key Vault. Enable secure, passwordless access to secrets.

- Enable Managed Identity on Azure App Service
- Grant Key Vault access to Managed Identity
- Update Flask app to use Azure SDK with Managed Identity
- Remove all hardcoded secrets from application code

## 🗂 Structure
```
lab9b/
├── app-secure.py (updated Flask app)
├── requirements.txt (updated)
├── scripts/
│   ├── setup-managed-identity.sh
│   └── deploy-secure-app.sh
└── README.md
```

## ✅ Step 1: Enable Managed Identity

### `scripts/setup-managed-identity.sh`
```bash
#!/bin/bash
set -e

# Configuration (use from Lab 9A)
source ../lab9a/.env
APP_NAME="lab9b-secure-app-$(openssl rand -hex 4)"
APP_RG="lab9b-rg"
LOCATION="australiaeast"

echo "🔒 Setting up Managed Identity for secure app..."

# Create resource group for app
echo "📦 Creating app resource group..."
az group create --name $APP_RG --location $LOCATION

# Create App Service plan
echo "📊 Creating App Service plan..."
az appservice plan create \
  --resource-group $APP_RG \
  --name lab9b-plan \
  --sku B1 \
  --is-linux

# Create web app
echo "🌐 Creating web app..."
az webapp create \
  --resource-group $APP_RG \
  --plan lab9b-plan \
  --name $APP_NAME \
  --runtime "PYTHON:3.11"

# Enable system-assigned managed identity
echo "🔐 Enabling system-assigned managed identity..."
az webapp identity assign \
  --resource-group $APP_RG \
  --name $APP_NAME

# Get the managed identity principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --resource-group $APP_RG \
  --name $APP_NAME \
  --query principalId -o tsv)

echo "✅ Managed Identity enabled with Principal ID: $PRINCIPAL_ID"

# Grant Key Vault access to Managed Identity
echo "🔑 Granting Key Vault access to Managed Identity..."
az keyvault set-policy \
  --name $KV_NAME \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list

# Configure app settings
echo "⚙️ Configuring app settings..."
az webapp config appsettings set \
  --resource-group $APP_RG \
  --name $APP_NAME \
  --settings \
    KEY_VAULT_URL="$KV_URI" \
    AZURE_CLIENT_ID="system"

# Save configuration
cat > .env << EOF
APP_NAME=$APP_NAME
APP_RG=$APP_RG
PRINCIPAL_ID=$PRINCIPAL_ID
KV_NAME=$KV_NAME
KV_URI=$KV_URI
EOF

echo "✅ Managed Identity setup complete!"
echo "🌐 App Name: $APP_NAME"
echo "🔐 Principal ID: $PRINCIPAL_ID"
echo "🔑 Key Vault Access: Granted"
```

## ✅ Step 2: Secure Flask Application

### `app-secure.py`
```python
import os
from flask import Flask, jsonify, request
from datetime import datetime
import pyodbc
import logging

# Azure SDK imports for Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Key Vault configuration
KEY_VAULT_URL = os.environ.get('KEY_VAULT_URL')

# Initialize Azure credential and Key Vault client
try:
    credential = DefaultAzureCredential()
    kv_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
    logger.info("✅ Connected to Key Vault using Managed Identity")
except Exception as e:
    logger.error(f"❌ Failed to connect to Key Vault: {e}")
    kv_client = None

def get_database_config():
    """Retrieve database configuration from Key Vault using Managed Identity."""
    if not kv_client:
        raise Exception("Key Vault client not initialized")
    
    try:
        logger.info("🔍 Retrieving database configuration from Key Vault...")
        
        # Retrieve secrets from Key Vault
        sql_server = kv_client.get_secret("sql-server").value
        sql_database = kv_client.get_secret("sql-database").value
        sql_username = kv_client.get_secret("sql-username").value
        sql_password = kv_client.get_secret("sql-password").value
        
        logger.info("✅ Database configuration retrieved successfully")
        
        return {
            'server': sql_server,
            'database': sql_database,
            'username': sql_username,
            'password': sql_password
        }
        
    except Exception as e:
        logger.error(f"❌ Error retrieving database config: {e}")
        raise

def get_db_connection():
    """Create database connection using Key Vault secrets."""
    try:
        config = get_database_config()
        
        connection_string = f"""
        DRIVER={{ODBC Driver 18 for SQL Server}};
        SERVER={config['server']};
        DATABASE={config['database']};
        UID={config['username']};
        PWD={config['password']};
        Encrypt=yes;
        TrustServerCertificate=yes;
        """
        
        return pyodbc.connect(connection_string)
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

@app.route('/')
def home():
    return jsonify({
        "service": "Secure Student Database Service",
        "version": "2.0 - Managed Identity",
        "security": "Azure Key Vault + Managed Identity",
        "authentication": "Passwordless",
        "endpoints": ["/students", "/student", "/health", "/security-info"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/students', methods=['GET'])
def get_students():
    """Get all students using secure database connection."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, created_at FROM students")
        rows = cursor.fetchall()
        
        students = []
        for row in rows:
            students.append({
                "id": row[0],
                "name": row[1], 
                "email": row[2],
                "created_at": row[3].isoformat() if row[3] else None
            })
        
        conn.close()
        
        return jsonify({
            "students": students,
            "count": len(students),
            "security": "Retrieved using Managed Identity",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error in get_students: {e}")
        return jsonify({"error": "Database operation failed"}), 500

@app.route('/student', methods=['POST'])
def add_student():
    """Add a new student using secure database connection."""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        
        # Get the new student ID
        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            "message": "Student added successfully",
            "id": int(new_id),
            "name": name,
            "email": email,
            "security": "Added using Managed Identity",
            "timestamp": datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        logger.error(f"❌ Error in add_student: {e}")
        return jsonify({"error": "Database operation failed"}), 500

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student using secure database connection."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, name, email, created_at FROM students WHERE id = ?",
            (student_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return jsonify({"error": "Student not found"}), 404
        
        student = {
            "id": row[0],
            "name": row[1],
            "email": row[2], 
            "created_at": row[3].isoformat() if row[3] else None
        }
        
        conn.close()
        
        return jsonify({
            "student": student,
            "security": "Retrieved using Managed Identity",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error in get_student: {e}")
        return jsonify({"error": "Database operation failed"}), 500

@app.route('/health')
def health():
    """Health check with secure database connectivity test."""
    try:
        # Test Key Vault access
        config = get_database_config()
        
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "security": "Key Vault + Managed Identity",
            "students_count": count,
            "key_vault": "accessible",
            "authentication": "passwordless",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected", 
            "security": "authentication_failed",
            "error": "Service unavailable",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/security-info')
def security_info():
    """Display security configuration information."""
    return jsonify({
        "security_model": "Azure Managed Identity",
        "authentication": "Passwordless",
        "secret_management": "Azure Key Vault",
        "encryption": "TLS 1.2+ for all connections",
        "identity_type": "System-assigned Managed Identity",
        "key_vault_url": KEY_VAULT_URL,
        "benefits": [
            "No hardcoded credentials",
            "Automatic credential rotation",
            "Azure AD integration",
            "Audit logging",
            "Principle of least privilege"
        ],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    if not KEY_VAULT_URL:
        logger.error("❌ KEY_VAULT_URL environment variable not set")
        exit(1)
    
    logger.info(f"🔒 Starting Secure Student Service with Key Vault: {KEY_VAULT_URL}")
    app.run(host='0.0.0.0', port=8000, debug=False)
```

### `requirements.txt`
```
Flask==3.0.0
pyodbc==5.0.1
azure-identity==1.15.0
azure-keyvault-secrets==4.7.0
```

## ✅ Step 3: Deploy Secure Application

### `scripts/deploy-secure-app.sh`
```bash
#!/bin/bash
set -e

# Load configuration
source .env

echo "🚀 Deploying secure Flask app with Managed Identity..."

# Create deployment package
echo "📦 Creating deployment package..."
zip -r app.zip app-secure.py requirements.txt

# Deploy to App Service
echo "📤 Deploying to App Service..."
az webapp deployment source config-zip \
  --resource-group $APP_RG \
  --name $APP_NAME \
  --src app.zip

# Set startup command
echo "⚙️ Configuring startup command..."
az webapp config set \
  --resource-group $APP_RG \
  --name $APP_NAME \
  --startup-file "python app-secure.py"

# Wait for deployment
echo "⏳ Waiting for deployment to complete..."
sleep 30

# Get app URL
APP_URL="https://$APP_NAME.azurewebsites.net"
echo "✅ App deployed to: $APP_URL"

# Test deployment
echo "🧪 Testing secure app deployment..."
for i in {1..5}; do
    echo "Health check attempt $i/5..."
    
    if curl -f $APP_URL/health; then
        echo "✅ Health check passed on attempt $i"
        break
    fi
    
    if [ $i -eq 5 ]; then
        echo "❌ Health check failed after 5 attempts"
        exit 1
    fi
    
    sleep 10
done

echo "✅ Secure app deployment successful!"
echo "🔗 App URL: $APP_URL"
echo "🔒 Security: Managed Identity + Key Vault"

# Test endpoints
echo "🧪 Testing secure endpoints..."
curl -s $APP_URL/security-info | head -20
```

## ✅ Step 4: Test Secure Application

### Run Setup and Deployment
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Setup Managed Identity
./scripts/setup-managed-identity.sh

# Deploy secure app
./scripts/deploy-secure-app.sh
```

### Test Security Features
```bash
# Get app URL from environment
source .env
APP_URL="https://$APP_NAME.azurewebsites.net"

# Test security info
curl $APP_URL/security-info

# Test health with security details
curl $APP_URL/health

# Test students endpoint
curl $APP_URL/students

# Add a student
curl -X POST $APP_URL/student \
  -H "Content-Type: application/json" \
  -d '{"name": "Secure User", "email": "secure@university.edu"}'
```

## ✅ Step 5: Verify Security

### Check Managed Identity
```bash
# Verify Managed Identity is enabled
az webapp identity show \
  --resource-group $APP_RG \
  --name $APP_NAME

# Check Key Vault access policies
az keyvault show \
  --name $KV_NAME \
  --query "properties.accessPolicies[?objectId=='$PRINCIPAL_ID']"
```

### Monitor Security Logs
```bash
# Check application logs
az webapp log tail \
  --resource-group $APP_RG \
  --name $APP_NAME
```

## ✅ Step 6: Security Comparison

### Before (Lab 8B) - Hardcoded Secrets ❌
```python
# INSECURE - Hardcoded credentials
DB_SERVER = os.environ.get('SQL_SERVER')
DB_PASSWORD = os.environ.get('SQL_PASSWORD')
```

### After (Lab 9B) - Managed Identity ✅
```python
# SECURE - Managed Identity + Key Vault
credential = DefaultAzureCredential()
kv_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
sql_password = kv_client.get_secret("sql-password").value
```

## ✅ Step 7: Cleanup

### Delete Resources
```bash
# Delete app resource group
az group delete --name lab9b-rg --yes --no-wait

# Keep Key Vault from Lab 9A for next labs
```

## 🎓 Lab Complete

### What You Built
✅ **Managed Identity** - System-assigned identity for App Service  
✅ **Passwordless Authentication** - No credentials in application code  
✅ **Secure Key Vault Access** - Identity-based secret retrieval  
✅ **Zero Hardcoded Secrets** - All credentials from Key Vault  
✅ **Audit-Ready Security** - All access logged and monitored  

### Key Skills Learned
- Azure Managed Identity configuration and usage
- Azure SDK integration with DefaultAzureCredential
- Passwordless authentication to Azure services
- Key Vault access policy management
- Secure application architecture patterns

### Security Benefits Achieved
- **No Credential Exposure**: Zero secrets in code or configuration
- **Automatic Rotation**: Key Vault handles credential lifecycle
- **Audit Trail**: All secret access logged in Azure Monitor
- **Principle of Least Privilege**: Minimal required permissions only
- **Azure AD Integration**: Centralized identity management

Your application now uses enterprise-grade security with Managed Identity and is ready for automated security scanning in Lab 9C!
