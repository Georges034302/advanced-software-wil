# 🐳 Lab 7B: Azure App Service Container Deployment

## 🎯 Objective
Containerize the microservices from Lab 7A and deploy them as Docker containers to Azure App Service using Azure Container Registry (ACR).

- Convert Flask microservices to Docker containers
- Build and push container images to Azure Container Registry
- Deploy containerized apps to Azure App Service
- Configure container-based service communication
- Compare container vs code deployment benefits

## 🗂 Structure
```
lab7b/
├── studentservice/
│   ├── app.py (from Lab 7A)
│   ├── requirements.txt
│   └── Dockerfile
├── reportservice/
│   ├── app.py (from Lab 7A)
│   ├── requirements.txt
│   └── Dockerfile
├── scripts/
│   ├── setup-infrastructure.sh
│   ├── build-images.sh
│   └── deploy-containers.sh
├── docker-compose.yml (for local testing)
└── cleanup.sh
```

## 🧭 Prerequisites

- Completed Lab 7A or equivalent Flask microservice knowledge
- Docker installed locally (for testing)
- Azure CLI with ACR integration
- **Register Container service provider:**

```bash
# Register Microsoft.ContainerRegistry provider
az provider register --namespace Microsoft.ContainerRegistry

# Confirm registration
az provider show --namespace Microsoft.ContainerRegistry --query registrationState
```

## ✅ Step 1: Infrastructure Setup

### `scripts/setup-infrastructure.sh`
```bash
#!/bin/bash
set -e

echo "🏗️ Setting up containerized infrastructure..."

# Check Azure login
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

# Generate unique names
UNIQUE_ID=$(openssl rand -hex 4)

# Create .env file
cat > .env << EOF
export RG_NAME=lab7b-rg
export LOCATION=australiaeast
export ACR_NAME=acr7b$UNIQUE_ID
export APP_SERVICE_PLAN=container-plan-$UNIQUE_ID
export STUDENT_SERVICE_APP=student-container-$UNIQUE_ID
export REPORT_SERVICE_APP=report-container-$UNIQUE_ID
EOF

source .env

echo "📦 Creating resource group..."
az group create \
  --name $RG_NAME \
  --location $LOCATION

echo "🐳 Creating Azure Container Registry..."
az acr create \
  --resource-group $RG_NAME \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

echo "📊 Creating App Service Plan for containers..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RG_NAME \
  --sku B1 \
  --is-linux

# Get ACR credentials for later use
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

echo "export ACR_USERNAME=$ACR_USERNAME" >> .env
echo "export ACR_PASSWORD=$ACR_PASSWORD" >> .env

echo "✅ Infrastructure setup complete!"
echo "📝 Environment variables saved to .env"
echo "🐳 ACR: $ACR_NAME.azurecr.io"
echo "📊 App Service Plan: $APP_SERVICE_PLAN"
```

### Run Infrastructure Setup
```bash
chmod +x scripts/*.sh
./scripts/setup-infrastructure.sh
source .env
```

## ✅ Step 2: Containerize Student Service

### `studentservice/app.py` (Enhanced from Lab 7A)
```python
from flask import Flask, jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
PORT = int(os.environ.get('PORT', 8000))
ENV = os.environ.get('ENV', 'development')

# Sample student data
STUDENTS = {
    "101": {"id": "101", "name": "Ava Chen", "major": "Computer Science", "year": 3},
    "102": {"id": "102", "name": "Marcus Johnson", "major": "Data Science", "year": 2},
    "103": {"id": "103", "name": "Sofia Rodriguez", "major": "Software Engineering", "year": 4},
    "104": {"id": "104", "name": "Kai Patel", "major": "Cybersecurity", "year": 1},
    "105": {"id": "105", "name": "Emma Thompson", "major": "AI/ML", "year": 3}
}

@app.route('/')
def home():
    return jsonify({
        "service": "Student Info Service (Containerized)",
        "version": "2.0.0",
        "environment": ENV,
        "port": PORT,
        "endpoints": ["/student/<id>", "/students", "/health", "/info"],
        "total_students": len(STUDENTS)
    })

@app.route('/student/<id>')
def get_student(id):
    app.logger.info(f"Fetching student with ID: {id}")
    student = STUDENTS.get(id)
    if student:
        return jsonify(student)
    else:
        app.logger.warning(f"Student not found: {id}")
        return jsonify({"error": "Student not found", "id": id}), 404

@app.route('/students')
def get_all_students():
    app.logger.info("Fetching all students")
    return jsonify({
        "students": list(STUDENTS.values()), 
        "count": len(STUDENTS),
        "service": "Student Info Service"
    })

@app.route('/info')
def get_service_info():
    return jsonify({
        "service": "Student Info Service",
        "deployment": "Container",
        "version": "2.0.0",
        "environment": ENV,
        "students_available": list(STUDENTS.keys())
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "student-info",
        "version": "2.0.0",
        "deployment": "container"
    })

if __name__ == '__main__':
    app.logger.info(f"Starting Student Service on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=(ENV == 'development'))
```

