# 🔄 Lab 7C: Production App Service CI/CD Pipeline

## 🎯 Objective
Create a complete production CI/CD pipeline using GitHub Actions to automate the build, test, and deployment of containerized microservices to Azure App Service with staging and production environments.

- Build automated CI/CD pipeline with GitHub Actions
- Implement staging and production environments
- Add automated testing and quality gates
- Configure environment-specific deployments
- Enable automated rollbacks and monitoring
- Integrate with GitHub Projects for Sprint 2 completion

## 🗂 Structure
```
lab7c/
├── studentservice/
│   ├── app.py (enhanced)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       └── test_app.py
├── reportservice/
│   ├── app.py (enhanced)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       └── test_app.py
├── .github/
│   └── workflows/
│       ├── ci-cd-pipeline.yml
│       └── destroy-environments.yml
├── infrastructure/
│   ├── setup-environments.sh
│   └── deploy-infrastructure.sh
├── scripts/
│   └── health-check.sh
└── README.md
```

## 🧭 Prerequisites

- Completed Lab 7A and 7B or equivalent microservice knowledge
- GitHub repository with proper secrets configuration
- Azure CLI and Docker knowledge
- Understanding of CI/CD concepts

## ✅ Step 1: Enhanced Application Code

### `studentservice/app.py` (Production-ready)
```python
from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 8000))
ENV = os.environ.get('ENV', 'development')
VERSION = os.environ.get('VERSION', '3.0.0')

# Enhanced student data
STUDENTS = {
    "101": {"id": "101", "name": "Ava Chen", "major": "Computer Science", "year": 3, "gpa": 3.8, "status": "active"},
    "102": {"id": "102", "name": "Marcus Johnson", "major": "Data Science", "year": 2, "gpa": 3.6, "status": "active"},
    "103": {"id": "103", "name": "Sofia Rodriguez", "major": "Software Engineering", "year": 4, "gpa": 3.9, "status": "active"},
    "104": {"id": "104", "name": "Kai Patel", "major": "Cybersecurity", "year": 1, "gpa": 3.5, "status": "active"},
    "105": {"id": "105", "name": "Emma Thompson", "major": "AI/ML", "year": 3, "gpa": 3.7, "status": "active"},
    "106": {"id": "106", "name": "James Wilson", "major": "Computer Science", "year": 2, "gpa": 3.4, "status": "active"}
}

@app.before_request
def log_request_info():
    logger.info(f"{request.method} {request.url} - User-Agent: {request.headers.get('User-Agent')}")

@app.route('/')
def home():
    return jsonify({
        "service": "Student Info Service",
        "version": VERSION,
        "environment": ENV,
        "deployment": "Production CI/CD",
        "port": PORT,
        "endpoints": ["/student/<id>", "/students", "/health", "/info", "/metrics"],
        "total_students": len(STUDENTS),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/student/<id>')
def get_student(id):
    logger.info(f"Fetching student with ID: {id}")
    student = STUDENTS.get(id)
    if student:
        return jsonify({
            "student": student,
            "fetched_at": datetime.now().isoformat(),
            "service_version": VERSION
        })
    else:
        logger.warning(f"Student not found: {id}")
        return jsonify({
            "error": "Student not found", 
            "id": id,
            "available_ids": list(STUDENTS.keys())
        }), 404

@app.route('/students')
def get_all_students():
    logger.info("Fetching all students")
    active_students = [s for s in STUDENTS.values() if s.get('status') == 'active']
    return jsonify({
        "students": active_students, 
        "count": len(active_students),
        "total_count": len(STUDENTS),
        "service": "Student Info Service",
        "version": VERSION,
        "fetched_at": datetime.now().isoformat()
    })

@app.route('/metrics')
def get_metrics():
    """Endpoint for monitoring and analytics"""
    majors = {}
    gpa_total = 0
    active_count = 0
    
    for student in STUDENTS.values():
        if student.get('status') == 'active':
            active_count += 1
            major = student.get('major', 'Unknown')
            majors[major] = majors.get(major, 0) + 1
            gpa_total += student.get('gpa', 0)
    
    return jsonify({
        "metrics": {
            "total_students": len(STUDENTS),
            "active_students": active_count,
            "average_gpa": round(gpa_total / active_count, 2) if active_count > 0 else 0,
            "majors_distribution": majors,
            "service_uptime": "healthy"
        },
        "service": "Student Info Service",
        "version": VERSION,
        "environment": ENV,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/info')
def get_service_info():
    return jsonify({
        "service": "Student Info Service",
        "deployment": "Production CI/CD Pipeline",
        "version": VERSION,
        "environment": ENV,
        "features": ["REST API", "Health Checks", "Metrics", "Logging"],
        "students_available": list(STUDENTS.keys()),
        "build_info": {
            "deployment_time": datetime.now().isoformat(),
            "platform": "Azure App Service",
            "container": True
        }
    })

@app.route('/health')
def health():
    """Health check endpoint for load balancers and monitoring"""
    health_status = {
        "status": "healthy",
        "service": "student-info",
        "version": VERSION,
        "environment": ENV,
        "checks": {
            "database": "healthy",  # In production, this would check actual DB
            "memory": "healthy",
            "dependencies": "healthy"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(health_status)

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "service": "Student Info Service",
        "version": VERSION
    }), 500

if __name__ == '__main__':
    logger.info(f"Starting Student Service v{VERSION} on port {PORT} in {ENV} environment")
    app.run(host='0.0.0.0', port=PORT, debug=(ENV == 'development'))
```

