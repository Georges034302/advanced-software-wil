# 🗄️ Lab 8A: Azure SQL Infrastructure Provisioning

## 🎯 Objective
Set up Azure SQL Database infrastructure using ARM templates and CLI scripts. Learn both declarative and imperative approaches to database provisioning.

- Create Azure SQL Server and Database using ARM template
- Alternative: Provision using Azure CLI script
- Configure basic firewall rules
- Test database connection

## 🗂 Structure
```
lab8a/
├── infrastructure/
│   ├── azuredeploy.json (ARM template)
│   ├── azuredeploy.parameters.json
│   └── provision-cli.sh (CLI alternative)
├── sql/
│   └── test-queries.sql
└── README.md
```

## ✅ Step 1: ARM Template Approach (Option A)

### `infrastructure/azuredeploy.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "serverName": {
            "type": "string",
            "defaultValue": "[concat('sqlserver-', uniqueString(resourceGroup().id))]",
            "metadata": {
                "description": "Name for the SQL server"
            }
        },
        "databaseName": {
            "type": "string",
            "defaultValue": "studentsdb",
            "metadata": {
                "description": "Name for the database"
            }
        },
        "adminUsername": {
            "type": "string",
            "defaultValue": "sqladmin",
            "metadata": {
                "description": "Admin username for SQL server"
            }
        },
        "adminPassword": {
            "type": "securestring",
            "metadata": {
                "description": "Admin password for SQL server"
            }
        }
    },
    "variables": {
        "firewallRuleName": "AllowAzureServices"
    },
    "resources": [
        {
            "type": "Microsoft.Sql/servers",
            "apiVersion": "2022-05-01-preview",
            "name": "[parameters('serverName')]",
            "location": "[resourceGroup().location]",
            "properties": {
                "administratorLogin": "[parameters('adminUsername')]",
                "administratorLoginPassword": "[parameters('adminPassword')]",
                "version": "12.0",
                "publicNetworkAccess": "Enabled"
            }
        },
        {
            "type": "Microsoft.Sql/servers/databases",
            "apiVersion": "2022-05-01-preview",
            "name": "[concat(parameters('serverName'), '/', parameters('databaseName'))]",
            "location": "[resourceGroup().location]",
            "dependsOn": [
                "[resourceId('Microsoft.Sql/servers', parameters('serverName'))]"
            ],
            "sku": {
                "name": "Basic",
                "tier": "Basic",
                "capacity": 5
            },
            "properties": {
                "maxSizeBytes": 2147483648
            }
        },
        {
            "type": "Microsoft.Sql/servers/firewallRules",
            "apiVersion": "2022-05-01-preview",
            "name": "[concat(parameters('serverName'), '/', variables('firewallRuleName'))]",
            "dependsOn": [
                "[resourceId('Microsoft.Sql/servers', parameters('serverName'))]"
            ],
            "properties": {
                "startIpAddress": "0.0.0.0",
                "endIpAddress": "0.0.0.0"
            }
        },
        {
            "type": "Microsoft.Sql/servers/firewallRules",
            "apiVersion": "2022-05-01-preview",
            "name": "[concat(parameters('serverName'), '/AllowLocalIP')]",
            "dependsOn": [
                "[resourceId('Microsoft.Sql/servers', parameters('serverName'))]"
            ],
            "properties": {
                "startIpAddress": "0.0.0.0",
                "endIpAddress": "255.255.255.255"
            }
        }
    ],
    "outputs": {
        "serverName": {
            "type": "string",
            "value": "[parameters('serverName')]"
        },
        "databaseName": {
            "type": "string",
            "value": "[parameters('databaseName')]"
        },
        "connectionString": {
            "type": "string",
            "value": "[concat('Server=tcp:', parameters('serverName'), '.database.windows.net,1433;Initial Catalog=', parameters('databaseName'), ';Persist Security Info=False;User ID=', parameters('adminUsername'), ';Password=', parameters('adminPassword'), ';MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;')]"
        }
    }
}
```

### `infrastructure/azuredeploy.parameters.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "serverName": {
            "value": "lab8a-sqlserver"
        },
        "databaseName": {
            "value": "studentsdb"
        },
        "adminUsername": {
            "value": "sqladmin"
        },
        "adminPassword": {
            "value": "YourStrongPassword123!"
        }
    }
}
```

### Deploy ARM Template
```bash
# Create resource group
az group create --name lab8a-rg --location australiaeast

# Deploy ARM template
az deployment group create \
  --resource-group lab8a-rg \
  --template-file infrastructure/azuredeploy.json \
  --parameters infrastructure/azuredeploy.parameters.json

# Get connection string
az deployment group show \
  --resource-group lab8a-rg \
  --name azuredeploy \
  --query properties.outputs.connectionString.value
```

## ✅ Step 2: CLI Script Approach (Option B)

### `infrastructure/provision-cli.sh`
```bash
#!/bin/bash
set -e

# Configuration
RG_NAME="lab8a-rg"
LOCATION="australiaeast"
SERVER_NAME="lab8a-sqlserver-$(openssl rand -hex 4)"
DB_NAME="studentsdb"
ADMIN_USER="sqladmin"
ADMIN_PASS="YourStrongPassword123!"

echo "🗄️ Provisioning Azure SQL Database with CLI..."