### `studentservice/requirements.txt`
```
Flask==2.3.3
gunicorn==21.2.0
```

### `studentservice/Dockerfile`
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60", "app:app"]
```

## ✅ Step 3: Containerize Report Service

### `reportservice/app.py` (Enhanced from Lab 7A)
```python
import os
import requests
from flask import Flask, jsonify
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
PORT = int(os.environ.get('PORT', 8000))
ENV = os.environ.get('ENV', 'development')
STUDENT_SERVICE_URL = os.environ.get("STUDENT_SERVICE_URL")

@app.route('/')
def home():
    return jsonify({
        "service": "Report Generation Service (Containerized)",
        "version": "2.0.0",
        "environment": ENV,
        "port": PORT,
        "endpoints": ["/report/<id>", "/report/summary", "/health", "/info"],
        "student_service": STUDENT_SERVICE_URL or "Not configured"
    })

@app.route('/report/<id>')
def get_student_report(id):
    if not STUDENT_SERVICE_URL:
        return jsonify({"error": "Student service not configured"}), 500
    
    try:
        # Call Student Service
        url = f"{STUDENT_SERVICE_URL}/student/{id}"
        app.logger.info(f"Calling student service: {url}")
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 404:
            return jsonify({"error": "Student not found", "id": id}), 404
        
        response.raise_for_status()
        student = response.json()
        
        # Generate enhanced report
        current_year = datetime.now().year
        credits_completed = 45 + (int(student.get('year', 1)) - 1) * 30
        
        report = {
            "report_id": f"RPT-{id}-{current_year}",
            "generated_at": datetime.now().isoformat(),
            "student_info": student,
            "academic_details": {
                "standing": "Good Standing",
                "credits_completed": credits_completed,
                "credits_required": 120,
                "completion_percentage": round((credits_completed / 120) * 100, 1),
                "graduation_status": "On Track" if int(student.get('year', 1)) <= 4 else "Extended"
            },
            "report_summary": f"Student {student['name']} is a {student['year']}-year {student['major']} student with {credits_completed} credits completed.",
            "generated_by": "Report Generation Service v2.0 (Container)"
        }
        
        return jsonify(report)
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling student service: {e}")
        return jsonify({"error": "Failed to fetch student data", "details": str(e)}), 500

@app.route('/report/summary')
def get_summary_report():
    if not STUDENT_SERVICE_URL:
        return jsonify({"error": "Student service not configured"}), 500
    
    try:
        # Get all students
        url = f"{STUDENT_SERVICE_URL}/students"
        app.logger.info(f"Fetching summary from: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        students = data.get('students', [])
        
        # Generate enhanced summary
        majors = {}
        years = {}
        total_students = len(students)
        
        for student in students:
            major = student.get('major', 'Unknown')
            year = student.get('year', 'Unknown')
            majors[major] = majors.get(major, 0) + 1
            years[str(year)] = years.get(str(year), 0) + 1
        
        summary = {
            "report_type": "Summary Report",
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_students": total_students,
                "majors_breakdown": majors,
                "year_breakdown": years,
                "most_popular_major": max(majors, key=majors.get) if majors else "N/A",
                "average_year": round(sum(int(s.get('year', 1)) for s in students) / total_students, 1) if students else 0
            },
            "generated_by": "Report Generation Service v2.0 (Container)"
        }
        
        return jsonify(summary)
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling student service: {e}")
        return jsonify({"error": "Failed to fetch student data", "details": str(e)}), 500

@app.route('/info')
def get_service_info():
    return jsonify({
        "service": "Report Generation Service",
        "deployment": "Container",
        "version": "2.0.0",
        "environment": ENV,
        "student_service_configured": STUDENT_SERVICE_URL is not None,
        "student_service_url": STUDENT_SERVICE_URL
    })

@app.route('/health')
def health():
    status = {
        "status": "healthy",
        "service": "report-generation",
        "version": "2.0.0",
        "deployment": "container",
        "student_service_configured": STUDENT_SERVICE_URL is not None
    }
    
    # Test connection to student service
    if STUDENT_SERVICE_URL:
        try:
            url = f"{STUDENT_SERVICE_URL}/health"
            response = requests.get(url, timeout=5)
            status["student_service_status"] = "reachable" if response.status_code == 200 else "unreachable"
        except:
            status["student_service_status"] = "unreachable"
    
    return jsonify(status)

if __name__ == '__main__':
    app.logger.info(f"Starting Report Service on port {PORT}")
    app.logger.info(f"Student Service URL: {STUDENT_SERVICE_URL}")
    app.run(host='0.0.0.0', port=PORT, debug=(ENV == 'development'))
