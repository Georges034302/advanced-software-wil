# 🔄 Lab 8C: CI/CD Pipeline with Database Schema Management

## 🎯 Objective
Create a simple CI/CD pipeline that automatically manages database schema and deploys the Flask application with GitHub Actions.

- Automate database schema creation/updates
- Deploy Flask app with CI/CD pipeline
- Use GitHub Secrets for secure database access
- Automated testing and deployment

## 🗂 Structure
```
lab8c/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── scripts/
│   ├── setup-database.sh
│   ├── test-connection.sh
│   ├── test-database.py
│   └── deploy-app.sh
├── sql/
│   ├── schema.sql
│   └── seed-data.sql
├── app.py (from Lab 8B)
├── requirements.txt (from Lab 8B)
└── README.md
```

## ✅ Step 1: Database Schema Scripts

### `sql/schema.sql`
```sql
-- Create students table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='students' AND xtype='U')
BEGIN
    CREATE TABLE students (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        email NVARCHAR(100) UNIQUE NOT NULL,
        created_at DATETIME DEFAULT GETDATE()
    );
    PRINT 'Students table created successfully';
END
ELSE
BEGIN
    PRINT 'Students table already exists';
END;

-- Add index on email if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='IX_students_email')
BEGIN
    CREATE INDEX IX_students_email ON students(email);
    PRINT 'Email index created successfully';
END
ELSE
BEGIN
    PRINT 'Email index already exists';
END;
```

### `sql/seed-data.sql`
```sql
-- Insert seed data only if table is empty
IF (SELECT COUNT(*) FROM students) = 0
BEGIN
    INSERT INTO students (name, email) VALUES
    ('Alice Johnson', 'alice@university.edu'),
    ('Bob Smith', 'bob@university.edu'),
    ('Carol Davis', 'carol@university.edu'),
    ('David Wilson', 'david@university.edu');
    
    PRINT 'Seed data inserted successfully';
END
ELSE
BEGIN
    PRINT 'Students table already contains data';
END;

-- Show current student count
SELECT COUNT(*) as total_students FROM students;
```

## ✅ Step 2: Database Setup Script

### `scripts/setup-database.sh`
```bash
#!/bin/bash
set -e

echo "🗄️ Setting up database schema..."

# Install sqlcmd
echo "📦 Installing SQL Server tools..."
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update
sudo apt-get install -y mssql-tools unixodbc-dev

# Add sqlcmd to PATH
export PATH="$PATH:/opt/mssql-tools/bin"

# Run schema script
echo "🗄️ Creating database schema..."
sqlcmd -S $SQL_SERVER \
  -d $SQL_DATABASE \
  -U $SQL_USERNAME \
  -P $SQL_PASSWORD \
  -i sql/schema.sql \
  -o schema-output.log

echo "📋 Schema script output:"
cat schema-output.log

# Run seed data script
echo "🌱 Adding seed data..."
sqlcmd -S $SQL_SERVER \
  -d $SQL_DATABASE \
  -U $SQL_USERNAME \
  -P $SQL_PASSWORD \
  -i sql/seed-data.sql \
  -o seed-output.log

echo "📋 Seed data script output:"
cat seed-output.log

echo "✅ Database setup completed successfully"
```

## ✅ Step 3: Database Test Script

