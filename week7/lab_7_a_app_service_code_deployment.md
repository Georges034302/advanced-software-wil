# 🚀 Lab 7A: Azure App Service Code Deployment

## 🎯 Objective
Deploy two independent Python microservices directly from code to Azure App Service with Git deployment and service-to-service HTTP communication.

- Create Azure App Service Plan and Web Apps
- Deploy Flask microservices using local Git deployment
- Configure service-to-service communication via environment variables
- Test microservice integration and HTTP communication
- Monitor and troubleshoot App Service deployments

## 🗂 Structure
```
lab7a/
├── studentservice/
│   ├── app.py
│   └── requirements.txt
├── reportservice/
│   ├── app.py
│   └── requirements.txt
├── scripts/
│   ├── setup-infrastructure.sh
│   ├── deploy-student-service.sh
│   └── deploy-report-service.sh
└── cleanup.sh
```

## 🧭 Prerequisites

- Azure Portal access ([https://portal.azure.com](https://portal.azure.com))
- Azure CLI installed and authenticated (`az login`)
- Python 3.11+
- Git installed
- **Register App Service provider (first-time users):**

```bash
# Register Microsoft.Web provider
az provider register --namespace Microsoft.Web

# Confirm registration
az provider show --namespace Microsoft.Web --query registrationState
```

## ✅ Step 1: Infrastructure Setup

### `scripts/setup-infrastructure.sh`
```bash
#!/bin/bash
set -e

echo "🏗️ Setting up Azure App Service infrastructure..."

# Check Azure login
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

# Generate unique names
UNIQUE_ID=$(openssl rand -hex 4)

# Create .env file
cat > .env << EOF
export RG_NAME=lab7a-rg
export LOCATION=australiaeast
export APP_SERVICE_PLAN=microservice-plan-$UNIQUE_ID
export STUDENT_SERVICE_APP=studentservice$UNIQUE_ID
export REPORT_SERVICE_APP=reportservice$UNIQUE_ID
EOF

source .env

echo "📦 Creating resource group..."
az group create \
  --name $RG_NAME \
  --location $LOCATION

echo "📊 Creating App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RG_NAME \
  --sku B1 \
  --is-linux

echo "✅ Infrastructure setup complete!"
echo "📝 Environment variables saved to .env"
echo "🔍 Resource Group: $RG_NAME"
echo "📊 App Service Plan: $APP_SERVICE_PLAN"
```

### Run Infrastructure Setup
```bash
chmod +x scripts/*.sh
./scripts/setup-infrastructure.sh
source .env
```

## ✅ Step 2: Student Info Microservice

### `studentservice/app.py`
```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Sample student data
STUDENTS = {
    "101": {"id": "101", "name": "Ava Chen", "major": "Computer Science", "year": 3},
    "102": {"id": "102", "name": "Marcus Johnson", "major": "Data Science", "year": 2},
    "103": {"id": "103", "name": "Sofia Rodriguez", "major": "Software Engineering", "year": 4},
    "104": {"id": "104", "name": "Kai Patel", "major": "Cybersecurity", "year": 1}
}

@app.route('/')
def home():
    return jsonify({
        "service": "Student Info Service",
        "version": "1.0.0",
        "endpoints": ["/student/<id>", "/students", "/health"]
    })

@app.route('/student/<id>')
def get_student(id):
    student = STUDENTS.get(id)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/students')
def get_all_students():
    return jsonify({"students": list(STUDENTS.values()), "count": len(STUDENTS)})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "student-info"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
```

### `studentservice/requirements.txt`
```
Flask==2.3.3
```

### `scripts/deploy-student-service.sh`
```bash
#!/bin/bash
set -e

echo "📚 Deploying Student Info Service..."
source .env

# Create the web app
echo "🌐 Creating Student Service web app..."
az webapp create \
  --resource-group $RG_NAME \
  --plan $APP_SERVICE_PLAN \
  --name $STUDENT_SERVICE_APP \
  --runtime "PYTHON|3.11" \
  --deployment-local-git

# Get deployment URL
DEPLOY_URL=$(az webapp deployment source config-local-git \
  --name $STUDENT_SERVICE_APP \
  --resource-group $RG_NAME \
  --query url -o tsv)

echo "📦 Setting up Git deployment..."
cd studentservice

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
fi

# Add Azure remote
git remote remove azure 2>/dev/null || true
git remote add azure $DEPLOY_URL

# Deploy code
git add .
git commit -m "Deploy Student Info Service" || echo "No changes to commit"
git push azure main:master

cd ..

echo "✅ Student Service deployed!"
echo "🌐 URL: https://$STUDENT_SERVICE_APP.azurewebsites.net"
echo "🧪 Test: https://$STUDENT_SERVICE_APP.azurewebsites.net/student/101"
```

## ✅ Step 3: Report Generation Microservice

### `reportservice/app.py`
```python
import os
import requests
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Get student service URL from environment
STUDENT_SERVICE_APP = os.environ.get("STUDENT_SERVICE_APP")

@app.route('/')
def home():
    return jsonify({
        "service": "Report Generation Service",
        "version": "1.0.0",
        "endpoints": ["/report/<id>", "/report/summary", "/health"],
        "student_service": f"https://{STUDENT_SERVICE_APP}.azurewebsites.net" if STUDENT_SERVICE_APP else "Not configured"
    })

@app.route('/report/<id>')
def get_student_report(id):
    if not STUDENT_SERVICE_APP:
        return jsonify({"error": "Student service not configured"}), 500
    
    try:
        # Call Student Service
        url = f"https://{STUDENT_SERVICE_APP}.azurewebsites.net/student/{id}"
        app.logger.info(f"Calling student service: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return jsonify({"error": "Student not found"}), 404
        
        response.raise_for_status()
        student = response.json()
        
        # Generate report
        report = {
            "report_id": f"RPT-{id}-2024",
            "student_info": student,
            "academic_standing": "Good Standing",
            "credits_completed": 45 + (int(student.get('year', 1)) - 1) * 30,
            "graduation_status": "On Track" if int(student.get('year', 1)) <= 4 else "Extended",
            "generated_by": "Report Generation Service",
            "report_summary": f"Student {student['name']} is a {student['year']}-year {student['major']} student in good academic standing."
        }
        
        return jsonify(report)
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling student service: {e}")
        return jsonify({"error": "Failed to fetch student data", "details": str(e)}), 500

@app.route('/report/summary')
def get_summary_report():
    if not STUDENT_SERVICE_APP:
        return jsonify({"error": "Student service not configured"}), 500
    
    try:
        # Get all students
        url = f"https://{STUDENT_SERVICE_APP}.azurewebsites.net/students"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        students = data.get('students', [])
        
        # Generate summary
        majors = {}
        total_students = len(students)
        
        for student in students:
            major = student.get('major', 'Unknown')
            majors[major] = majors.get(major, 0) + 1
        
        summary = {
            "report_type": "Summary Report",
            "total_students": total_students,
            "majors_breakdown": majors,
            "most_popular_major": max(majors, key=majors.get) if majors else "N/A",
            "generated_by": "Report Generation Service"
        }
        
        return jsonify(summary)
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling student service: {e}")
        return jsonify({"error": "Failed to fetch student data", "details": str(e)}), 500

@app.route('/health')
def health():
    status = {
        "status": "healthy",
        "service": "report-generation",
        "student_service_configured": STUDENT_SERVICE_APP is not None
    }
    
    # Test connection to student service
    if STUDENT_SERVICE_APP:
        try:
            url = f"https://{STUDENT_SERVICE_APP}.azurewebsites.net/health"
            response = requests.get(url, timeout=5)
            status["student_service_status"] = "reachable" if response.status_code == 200 else "unreachable"
        except:
            status["student_service_status"] = "unreachable"
    
    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
```

### `reportservice/requirements.txt`
```
Flask==2.3.3
requests==2.31.0
```

### `scripts/deploy-report-service.sh`
```bash
#!/bin/bash
set -e

echo "📊 Deploying Report Generation Service..."
source .env

# Create the web app
echo "🌐 Creating Report Service web app..."
az webapp create \
  --resource-group $RG_NAME \
  --plan $APP_SERVICE_PLAN \
  --name $REPORT_SERVICE_APP \
  --runtime "PYTHON|3.11" \
  --deployment-local-git

# Configure environment variable for service communication
echo "🔗 Configuring service communication..."
az webapp config appsettings set \
  --resource-group $RG_NAME \
  --name $REPORT_SERVICE_APP \
  --settings STUDENT_SERVICE_APP=$STUDENT_SERVICE_APP

# Get deployment URL
DEPLOY_URL=$(az webapp deployment source config-local-git \
  --name $REPORT_SERVICE_APP \
  --resource-group $RG_NAME \
  --query url -o tsv)

echo "📦 Setting up Git deployment..."
cd reportservice

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
fi

# Add Azure remote
git remote remove azure 2>/dev/null || true
git remote add azure $DEPLOY_URL

# Deploy code
git add .
git commit -m "Deploy Report Generation Service" || echo "No changes to commit"
git push azure main:master

cd ..

echo "✅ Report Service deployed!"
echo "🌐 URL: https://$REPORT_SERVICE_APP.azurewebsites.net"
echo "🧪 Test: https://$REPORT_SERVICE_APP.azurewebsites.net/report/101"
```

## ✅ Step 4: Deploy Services

### Deploy Student Service
```bash
./scripts/deploy-student-service.sh
```

### Deploy Report Service
```bash
./scripts/deploy-report-service.sh
```

**Note:** You'll be prompted for Azure App Service deployment credentials during Git push. Set these in Azure Portal under **App Services** > **Deployment Center** > **Local Git/FTPS Credentials**.

## ✅ Step 5: Test Integration

### Test Individual Services
```bash
source .env

# Test Student Service
echo "📚 Testing Student Service..."
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/student/101

# Test all students
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/students
```

### Test Service Integration
```bash
# Test Report Service (calls Student Service)
echo "📊 Testing Report Service..."
curl https://$REPORT_SERVICE_APP.azurewebsites.net/report/101

# Test Summary Report
curl https://$REPORT_SERVICE_APP.azurewebsites.net/report/summary

# Test Health Endpoints
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/health
curl https://$REPORT_SERVICE_APP.azurewebsites.net/health
```

### Browser Testing
Visit these URLs in your browser:

1. **Student Service**: `https://<STUDENT_SERVICE_APP>.azurewebsites.net/student/101`
2. **Report Service**: `https://<REPORT_SERVICE_APP>.azurewebsites.net/report/101`
3. **Summary Report**: `https://<REPORT_SERVICE_APP>.azurewebsites.net/report/summary`

**Expected Results:**
- Student Service returns JSON with student details
- Report Service returns formatted academic report
- Summary Report shows statistics for all students

## ✅ Step 6: Monitor & Troubleshoot

### View Application Logs
```bash
# Student Service logs
az webapp log tail \
  --name $STUDENT_SERVICE_APP \
  --resource-group $RG_NAME

# Report Service logs
az webapp log tail \
  --name $REPORT_SERVICE_APP \
  --resource-group $RG_NAME
```

### Check App Status
```bash
# List all web apps
az webapp list \
  --resource-group $RG_NAME \
  --output table

# Check specific app status
az webapp show \
  --name $STUDENT_SERVICE_APP \
  --resource-group $RG_NAME \
  --query "{name:name, state:state, defaultHostName:defaultHostName}"
```

### Common Issues & Solutions

**🔧 Git Push Authentication:**
- Set deployment credentials in Azure Portal: **App Services** > **Deployment Center** > **Local Git/FTPS Credentials**

**🔧 Service Communication Errors:**
- Verify environment variable: `az webapp config appsettings list --name $REPORT_SERVICE_APP --resource-group $RG_NAME`
- Check service URLs and test individual endpoints first

**🔧 Slow Initial Response:**
- App Service has cold start delay (~30-60 seconds) after deployment
- Test health endpoints first, then functional endpoints

## ✅ Step 7: Cleanup

### `cleanup.sh`
```bash
#!/bin/bash

echo "🧹 Cleaning up Lab 7A resources..."
source .env

# Delete resource group (removes all resources)
az group delete \
  --name $RG_NAME \
  --yes \
  --no-wait

echo "✅ Cleanup initiated"
echo "🔍 Monitor cleanup: az group list --query \"[?name=='$RG_NAME']\""
```

```bash
chmod +x cleanup.sh
./cleanup.sh
```

## 🎓 Lab Complete

### What You Built
✅ **Microservice Architecture** - Two independent services with HTTP communication  
✅ **Azure App Service** - PaaS deployment with built-in scaling and monitoring  
✅ **Git Deployment** - Direct code deployment without containers  
✅ **Service Discovery** - Environment-based service communication  
✅ **Health Monitoring** - Health endpoints and logging  

### Key Skills Learned
- Azure App Service Plan and Web App creation
- Python Flask microservice development
- Local Git deployment to Azure App Service
- Service-to-service HTTP communication
- Environment variable configuration for service discovery
- Azure CLI automation and monitoring
- Troubleshooting App Service deployments

### Architecture Pattern
```
Internet → Report Service → Student Service
          (HTTP calls)    (Data provider)
```

### Production Benefits
- **Simplified Deployment**: No container management required
- **Auto-scaling**: Built-in App Service scaling capabilities
- **Monitoring**: Integrated Azure monitoring and logging
- **Cost-effective**: Pay-per-use pricing model
- **SSL/TLS**: Automatic HTTPS certificate management

### Next Steps (Lab 7B Preview)
In the next lab, you'll containerize these same microservices and deploy them as Docker containers to Azure App Service, learning the benefits of containerized deployments.