# Create resource group
echo "📦 Creating resource group..."
az group create \
  --name $RG_NAME \
  --location $LOCATION

# Create SQL server
echo "🖥️ Creating SQL server..."
az sql server create \
  --resource-group $RG_NAME \
  --name $SERVER_NAME \
  --location $LOCATION \
  --admin-user $ADMIN_USER \
  --admin-password $ADMIN_PASS

# Create database
echo "🗄️ Creating database..."
az sql db create \
  --resource-group $RG_NAME \
  --server $SERVER_NAME \
  --name $DB_NAME \
  --service-objective Basic

# Configure firewall (allow Azure services)
echo "🛡️ Configuring firewall..."
az sql server firewall-rule create \
  --resource-group $RG_NAME \
  --server $SERVER_NAME \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Allow all IPs for development (not for production!)
az sql server firewall-rule create \
  --resource-group $RG_NAME \
  --server $SERVER_NAME \
  --name AllowAll \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255

# Show connection string
echo "✅ Infrastructure provisioned!"
echo "🔗 Server: $SERVER_NAME.database.windows.net"
echo "🗄️ Database: $DB_NAME"
echo "👤 Username: $ADMIN_USER"
echo "🔑 Password: $ADMIN_PASS"

# Connection string for applications
CONNECTION_STRING="Server=tcp:$SERVER_NAME.database.windows.net,1433;Initial Catalog=$DB_NAME;Persist Security Info=False;User ID=$ADMIN_USER;Password=$ADMIN_PASS;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"

echo "📋 Connection String:"
echo "$CONNECTION_STRING"

# Save to .env file
cat > .env << EOF
SQL_SERVER=$SERVER_NAME.database.windows.net
SQL_DATABASE=$DB_NAME
SQL_USERNAME=$ADMIN_USER
SQL_PASSWORD=$ADMIN_PASS
CONNECTION_STRING="$CONNECTION_STRING"
EOF

echo "💾 Connection details saved to .env file"
```

### Run CLI Provisioning
```bash
chmod +x infrastructure/provision-cli.sh
./infrastructure/provision-cli.sh
```

## ✅ Step 3: Test Database Connection

### `sql/test-queries.sql`
```sql
-- Test connection and create a simple table
CREATE TABLE students (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- Insert test data
INSERT INTO students (name, email) VALUES
('Alice Johnson', 'alice@university.edu'),
('Bob Smith', 'bob@university.edu'),
('Carol Davis', 'carol@university.edu');

-- Query test data
SELECT * FROM students;

-- Simple analytics query
SELECT 
    COUNT(*) as total_students,
    GETDATE() as query_time;
```

### Test Using Azure Portal
1. Go to Azure Portal → SQL databases
2. Find your database → Query editor
3. Login with your credentials
4. Copy and paste queries from `test-queries.sql`
5. Run each query to verify connection

### Test Using Azure CLI
```bash
# Test connection using sqlcmd (if installed)
sqlcmd -S $SERVER_NAME.database.windows.net -d $DB_NAME -U $ADMIN_USER -P $ADMIN_PASS -Q "SELECT GETDATE() as connection_test"

# Alternative: Test using Azure CLI
az sql db show \
  --resource-group $RG_NAME \
  --server $SERVER_NAME \
  --name $DB_NAME
```

## ✅ Step 4: Verification

### Check Resources
```bash
# List all resources in the resource group
az resource list \
  --resource-group lab8a-rg \
  --output table

# Get database details
az sql db show \
  --resource-group lab8a-rg \
  --server $SERVER_NAME \
  --name studentsdb \
  --output table

# Check firewall rules
az sql server firewall-rule list \
  --resource-group lab8a-rg \
  --server $SERVER_NAME \
  --output table
```

### Connection String Format
```
Server=tcp:[server-name].database.windows.net,1433;
Initial Catalog=[database-name];
Persist Security Info=False;
User ID=[username];
Password=[password];
MultipleActiveResultSets=False;
Encrypt=True;
TrustServerCertificate=False;
Connection Timeout=30;
```

## ✅ Step 5: Cleanup

### Delete Resources
```bash
# Delete the entire resource group
az group delete --name lab8a-rg --yes --no-wait

# Or delete individual resources
az sql db delete --resource-group lab8a-rg --server $SERVER_NAME --name studentsdb --yes
az sql server delete --resource-group lab8a-rg --name $SERVER_NAME --yes
```

## 🎓 Lab Complete

### What You Built
✅ **Azure SQL Server** - Managed database server  
✅ **Azure SQL Database** - Basic tier database  
✅ **Firewall Rules** - Access control configuration  
✅ **ARM Template** - Infrastructure as Code approach  
✅ **CLI Script** - Imperative provisioning alternative  

### Key Skills Learned
- Azure SQL Database infrastructure provisioning
- ARM template creation and deployment
- Azure CLI database commands
- Firewall configuration for database access
- Connection string generation and usage
- Basic SQL table creation and data insertion

### Infrastructure Created
- **SQL Server**: Managed database server instance
- **Database**: Basic tier with 2GB storage
- **Firewall**: Rules for Azure services and development access
- **Connection String**: Ready for application integration

This basic infrastructure is ready for connecting applications in Lab 8B!