### `scripts/test-database.py`
```python
#!/usr/bin/env python3
"""
Database connection and schema validation test script.
Tests Azure SQL Database connectivity and validates table structure.
"""

import os
import sys
import pyodbc
from datetime import datetime


def test_database_connection():
    """Test basic database connectivity."""
    print("🔗 Testing database connection...")
    
    # Get connection parameters from environment
    server = os.environ.get('SQL_SERVER')
    database = os.environ.get('SQL_DATABASE')
    username = os.environ.get('SQL_USERNAME')
    password = os.environ.get('SQL_PASSWORD')
    
    if not all([server, database, username, password]):
        print("❌ Missing required environment variables")
        return False
    
    connection_string = f"""
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    Encrypt=yes;
    TrustServerCertificate=yes;
    """
    
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Test basic connectivity
        cursor.execute("SELECT GETDATE() as current_time")
        result = cursor.fetchone()
        print(f"✅ Database connection successful at {result[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_students_table():
    """Test students table structure and data."""
    print("🗄️ Testing students table...")
    
    connection_string = f"""
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={os.environ['SQL_SERVER']};
    DATABASE={os.environ['SQL_DATABASE']};
    UID={os.environ['SQL_USERNAME']};
    PWD={os.environ['SQL_PASSWORD']};
    Encrypt=yes;
    TrustServerCertificate=yes;
    """
    
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'students'
        """)
        
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            print("❌ Students table does not exist")
            conn.close()
            return False
        
        # Get student count
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        print(f"📊 Students table contains {count} records")
        
        # Validate table structure
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'students'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        print("📋 Table structure:")
        expected_columns = ['id', 'name', 'email', 'created_at']
        
        for i, col in enumerate(columns):
            column_name, data_type, is_nullable = col
            print(f"  - {column_name}: {data_type} ({'NULL' if is_nullable == 'YES' else 'NOT NULL'})")
            
            if i < len(expected_columns) and column_name != expected_columns[i]:
                print(f"⚠️  Warning: Expected column '{expected_columns[i]}' but found '{column_name}'")
        
        # Test sample data
        if count > 0:
            cursor.execute("SELECT TOP 3 id, name, email FROM students ORDER BY created_at")
            samples = cursor.fetchall()
            print("📄 Sample data:")
            for sample in samples:
                print(f"  - ID {sample[0]}: {sample[1]} ({sample[2]})")
        
        conn.close()
        print("✅ Students table validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Students table test failed: {e}")
        return False


def test_indexes():
    """Test database indexes."""
    print("🔍 Testing database indexes...")
    
    connection_string = f"""
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={os.environ['SQL_SERVER']};
    DATABASE={os.environ['SQL_DATABASE']};
    UID={os.environ['SQL_USERNAME']};
    PWD={os.environ['SQL_PASSWORD']};
    Encrypt=yes;
    TrustServerCertificate=yes;
    """
    
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.name as index_name, i.type_desc
            FROM sys.indexes i
            INNER JOIN sys.objects o ON i.object_id = o.object_id
            WHERE o.name = 'students' AND i.name IS NOT NULL
        """)
        
        indexes = cursor.fetchall()
        print("📇 Indexes found:")
        for index in indexes:
            print(f"  - {index[0]}: {index[1]}")
        
        conn.close()
        print("✅ Index validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Index test failed: {e}")
        return False


def main():
    """Run all database tests."""
    print("🧪 Starting database tests...")
    print(f"⏰ Test started at: {datetime.now().isoformat()}")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Students Table", test_students_table),
        ("Database Indexes", test_indexes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All database tests passed successfully!")
        return True
    else:
        print("❌ Some database tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

## ✅ Step 4: Updated Connection Test Script

### `scripts/test-connection.sh`
```bash
#!/bin/bash
set -e

echo "🧪 Testing database connection and Flask application..."

# Run database tests using Python script
echo "🗄️ Running database connectivity tests..."
python scripts/test-database.py

echo "🌐 Testing Flask app startup..."
timeout 10s python app.py &
sleep 5

# Test Flask endpoints
echo "🔍 Testing Flask endpoints..."
curl -f http://localhost:5000/health || { echo "❌ Health check failed"; exit 1; }
curl -f http://localhost:5000/students || { echo "❌ Students endpoint failed"; exit 1; }

echo "✅ All tests passed successfully"
```

## ✅ Step 5: Deployment Script

### `scripts/deploy-app.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying Flask app to Azure App Service..."

# Generate unique app name using GitHub SHA
APP_NAME="lab8c-app-$(echo $GITHUB_SHA | cut -c1-8)"
RG_NAME="lab8c-rg"
PLAN_NAME="lab8c-plan"
LOCATION="australiaeast"

echo "📦 App name: $APP_NAME"

# Create resource group (idempotent)
echo "📁 Creating/updating resource group..."
az group create --name $RG_NAME --location $LOCATION

# Create App Service plan (idempotent)
echo "📊 Creating/updating App Service plan..."
az appservice plan create \
  --resource-group $RG_NAME \
  --name $PLAN_NAME \
  --sku B1 \
  --is-linux || echo "App Service plan already exists"

# Create or update web app
echo "🌐 Creating/updating web app..."
az webapp create \
  --resource-group $RG_NAME \
  --plan $PLAN_NAME \
  --name $APP_NAME \
  --runtime "PYTHON:3.11" || \
az webapp config set \
  --resource-group $RG_NAME \
  --name $APP_NAME \
  --startup-file "python app.py"

# Configure app settings with database credentials
echo "⚙️ Configuring app settings..."
az webapp config appsettings set \
  --resource-group $RG_NAME \
  --name $APP_NAME \
  --settings \
    SQL_SERVER="$SQL_SERVER" \
    SQL_DATABASE="$SQL_DATABASE" \
    SQL_USERNAME="$SQL_USERNAME" \
    SQL_PASSWORD="$SQL_PASSWORD"

# Deploy application code
echo "📤 Deploying application code..."
az webapp up \
  --resource-group $RG_NAME \
  --name $APP_NAME \
  --runtime "PYTHON:3.11"

# Set the app URL for health checks
APP_URL="https://$APP_NAME.azurewebsites.net"
echo "✅ Deployed to: $APP_URL"

# Export for GitHub Actions
echo "APP_URL=$APP_URL" >> $GITHUB_ENV

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
sleep 30

# Health check with retries
echo "🏥 Running health checks..."
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
  
  echo "Retrying in 10 seconds..."
  sleep 10
done

# Test application endpoints
echo "🧪 Testing application endpoints..."
curl -f $APP_URL/ || { echo "❌ Home endpoint failed"; exit 1; }
curl -f $APP_URL/students || { echo "❌ Students endpoint failed"; exit 1; }

echo "✅ Deployment and verification completed successfully"
echo "🌐 Application URL: $APP_URL"
```

## ✅ Step 6: Clean CI/CD Pipeline

### `.github/workflows/ci-cd.yml`
```yaml
name: CI/CD Pipeline with Database

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'