```

### `reportservice/requirements.txt`
```
Flask==2.3.3
requests==2.31.0
gunicorn==21.2.0
```

### `reportservice/Dockerfile`
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60", "app:app"]
```

## ✅ Step 4: Local Testing with Docker Compose

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  student-service:
    build: ./studentservice
    ports:
      - "8001:8000"
    environment:
      - ENV=development
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  report-service:
    build: ./reportservice
    ports:
      - "8002:8000"
    environment:
      - ENV=development
      - STUDENT_SERVICE_URL=http://student-service:8000
    depends_on:
      - student-service
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Test Locally
```bash
# Build and run containers locally
docker-compose up -d

# Test services
curl http://localhost:8001/students
curl http://localhost:8002/report/101

# View logs
docker-compose logs student-service
docker-compose logs report-service

# Stop containers
docker-compose down
```

## ✅ Step 5: Build and Push Container Images

### `scripts/build-images.sh`
```bash
#!/bin/bash
set -e

echo "🐳 Building and pushing container images..."
source .env

# Login to ACR
echo "🔐 Logging into ACR..."
az acr login --name $ACR_NAME

# Build and push Student Service
echo "📚 Building Student Service container..."
az acr build \
  --registry $ACR_NAME \
  --image studentservice:v2.0 \
  --image studentservice:latest \
  --file studentservice/Dockerfile \
  studentservice/

# Build and push Report Service
echo "📊 Building Report Service container..."
az acr build \
  --registry $ACR_NAME \
  --image reportservice:v2.0 \
  --image reportservice:latest \
  --file reportservice/Dockerfile \
  reportservice/

echo "✅ Container images built and pushed!"
echo "🐳 Images available at $ACR_NAME.azurecr.io"

# List images
az acr repository list --name $ACR_NAME --output table
```

### Build Images
```bash
./scripts/build-images.sh
```

## ✅ Step 6: Deploy Containers to App Service

### `scripts/deploy-containers.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying containers to App Service..."
source .env

# Create Student Service Web App
echo "📚 Creating Student Service container app..."
az webapp create \
  --resource-group $RG_NAME \
  --plan $APP_SERVICE_PLAN \
  --name $STUDENT_SERVICE_APP \
  --deployment-container-image-name $ACR_NAME.azurecr.io/studentservice:latest

# Configure Student Service
az webapp config appsettings set \
  --resource-group $RG_NAME \
  --name $STUDENT_SERVICE_APP \
  --settings \
    ENV=production \
    PORT=8000

# Set ACR credentials for Student Service
az webapp config container set \
  --name $STUDENT_SERVICE_APP \
  --resource-group $RG_NAME \
  --docker-custom-image-name $ACR_NAME.azurecr.io/studentservice:latest \
  --docker-registry-server-url https://$ACR_NAME.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Create Report Service Web App
echo "📊 Creating Report Service container app..."
az webapp create \
  --resource-group $RG_NAME \
  --plan $APP_SERVICE_PLAN \
  --name $REPORT_SERVICE_APP \
  --deployment-container-image-name $ACR_NAME.azurecr.io/reportservice:latest

# Configure Report Service with Student Service URL
az webapp config appsettings set \
  --resource-group $RG_NAME \
  --name $REPORT_SERVICE_APP \
  --settings \
    ENV=production \
    PORT=8000 \
    STUDENT_SERVICE_URL=https://$STUDENT_SERVICE_APP.azurewebsites.net

# Set ACR credentials for Report Service
az webapp config container set \
  --name $REPORT_SERVICE_APP \
  --resource-group $RG_NAME \
  --docker-custom-image-name $ACR_NAME.azurecr.io/reportservice:latest \
  --docker-registry-server-url https://$ACR_NAME.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

echo "✅ Container deployment complete!"
echo "📚 Student Service: https://$STUDENT_SERVICE_APP.azurewebsites.net"
echo "📊 Report Service: https://$REPORT_SERVICE_APP.azurewebsites.net"

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 60

# Test deployment
echo "🧪 Testing deployment..."
curl -f https://$STUDENT_SERVICE_APP.azurewebsites.net/health || echo "Student service not ready yet"
curl -f https://$REPORT_SERVICE_APP.azurewebsites.net/health || echo "Report service not ready yet"
```

### Deploy Containers
```bash
./scripts/deploy-containers.sh
```

## ✅ Step 7: Test Containerized Services

### Test Container Deployment
```bash
source .env

# Test Student Service
echo "📚 Testing Student Service (Container)..."
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/student/101
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/info

# Test Report Service
echo "📊 Testing Report Service (Container)..."
curl https://$REPORT_SERVICE_APP.azurewebsites.net/
curl https://$REPORT_SERVICE_APP.azurewebsites.net/report/101
curl https://$REPORT_SERVICE_APP.azurewebsites.net/report/summary

