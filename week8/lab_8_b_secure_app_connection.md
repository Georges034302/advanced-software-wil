# 🔐 Lab 8B: Secure Application Database Connection

## 🎯 Objective
Connect a simple Flask application to Azure SQL Database using secure environment variables and GitHub Secrets.

- Create a minimal Flask app with database operations
- Use environment variables for database connection
- Configure GitHub Secrets for secure credentials
- Test CRUD operations with the students table

## 🗂 Structure
```
lab8b/
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

## ✅ Step 1: Simple Flask Application

### `app.py`
```python
import os
import pyodbc
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Database configuration from environment variables
DB_SERVER = os.environ.get('SQL_SERVER')
DB_DATABASE = os.environ.get('SQL_DATABASE') 
DB_USERNAME = os.environ.get('SQL_USERNAME')
DB_PASSWORD = os.environ.get('SQL_PASSWORD')

def get_db_connection():
    """Create database connection"""
    connection_string = f"""
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={DB_SERVER};
    DATABASE={DB_DATABASE};
    UID={DB_USERNAME};
    PWD={DB_PASSWORD};
    Encrypt=yes;
    TrustServerCertificate=yes;
    """
    return pyodbc.connect(connection_string)

@app.route('/')
def home():
    return jsonify({
        "service": "Student Database Service",
        "status": "running",
        "database": DB_DATABASE,
        "server": DB_SERVER,
        "endpoints": ["/students", "/student", "/health"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
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
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/student', methods=['POST'])
def add_student():
    """Add a new student"""
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
            "timestamp": datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student"""
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
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check with database connectivity test"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "students_count": count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected", 
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Check if required environment variables are set
    required_vars = ['SQL_SERVER', 'SQL_DATABASE', 'SQL_USERNAME', 'SQL_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set all required database environment variables")
        exit(1)
    
    print(f"🗄️ Connecting to database: {DB_DATABASE} on {DB_SERVER}")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### `requirements.txt`
```
Flask==3.0.0
pyodbc==5.0.1
python-dotenv==1.0.0
```

### `.env.example`
```env
# Azure SQL Database Configuration
SQL_SERVER=your-server.database.windows.net
SQL_DATABASE=studentsdb
SQL_USERNAME=sqladmin
SQL_PASSWORD=YourStrongPassword123!
```

## ✅ Step 2: Local Testing Setup

### Create `.env` file
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual database credentials from Lab 8A
# Use the connection details from your Lab 8A deployment
```

### Install Dependencies and Test Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Load environment variables and run app
python -m dotenv run python app.py

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/students
```

### Test Adding Students
```bash
# Add a new student
curl -X POST http://localhost:5000/student \
  -H "Content-Type: application/json" \
  -d '{"name": "David Wilson", "email": "david@university.edu"}'

# Get all students
curl http://localhost:5000/students

# Get specific student
curl http://localhost:5000/student/1
```

## ✅ Step 3: GitHub Repository Setup

### Add Lab Files to Repository
```bash
# Add new lab files to your existing repository
git add .
git commit -m "Add Lab 8B: Flask SQL app with secure connection"
git push origin main
```

### Configure GitHub Secrets (for Lab 8C)
Go to your GitHub repository: **Settings** → **Secrets and variables** → **Actions**

Add these secrets (we'll use them in Lab 8C):
```
SQL_SERVER = your-server.database.windows.net
SQL_DATABASE = studentsdb  
SQL_USERNAME = sqladmin
SQL_PASSWORD = YourStrongPassword123!
```

## ✅ Step 4: Deploy to Azure App Service (Optional)

### `deploy.sh`
```bash
#!/bin/bash
set -e

# Configuration
RG_NAME="lab8b-rg"
APP_NAME="lab8b-app-$(openssl rand -hex 4)"
LOCATION="australiaeast"

echo "🚀 Deploying Flask app to Azure App Service..."

# Create resource group
az group create --name $RG_NAME --location $LOCATION

# Create App Service plan
az appservice plan create \
  --resource-group $RG_NAME \
  --name lab8b-plan \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group $RG_NAME \
  --plan lab8b-plan \
  --name $APP_NAME \
  --runtime "PYTHON:3.11"

# Configure app settings with database credentials
az webapp config appsettings set \
  --resource-group $RG_NAME \
  --name $APP_NAME \
  --settings \
    SQL_SERVER="$SQL_SERVER" \
    SQL_DATABASE="$SQL_DATABASE" \
    SQL_USERNAME="$SQL_USERNAME" \
    SQL_PASSWORD="$SQL_PASSWORD"

# Deploy code
az webapp up \
  --resource-group $RG_NAME \
  --name $APP_NAME \
  --runtime "PYTHON:3.11"

echo "✅ App deployed to: https://$APP_NAME.azurewebsites.net"
```

## ✅ Step 5: Testing

### Test All Endpoints
```bash
# Set your app URL
APP_URL="http://localhost:5000"  # or your Azure App Service URL

# Test home
curl $APP_URL/

# Test health check
curl $APP_URL/health

# Get all students
curl $APP_URL/students

# Add a student
curl -X POST $APP_URL/student \
  -H "Content-Type: application/json" \
  -d '{"name": "Emma Davis", "email": "emma@university.edu"}'

# Get specific student
curl $APP_URL/student/1
```

### Verify Database
Use Azure Portal Query Editor to check the data:
```sql
SELECT * FROM students ORDER BY created_at DESC;
```

## ✅ Step 6: Cleanup

### Delete Resources
```bash
# Delete App Service resources (if deployed)
az group delete --name lab8b-rg --yes --no-wait

# Keep the database from Lab 8A for Lab 8C
```

## 🎓 Lab Complete

### What You Built
✅ **Flask Application** - Simple web API with database operations  
✅ **Secure Configuration** - Environment variables and GitHub Secrets setup  
✅ **CRUD Operations** - Create, Read operations for students  
✅ **Health Checks** - Database connectivity monitoring  
✅ **Local Testing** - Complete local development setup  

### Key Skills Learned
- Flask application development with SQL Server
- Secure database credential management
- Environment variable configuration
- ODBC connection string setup
- GitHub Secrets preparation for CI/CD
- Basic CRUD API development
- Database connectivity testing

### Security Features
- **No Hardcoded Credentials**: All secrets in environment variables
- **GitHub Secrets**: Prepared for secure CI/CD credential storage
- **Encrypted Connections**: TLS encryption to Azure SQL
- **Error Handling**: Safe error messages without credential exposure

The application is now ready for CI/CD automation in Lab 8C!