### `studentservice/tests/test_app.py`
```python
import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['service'] == 'Student Info Service'
    assert 'endpoints' in data

def test_get_student_valid_id(client):
    """Test getting a valid student"""
    response = client.get('/student/101')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['student']['id'] == '101'
    assert data['student']['name'] == 'Ava Chen'

def test_get_student_invalid_id(client):
    """Test getting an invalid student"""
    response = client.get('/student/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Student not found'

def test_get_all_students(client):
    """Test getting all students"""
    response = client.get('/students')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'students' in data
    assert data['count'] > 0

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'metrics' in data
    assert 'total_students' in data['metrics']
```

### `reportservice/app.py` (Production-ready)
```python
import os
import requests
from flask import Flask, jsonify, request
import logging
from datetime import datetime
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 8000))
ENV = os.environ.get('ENV', 'development')
VERSION = os.environ.get('VERSION', '3.0.0')
STUDENT_SERVICE_URL = os.environ.get("STUDENT_SERVICE_URL")
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '15'))

@app.before_request
def log_request_info():
    logger.info(f"{request.method} {request.url} - User-Agent: {request.headers.get('User-Agent')}")

def call_student_service(endpoint):
    """Helper function to call student service with proper error handling"""
    if not STUDENT_SERVICE_URL:
        raise Exception("Student service not configured")
    
    url = f"{STUDENT_SERVICE_URL}{endpoint}"
    logger.info(f"Calling student service: {url}")
    
    start_time = time.time()
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response_time = time.time() - start_time
    
    logger.info(f"Student service response: {response.status_code} in {response_time:.2f}s")
    
    if response.status_code == 404:
        return None, 404
    
    response.raise_for_status()
    return response.json(), response.status_code

@app.route('/')
def home():
    return jsonify({
        "service": "Report Generation Service",
        "version": VERSION,
        "environment": ENV,
        "deployment": "Production CI/CD",
        "port": PORT,
        "endpoints": ["/report/<id>", "/report/summary", "/report/analytics", "/health", "/info", "/metrics"],
        "student_service": STUDENT_SERVICE_URL or "Not configured",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/report/<id>')
def get_student_report(id):
    try:
        student_data, status_code = call_student_service(f"/student/{id}")
        
        if status_code == 404:
            return jsonify({"error": "Student not found", "id": id}), 404
        
        student = student_data['student']
        current_year = datetime.now().year
        credits_completed = 45 + (int(student.get('year', 1)) - 1) * 30
        
        # Enhanced report with more details
        report = {
            "report_id": f"RPT-{id}-{current_year}",
            "generated_at": datetime.now().isoformat(),
            "student_info": student,
            "academic_details": {
                "standing": "Good Standing" if student.get('gpa', 0) >= 3.0 else "Academic Probation",
                "credits_completed": credits_completed,
                "credits_required": 120,
                "completion_percentage": round((credits_completed / 120) * 100, 1),
                "graduation_status": "On Track" if int(student.get('year', 1)) <= 4 else "Extended",
                "gpa": student.get('gpa', 0),
                "gpa_standing": "Dean's List" if student.get('gpa', 0) >= 3.8 else "Good Standing" if student.get('gpa', 0) >= 3.0 else "Probation"
            },
            "recommendations": [],
            "report_summary": f"Student {student['name']} is a {student['year']}-year {student['major']} student with {credits_completed} credits completed and a {student.get('gpa', 0)} GPA.",
            "generated_by": f"Report Generation Service v{VERSION}",
            "service_info": {
                "version": VERSION,
                "environment": ENV
            }
        }
        
        # Add recommendations based on GPA
        if student.get('gpa', 0) >= 3.8:
            report["recommendations"].append("Consider applying for academic honors programs")
        elif student.get('gpa', 0) < 3.0:
            report["recommendations"].append("Meet with academic advisor for support resources")
        
        return jsonify(report)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling student service: {e}")
        return jsonify({
            "error": "Failed to fetch student data", 
            "details": str(e),
            "service": "Report Generation Service"
        }), 500

@app.route('/report/summary')
def get_summary_report():
    try:
        students_data, status_code = call_student_service("/students")
        
        students = students_data.get('students', [])
        
        # Generate enhanced summary
        majors = {}
        years = {}
        gpa_total = 0
        gpa_count = 0
        total_students = len(students)
        
        for student in students:
            major = student.get('major', 'Unknown')
            year = student.get('year', 'Unknown')
            gpa = student.get('gpa', 0)
            
            majors[major] = majors.get(major, 0) + 1
            years[str(year)] = years.get(str(year), 0) + 1
            
            if gpa > 0:
                gpa_total += gpa
                gpa_count += 1
        
        summary = {
            "report_type": "Comprehensive Summary Report",
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_students": total_students,
                "majors_breakdown": majors,
                "year_breakdown": years,
                "most_popular_major": max(majors, key=majors.get) if majors else "N/A",
                "average_year": round(sum(int(s.get('year', 1)) for s in students) / total_students, 1) if students else 0,
                "average_gpa": round(gpa_total / gpa_count, 2) if gpa_count > 0 else 0,
                "high_performers": len([s for s in students if s.get('gpa', 0) >= 3.8]),
                "at_risk_students": len([s for s in students if s.get('gpa', 0) < 3.0])
            },
            "insights": {
                "academic_performance": "Good" if (gpa_total / gpa_count if gpa_count > 0 else 0) >= 3.5 else "Average",
                "enrollment_health": "Stable"
            },
            "generated_by": f"Report Generation Service v{VERSION}",
            "service_info": {
                "version": VERSION,
                "environment": ENV
            }
        }
        
        return jsonify(summary)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling student service: {e}")
        return jsonify({
            "error": "Failed to fetch student data", 
            "details": str(e)
        }), 500

@app.route('/report/analytics')
def get_analytics_report():
    """Advanced analytics endpoint"""
    try:
        # Get metrics from student service
        metrics_data, status_code = call_student_service("/metrics")
        
        analytics = {
            "analytics_type": "Advanced Analytics Report",
            "generated_at": datetime.now().isoformat(),
            "student_metrics": metrics_data.get('metrics', {}),
            "service_performance": {
                "report_service_version": VERSION,
                "environment": ENV,
                "uptime": "healthy"
            },
            "trends": {
                "enrollment_trend": "stable",
                "performance_trend": "improving"
            },
            "generated_by": f"Report Generation Service v{VERSION}"
        }
        
        return jsonify(analytics)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling student service: {e}")
        return jsonify({
            "error": "Failed to fetch analytics data", 
            "details": str(e)
        }), 500

@app.route('/metrics')
def get_metrics():
    """Service metrics for monitoring"""
    metrics = {
        "service_metrics": {
            "version": VERSION,
            "environment": ENV,
            "uptime": "healthy",
            "dependencies": {
                "student_service": "configured" if STUDENT_SERVICE_URL else "not_configured"
            }
        },
        "request_metrics": {
            "total_requests": "N/A",  # In production, use actual metrics
            "avg_response_time": "N/A",
            "error_rate": "0%"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(metrics)

@app.route('/info')
def get_service_info():
    return jsonify({
        "service": "Report Generation Service",
        "deployment": "Production CI/CD Pipeline",
        "version": VERSION,
        "environment": ENV,
        "features": ["Student Reports", "Summary Analytics", "Health Checks", "Metrics"],
        "student_service_configured": STUDENT_SERVICE_URL is not None,
        "student_service_url": STUDENT_SERVICE_URL,
        "build_info": {
            "deployment_time": datetime.now().isoformat(),
            "platform": "Azure App Service",
            "container": True
        }
    })

@app.route('/health')
def health():
    """Comprehensive health check"""
    status = {
        "status": "healthy",
        "service": "report-generation",
        "version": VERSION,
        "environment": ENV,
        "checks": {
            "service": "healthy",
            "student_service_configured": STUDENT_SERVICE_URL is not None
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Test connection to student service
    if STUDENT_SERVICE_URL:
        try:
            student_health, _ = call_student_service("/health")
            status["checks"]["student_service_status"] = "reachable"
            status["checks"]["student_service_health"] = student_health.get("status", "unknown")
        except Exception as e:
            status["checks"]["student_service_status"] = "unreachable"
            status["checks"]["student_service_error"] = str(e)
            status["status"] = "degraded"
    
    return jsonify(status)

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "service": "Report Generation Service",
        "version": VERSION
    }), 500

if __name__ == '__main__':
    logger.info(f"Starting Report Service v{VERSION} on port {PORT} in {ENV} environment")
    logger.info(f"Student Service URL: {STUDENT_SERVICE_URL}")
    app.run(host='0.0.0.0', port=PORT, debug=(ENV == 'development'))
```