jobs:
  database-setup:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Database Schema
      env:
        SQL_SERVER: ${{ secrets.SQL_SERVER }}
        SQL_DATABASE: ${{ secrets.SQL_DATABASE }}
        SQL_USERNAME: ${{ secrets.SQL_USERNAME }}
        SQL_PASSWORD: ${{ secrets.SQL_PASSWORD }}
      run: |
        chmod +x scripts/setup-database.sh
        ./scripts/setup-database.sh

  test:
    needs: database-setup
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Test database and application
      env:
        SQL_SERVER: ${{ secrets.SQL_SERVER }}
        SQL_DATABASE: ${{ secrets.SQL_DATABASE }}
        SQL_USERNAME: ${{ secrets.SQL_USERNAME }}
        SQL_PASSWORD: ${{ secrets.SQL_PASSWORD }}
      run: |
        chmod +x scripts/test-connection.sh
        ./scripts/test-connection.sh

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Azure App Service
      env:
        SQL_SERVER: ${{ secrets.SQL_SERVER }}
        SQL_DATABASE: ${{ secrets.SQL_DATABASE }}
        SQL_USERNAME: ${{ secrets.SQL_USERNAME }}
        SQL_PASSWORD: ${{ secrets.SQL_PASSWORD }}
      run: |
        chmod +x scripts/deploy-app.sh
        ./scripts/deploy-app.sh
```

## ✅ Step 7: Update Application (Optional Enhancement)

### Enhanced `app.py` (if you want to update from Lab 8B)
```python
# Add this route to your existing app.py for deployment info
@app.route('/info')
def info():
    return jsonify({
        "service": "Student Database Service",
        "version": "2.0",
        "deployment": "CI/CD Automated",
        "database": DB_DATABASE,
        "server": DB_SERVER,
        "features": ["Auto Schema", "CI/CD Pipeline", "Health Checks"],
        "timestamp": datetime.now().isoformat()
    })
```

## ✅ Step 8: Required GitHub Secrets

Ensure these secrets are configured in your GitHub repository:
**Settings** → **Secrets and variables** → **Actions**

```
# Database secrets (from Lab 8B)
SQL_SERVER = your-server.database.windows.net
SQL_DATABASE = studentsdb
SQL_USERNAME = sqladmin
SQL_PASSWORD = YourStrongPassword123!

# Azure credentials for deployment
AZURE_CREDENTIALS = {
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "..."
}
```

### Create Azure Service Principal (if needed)
```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "github-actions-lab8c" \
  --role contributor \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth

# Copy the JSON output to AZURE_CREDENTIALS secret
```

## ✅ Step 9: Deploy and Test

### Trigger Pipeline
```bash
# Add files and push to trigger CI/CD
git add .
git commit -m "Add Lab 8C: CI/CD pipeline with database automation"
git push origin main
```

### Monitor Pipeline
1. Go to GitHub Actions tab
2. Watch the pipeline execution:
   - **Database Setup**: Schema and seed data
   - **Test**: Database connection and Flask app
   - **Deploy**: Azure App Service deployment
   - **Health Check**: Verify deployment

### Test Deployed Application
```bash
# Get the app URL from GitHub Actions output
APP_URL="https://lab8c-app-[hash].azurewebsites.net"

# Test endpoints
curl $APP_URL/
curl $APP_URL/health
curl $APP_URL/students
curl $APP_URL/info

# Add a student via API
curl -X POST $APP_URL/student \
  -H "Content-Type: application/json" \
  -d '{"name": "Emma Davis", "email": "emma@university.edu"}'
```

## ✅ Step 10: Verify Database Schema

### Check Schema in Azure Portal
1. Go to Azure Portal → SQL databases
2. Open Query editor
3. Run verification queries:

```sql
-- Check table structure
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'students';

-- Check indexes
SELECT name FROM sys.indexes WHERE object_id = OBJECT_ID('students');

-- Check data
SELECT * FROM students ORDER BY created_at;
```

## ✅ Step 11: Cleanup

### Delete Resources
```bash
# Delete the resource group (keeps database from Lab 8A)
az group delete --name lab8c-rg --yes --no-wait
```

## 🎓 Lab Complete

### What You Built
✅ **Automated Database Schema** - SQL scripts for table creation and seeding  
✅ **CI/CD Pipeline** - Complete GitHub Actions automation  
✅ **Database Integration** - Automated schema management in pipeline  
✅ **App Deployment** - Automated Azure App Service deployment  
✅ **Health Monitoring** - Automated health checks and verification  

### Key Skills Learned
- Database schema automation with SQL scripts
- GitHub Actions CI/CD pipeline creation
- Automated database setup in pipelines
- Azure App Service automated deployment
- Environment-based configuration management
- Continuous integration with database dependencies

### Pipeline Benefits
- **Automated Schema**: No manual database setup required
- **Consistent Deployments**: Same process every time
- **Quality Gates**: Automated testing before deployment
- **Zero-Downtime**: Health checks ensure successful deployment
- **Rollback Ready**: Git-based deployment tracking

Your Flask application now has a complete CI/CD pipeline with automated database management!