# Test Health Endpoints
curl https://$STUDENT_SERVICE_APP.azurewebsites.net/health
curl https://$REPORT_SERVICE_APP.azurewebsites.net/health
```

### Browser Testing
Visit these URLs to compare with Lab 7A:

1. **Student Service Info**: `https://<STUDENT_SERVICE_APP>.azurewebsites.net/info`
2. **Report Service Info**: `https://<REPORT_SERVICE_APP>.azurewebsites.net/info`
3. **Enhanced Report**: `https://<REPORT_SERVICE_APP>.azurewebsites.net/report/101`
4. **Summary Report**: `https://<REPORT_SERVICE_APP>.azurewebsites.net/report/summary`

## ✅ Step 8: Monitor Container Applications

### Container Logs
```bash
# View container logs
az webapp log tail \
  --name $STUDENT_SERVICE_APP \
  --resource-group $RG_NAME

az webapp log tail \
  --name $REPORT_SERVICE_APP \
  --resource-group $RG_NAME
```

### Container Configuration
```bash
# Check container settings
az webapp config container show \
  --name $STUDENT_SERVICE_APP \
  --resource-group $RG_NAME

# Check app settings
az webapp config appsettings list \
  --name $REPORT_SERVICE_APP \
  --resource-group $RG_NAME
```

### Update Container Images
```bash
# Rebuild and redeploy containers
./scripts/build-images.sh

# Restart apps to pull latest images
az webapp restart --name $STUDENT_SERVICE_APP --resource-group $RG_NAME
az webapp restart --name $REPORT_SERVICE_APP --resource-group $RG_NAME
```

## ✅ Step 9: Compare Deployment Methods

### Container vs Code Deployment Benefits

| Aspect | Code Deployment (Lab 7A) | Container Deployment (Lab 7B) |
|--------|---------------------------|--------------------------------|
| **Deployment Speed** | Fast (Git push) | Moderate (Build + Deploy) |
| **Environment Consistency** | Platform-dependent | Identical across environments |
| **Dependency Management** | App Service managed | Container controlled |
| **Version Control** | Git-based | Image tags + Git |
| **Scaling** | App Service scaling | Container + App Service scaling |
| **Development Workflow** | Direct code changes | Build → Test → Deploy |
| **Debugging** | Direct logs | Container logs |
| **Portability** | Azure App Service only | Any container platform |

### Performance Comparison
```bash
# Test response times
time curl https://<student-code-app>.azurewebsites.net/students     # Lab 7A
time curl https://<student-container-app>.azurewebsites.net/students # Lab 7B
```

## ✅ Step 10: Cleanup

### `cleanup.sh`
```bash
#!/bin/bash

echo "🧹 Cleaning up Lab 7B resources..."
source .env

# Delete resource group (removes all resources)
az group delete \
  --name $RG_NAME \
  --yes \
  --no-wait

# Clean up local Docker resources
docker-compose down --volumes --remove-orphans 2>/dev/null || true
docker system prune -f

echo "✅ Cleanup initiated"
echo "🔍 Monitor cleanup: az group list --query \"[?name=='$RG_NAME']\""
```

```bash
chmod +x cleanup.sh
./cleanup.sh
```

## 🎓 Lab Complete

### What You Built
✅ **Containerized Microservices** - Docker containers with proper health checks  
✅ **Azure Container Registry** - Private container image repository  
✅ **Container App Service** - Container-based PaaS deployment  
✅ **Enhanced Service Communication** - Production-ready HTTP communication  
✅ **Multi-stage Deployment** - Local testing → ACR → App Service  

### Key Skills Learned
- Docker containerization for Python Flask applications
- Azure Container Registry creation and image management
- Container-based App Service deployment
- Production-ready container configuration (health checks, non-root users)
- Container orchestration with Docker Compose
- Container monitoring and troubleshooting
- Comparing deployment strategies

### Container Benefits Demonstrated
- **Environment Consistency**: Same container runs locally and in production
- **Dependency Isolation**: All dependencies packaged with application
- **Version Control**: Image tags for precise version management
- **Portability**: Containers can run on any container platform
- **Security**: Non-root users and minimal base images
- **Monitoring**: Built-in health checks and container logs

### Production Advantages
- **Immutable Deployments**: Each deployment uses a specific image version
- **Rollback Capability**: Easy rollback to previous image versions
- **Development Parity**: Same container in dev, staging, and production
- **Resource Efficiency**: Optimized container resource usage
- **Security Scanning**: ACR vulnerability scanning capabilities

### Next Steps (Lab 7C Preview)
In the next lab, you'll automate the entire container build and deployment process using GitHub Actions, creating a complete CI/CD pipeline for production deployments.