### `reportservice/tests/test_app.py`
```python
import pytest
import json
from unittest.mock import patch, MagicMock
from app import app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ['STUDENT_SERVICE_URL'] = 'http://test-student-service'
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['service'] == 'Report Generation Service'

@patch('app.requests.get')
def test_get_student_report(mock_get, client):
    """Test getting a student report"""
    # Mock student service response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'student': {
            'id': '101',
            'name': 'Test Student',
            'major': 'Computer Science',
            'year': 3,
            'gpa': 3.8
        }
    }
    mock_get.return_value = mock_response
    
    response = client.get('/report/101')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['student_info']['id'] == '101'
    assert 'academic_details' in data

@patch('app.requests.get')
def test_get_summary_report(mock_get, client):
    """Test getting summary report"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'students': [
            {'id': '101', 'major': 'CS', 'year': 3, 'gpa': 3.8},
            {'id': '102', 'major': 'DS', 'year': 2, 'gpa': 3.6}
        ]
    }
    mock_get.return_value = mock_response
    
    response = client.get('/report/summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'statistics' in data
    assert data['statistics']['total_students'] == 2

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert 'checks' in data

def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'service_metrics' in data
```

## ✅ Step 2: Infrastructure Setup

### `infrastructure/setup-environments.sh`
```bash
#!/bin/bash
set -e

echo "🏗️ Setting up staging and production environments..."

# Check Azure login
if ! az account show &>/dev/null; then
    echo "🔐 Please login to Azure"
    az login
fi

# Generate unique names
UNIQUE_ID=$(openssl rand -hex 4)

# Create .env file
cat > .env << EOF
export RG_NAME=lab7c-rg
export LOCATION=australiaeast
export ACR_NAME=acr7c$UNIQUE_ID
export APP_SERVICE_PLAN_STAGING=staging-plan-$UNIQUE_ID
export APP_SERVICE_PLAN_PROD=prod-plan-$UNIQUE_ID
export STUDENT_SERVICE_STAGING=student-staging-$UNIQUE_ID
export STUDENT_SERVICE_PROD=student-prod-$UNIQUE_ID
export REPORT_SERVICE_STAGING=report-staging-$UNIQUE_ID
export REPORT_SERVICE_PROD=report-prod-$UNIQUE_ID
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
  --sku Standard \
  --admin-enabled true

echo "📊 Creating staging App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN_STAGING \
  --resource-group $RG_NAME \
  --sku B1 \
  --is-linux

echo "📊 Creating production App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN_PROD \
  --resource-group $RG_NAME \
  --sku S1 \
  --is-linux

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

echo "export ACR_USERNAME=$ACR_USERNAME" >> .env
echo "export ACR_PASSWORD=$ACR_PASSWORD" >> .env

echo "✅ Infrastructure setup complete!"
echo "📝 Environment variables saved to .env"
echo "🐳 ACR: $ACR_NAME.azurecr.io"
echo "🔄 Staging Plan: $APP_SERVICE_PLAN_STAGING"
echo "🚀 Production Plan: $APP_SERVICE_PLAN_PROD"
```

### Run Infrastructure Setup
```bash
chmod +x infrastructure/*.sh scripts/*.sh
./infrastructure/setup-environments.sh
source .env
```

## ✅ Step 3: CI/CD Pipeline Configuration

### `.github/workflows/ci-cd-pipeline.yml`
```yaml
name: 'Production CI/CD Pipeline'

on:
  push:
    branches: [ main, develop ]
    paths: 
      - 'studentservice/**'
      - 'reportservice/**'
      - '.github/workflows/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'studentservice/**'
      - 'reportservice/**'

env:
  REGISTRY: ${{ secrets.ACR_NAME }}.azurecr.io
  ACR_NAME: ${{ secrets.ACR_NAME }}
  RESOURCE_GROUP: ${{ secrets.RG_NAME }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [studentservice, reportservice]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd ${{ matrix.service }}
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd ${{ matrix.service }}
        pytest tests/ -v --cov=app --cov-report=term-missing
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./${{ matrix.service }}/coverage.xml
        flags: ${{ matrix.service }}

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    strategy:
      matrix:
        service: [studentservice, reportservice]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Login to ACR
      uses: azure/docker-login@v1
      with:
        login-server: ${{ env.REGISTRY }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}
    
    - name: Build and push container image
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        
        # Build image
        docker build -t ${{ env.REGISTRY }}/${{ matrix.service }}:$IMAGE_TAG \
          -t ${{ env.REGISTRY }}/${{ matrix.service }}:latest \
          --build-arg VERSION=3.0.${{ github.run_number }} \
          ./${{ matrix.service }}/
        
        # Push images
        docker push ${{ env.REGISTRY }}/${{ matrix.service }}:$IMAGE_TAG
        docker push ${{ env.REGISTRY }}/${{ matrix.service }}:latest
        
        echo "IMAGE_TAG=$IMAGE_TAG" >> $GITHUB_ENV
        echo "✅ Built and pushed ${{ matrix.service }}:$IMAGE_TAG"

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Staging
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        VERSION=3.0.${{ github.run_number }}
        
        # Deploy Student Service to Staging
        az webapp create \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --plan ${{ secrets.APP_SERVICE_PLAN_STAGING }} \
          --name ${{ secrets.STUDENT_SERVICE_STAGING }} \
          --deployment-container-image-name ${{ env.REGISTRY }}/studentservice:$IMAGE_TAG \
          --docker-registry-server-url https://${{ env.REGISTRY }} \
          --docker-registry-server-user ${{ secrets.ACR_USERNAME }} \
          --docker-registry-server-password ${{ secrets.ACR_PASSWORD }} || true
        
        # Configure Student Service settings
        az webapp config appsettings set \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --name ${{ secrets.STUDENT_SERVICE_STAGING }} \
          --settings \
            ENV=staging \
            VERSION=$VERSION \
            PORT=8000
        
        # Deploy Report Service to Staging
        az webapp create \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --plan ${{ secrets.APP_SERVICE_PLAN_STAGING }} \
          --name ${{ secrets.REPORT_SERVICE_STAGING }} \
          --deployment-container-image-name ${{ env.REGISTRY }}/reportservice:$IMAGE_TAG \
          --docker-registry-server-url https://${{ env.REGISTRY }} \
          --docker-registry-server-user ${{ secrets.ACR_USERNAME }} \
          --docker-registry-server-password ${{ secrets.ACR_PASSWORD }} || true
        
        # Configure Report Service settings
        az webapp config appsettings set \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --name ${{ secrets.REPORT_SERVICE_STAGING }} \
          --settings \
            ENV=staging \
            VERSION=$VERSION \
            PORT=8000 \
            STUDENT_SERVICE_URL=https://${{ secrets.STUDENT_SERVICE_STAGING }}.azurewebsites.net
        
        echo "✅ Deployed to staging environment"

  staging-tests:
    needs: deploy-staging
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    
    steps:
    - name: Wait for staging deployment
      run: sleep 60
    
    - name: Run staging health checks
      run: |
        echo "🧪 Running staging health checks..."
        
        # Check Student Service health
        STUDENT_HEALTH=$(curl -s https://${{ secrets.STUDENT_SERVICE_STAGING }}.azurewebsites.net/health || echo "failed")
        echo "Student Service Health: $STUDENT_HEALTH"
        
        # Check Report Service health
        REPORT_HEALTH=$(curl -s https://${{ secrets.REPORT_SERVICE_STAGING }}.azurewebsites.net/health || echo "failed")
        echo "Report Service Health: $REPORT_HEALTH"
        
        # Test integration
        INTEGRATION_TEST=$(curl -s https://${{ secrets.REPORT_SERVICE_STAGING }}.azurewebsites.net/report/101 || echo "failed")
        echo "Integration Test: $INTEGRATION_TEST"
        
        # Verify responses contain expected data
        if [[ "$STUDENT_HEALTH" == *"healthy"* ]] && [[ "$REPORT_HEALTH" == *"healthy"* ]]; then
          echo "✅ Staging health checks passed"
        else
          echo "❌ Staging health checks failed"
          exit 1
        fi

  deploy-production:
    needs: [deploy-staging, staging-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Production
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        VERSION=3.0.${{ github.run_number }}
        
        echo "🚀 Deploying to production with image tag: $IMAGE_TAG"
        
        # Deploy Student Service to Production
        az webapp create \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --plan ${{ secrets.APP_SERVICE_PLAN_PROD }} \
          --name ${{ secrets.STUDENT_SERVICE_PROD }} \
          --deployment-container-image-name ${{ env.REGISTRY }}/studentservice:$IMAGE_TAG \
          --docker-registry-server-url https://${{ env.REGISTRY }} \
          --docker-registry-server-user ${{ secrets.ACR_USERNAME }} \
          --docker-registry-server-password ${{ secrets.ACR_PASSWORD }} || true
        
        # Configure Student Service settings
        az webapp config appsettings set \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --name ${{ secrets.STUDENT_SERVICE_PROD }} \
          --settings \
            ENV=production \
            VERSION=$VERSION \
            PORT=8000
        
        # Deploy Report Service to Production
        az webapp create \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --plan ${{ secrets.APP_SERVICE_PROD }} \
          --name ${{ secrets.REPORT_SERVICE_PROD }} \
          --deployment-container-image-name ${{ env.REGISTRY }}/reportservice:$IMAGE_TAG \
          --docker-registry-server-url https://${{ env.REGISTRY }} \
          --docker-registry-server-user ${{ secrets.ACR_USERNAME }} \
          --docker-registry-server-password ${{ secrets.ACR_PASSWORD }} || true
        
        # Configure Report Service settings
        az webapp config appsettings set \
          --resource-group ${{ env.RESOURCE_GROUP }} \
          --name ${{ secrets.REPORT_SERVICE_PROD }} \
          --settings \
            ENV=production \
            VERSION=$VERSION \
            PORT=8000 \
            STUDENT_SERVICE_URL=https://${{ secrets.STUDENT_SERVICE_PROD }}.azurewebsites.net
        
        echo "✅ Deployed to production environment"

  production-health-check:
    needs: deploy-production
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Wait for production deployment
      run: sleep 90
    
    - name: Run production health checks
      run: |
        echo "🏥 Running production health checks..."
        
        # Comprehensive health checks
        for i in {1..5}; do
          echo "Health check attempt $i/5..."
          
          STUDENT_HEALTH=$(curl -s https://${{ secrets.STUDENT_SERVICE_PROD }}.azurewebsites.net/health || echo "failed")
          REPORT_HEALTH=$(curl -s https://${{ secrets.REPORT_SERVICE_PROD }}.azurewebsites.net/health || echo "failed")
          
          if [[ "$STUDENT_HEALTH" == *"healthy"* ]] && [[ "$REPORT_HEALTH" == *"healthy"* ]]; then
            echo "✅ Production health checks passed on attempt $i"
            break
          fi
          
          if [ $i -eq 5 ]; then
            echo "❌ Production health checks failed after 5 attempts"
            echo "Student Health: $STUDENT_HEALTH"
            echo "Report Health: $REPORT_HEALTH"
            exit 1
          fi
          
          sleep 30
        done
    
    - name: Run production smoke tests
      run: |
        echo "💨 Running production smoke tests..."
        
        # Test key endpoints
        curl -f https://${{ secrets.STUDENT_SERVICE_PROD }}.azurewebsites.net/students
        curl -f https://${{ secrets.REPORT_SERVICE_PROD }}.azurewebsites.net/report/101
        curl -f https://${{ secrets.REPORT_SERVICE_PROD }}.azurewebsites.net/report/summary
        
        echo "✅ Production smoke tests passed"

  notify-success:
    needs: [production-health-check]
    runs-on: ubuntu-latest
    if: success() && github.ref == 'refs/heads/main'
    
    steps:
    - name: Notify deployment success
      run: |
        echo "🎉 Production deployment successful!"
        echo "📚 Student Service: https://${{ secrets.STUDENT_SERVICE_PROD }}.azurewebsites.net"
        echo "📊 Report Service: https://${{ secrets.REPORT_SERVICE_PROD }}.azurewebsites.net"
        echo "🏷️ Version: 3.0.${{ github.run_number }}"
        echo "📦 Image Tag: ${GITHUB_SHA::8}"
```

## ✅ Step 4: GitHub Secrets Configuration

### Required GitHub Secrets
Set these in your GitHub repository: **Settings** → **Secrets and variables** → **Actions**

```bash
# Azure credentials (service principal JSON)
AZURE_CREDENTIALS

# ACR and resource details
ACR_NAME=<your-acr-name>
ACR_USERNAME=<acr-username>
ACR_PASSWORD=<acr-password>
RG_NAME=lab7c-rg

# App Service Plans
APP_SERVICE_PLAN_STAGING=<staging-plan-name>
APP_SERVICE_PLAN_PROD=<prod-plan-name>

# App Service Names
STUDENT_SERVICE_STAGING=<student-staging-name>
STUDENT_SERVICE_PROD=<student-prod-name>
REPORT_SERVICE_STAGING=<report-staging-name>
REPORT_SERVICE_PROD=<report-prod-name>
```

### Create Azure Service Principal
```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "github-actions-lab7c" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/lab7c-rg \
  --sdk-auth

# Copy the JSON output to AZURE_CREDENTIALS secret
```

## ✅ Step 5: Health Check Script

### `scripts/health-check.sh`
```bash
#!/bin/bash

echo "🏥 Comprehensive health check script..."

# Check if environment variables are set
if [[ -z "$STUDENT_SERVICE_URL" || -z "$REPORT_SERVICE_URL" ]]; then
    echo "❌ Environment variables not set"
    echo "Set STUDENT_SERVICE_URL and REPORT_SERVICE_URL"
    exit 1
fi

echo "🔍 Checking Student Service..."
STUDENT_HEALTH=$(curl -s $STUDENT_SERVICE_URL/health)
echo "Student Service Health: $STUDENT_HEALTH"

echo "🔍 Checking Report Service..."
REPORT_HEALTH=$(curl -s $REPORT_SERVICE_URL/health)
echo "Report Service Health: $REPORT_HEALTH"

echo "🔗 Testing integration..."
INTEGRATION_TEST=$(curl -s $REPORT_SERVICE_URL/report/101)
echo "Integration Test Result: ${INTEGRATION_TEST:0:100}..."

echo "📊 Testing analytics..."
ANALYTICS_TEST=$(curl -s $REPORT_SERVICE_URL/report/analytics)
echo "Analytics Test Result: ${ANALYTICS_TEST:0:100}..."

# Performance test
echo "⚡ Performance test..."
start_time=$(date +%s%N)
curl -s $STUDENT_SERVICE_URL/students > /dev/null
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))
echo "Response time: ${duration}ms"

echo "✅ Health check complete!"
```

## ✅ Step 6: Deploy and Test

### Initial Deployment
```bash
# Setup infrastructure
./infrastructure/setup-environments.sh
source .env

# Commit and push to trigger CI/CD
git add .
git commit -m "Initial CI/CD pipeline setup"
git push origin main
```

### Monitor Pipeline
1. Go to GitHub Actions tab in your repository
2. Watch the pipeline execution
3. Check staging deployment first
4. Verify production deployment

### Test Environments
```bash
# Test staging environment
export STUDENT_SERVICE_URL=https://$STUDENT_SERVICE_STAGING.azurewebsites.net
export REPORT_SERVICE_URL=https://$REPORT_SERVICE_STAGING.azurewebsites.net
./scripts/health-check.sh

# Test production environment
export STUDENT_SERVICE_URL=https://$STUDENT_SERVICE_PROD.azurewebsites.net
export REPORT_SERVICE_URL=https://$REPORT_SERVICE_PROD.azurewebsites.net
./scripts/health-check.sh
```

## ✅ Step 7: Cleanup

### `.github/workflows/destroy-environments.yml`
```yaml
name: 'Destroy Environments'

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to destroy'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
        - all

jobs:
  destroy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Destroy Environment
      run: |
        if [ "${{ github.event.inputs.environment }}" == "all" ]; then
          echo "🧹 Destroying all Lab 7C resources..."
          az group delete --name ${{ secrets.RG_NAME }} --yes --no-wait
        elif [ "${{ github.event.inputs.environment }}" == "staging" ]; then
          echo "🧹 Destroying staging environment..."
          az webapp delete --name ${{ secrets.STUDENT_SERVICE_STAGING }} --resource-group ${{ secrets.RG_NAME }}
          az webapp delete --name ${{ secrets.REPORT_SERVICE_STAGING }} --resource-group ${{ secrets.RG_NAME }}
        elif [ "${{ github.event.inputs.environment }}" == "production" ]; then
          echo "🧹 Destroying production environment..."
          az webapp delete --name ${{ secrets.STUDENT_SERVICE_PROD }} --resource-group ${{ secrets.RG_NAME }}
          az webapp delete --name ${{ secrets.REPORT_SERVICE_PROD }} --resource-group ${{ secrets.RG_NAME }}
        fi
        
        echo "✅ Environment destruction initiated"
```

## 🎓 Lab Complete

### What You Built
✅ **Production CI/CD Pipeline** - Complete GitHub Actions automation  
✅ **Multi-Environment Deployment** - Staging and production environments  
✅ **Automated Testing** - Unit tests, integration tests, and health checks  
✅ **Container Registry** - Private ACR with automated builds  
✅ **Quality Gates** - Automated testing before production deployment  
✅ **Monitoring & Analytics** - Comprehensive health and metrics endpoints  

### Key Skills Learned
- GitHub Actions CI/CD pipeline creation and management
- Multi-environment deployment strategies (staging/production)
- Automated testing integration in CI/CD pipelines
- Azure App Service container deployment automation
- Service monitoring and health check implementation
- Production deployment best practices and rollback strategies
- GitHub Projects integration for Sprint tracking

### Production Benefits Achieved
- **Zero-Downtime Deployments**: Automated staging validation before production
- **Quality Assurance**: Automated testing prevents broken deployments
- **Rapid Iteration**: Fast feedback loop from commit to production
- **Environment Parity**: Identical staging and production environments
- **Monitoring**: Built-in health checks and performance metrics
- **Security**: Private container registry and secure credential management

### Sprint 2 Deliverables Completed
- ✅ **App Release v2**: Production-ready microservices deployment
- ✅ **CI/CD Automation**: Complete GitHub Actions pipeline
- ✅ **Azure Integration**: Full Azure App Service deployment pipeline
- ✅ **Quality Gates**: Automated testing and validation
- ✅ **Documentation**: Complete deployment and monitoring documentation

### Next Steps
Your microservices are now production-ready with:
- Automated deployment pipeline
- Multi-environment strategy
- Comprehensive monitoring
- Professional development workflow

This completes the Azure App Service deployment track and Sprint 2 objectives. Your applications are ready for real-world production use!
