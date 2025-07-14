# Lab 2D: Simple Development Helpers

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Create basic automation scripts for daily development tasks
- Build simple project setup helpers
- Use bash scripting to solve common problems
- Start development servers easily
- Organize your files automatically

## 📋 Prerequisites
- Completion of Labs 2A, 2B, and 2C
- Basic understanding of bash commands (`ls`, `cp`, `mv`, `mkdir`)
- Knowledge of simple bash loops and conditionals

---

## Part 1: Simple Project Starters

### 1.1 Simple HTML Project Creator

**💡 Copilot Prompt:**
```
Create a very simple bash script that makes a basic HTML project with an index.html file, style.css, and script.js file.
```

```bash
#!/bin/bash
# Simple HTML Project Creator
# File: new_html.sh

echo "Creating a new HTML project..."

# Get project name
read -p "What's your project name? " project_name

# Check if name is empty
if [ -z "$project_name" ]; then
    echo "Please enter a project name!"
    exit 1
fi

# Create project folder
mkdir "$project_name"
cd "$project_name"

# Create basic HTML file
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Welcome to My Website!</h1>
    <p>This is my awesome website.</p>
    <button onclick="sayHello()">Click Me!</button>
    
    <script src="script.js"></script>
</body>
</html>
EOF

# Create basic CSS file
cat > style.css << 'EOF'
body {
    font-family: Arial, sans-serif;
    margin: 40px;
    background-color: #f0f0f0;
}

h1 {
    color: blue;
}

button {
    background-color: green;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: darkgreen;
}
EOF

# Create basic JavaScript file
cat > script.js << 'EOF'
function sayHello() {
    alert("Hello! Welcome to my website!");
}

console.log("Website loaded successfully!");
EOF

echo "✅ HTML project '$project_name' created!"
echo "📁 Open index.html in your browser to see it"
```

### 1.2 Simple Python Project Creator

**💡 Copilot Prompt:**
```
Create a very simple bash script that makes a basic Python project with a main.py file and a simple function.
```

```bash
#!/bin/bash
# Simple Python Project Creator
# File: new_python.sh

echo "Creating a new Python project..."

# Get project name
read -p "What's your project name? " project_name

# Check if name is empty
if [ -z "$project_name" ]; then
    echo "Please enter a project name!"
    exit 1
fi

# Create project folder
mkdir "$project_name"
cd "$project_name"

# Create main Python file
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
My Python Project
"""

def greet(name):
    """Say hello to someone"""
    return f"Hello, {name}!"

def add_numbers(a, b):
    """Add two numbers together"""
    return a + b

def main():
    """Main function"""
    print("Welcome to my Python project!")
    
    # Try the functions
    message = greet("World")
    print(message)
    
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
    
    # Get user input
    name = input("What's your name? ")
    personal_greeting = greet(name)
    print(personal_greeting)

if __name__ == "__main__":
    main()
EOF

# Create a simple test file
cat > test.py << 'EOF'
"""
Simple tests for our functions
"""
from main import greet, add_numbers

def test_greet():
    """Test the greet function"""
    result = greet("Alice")
    expected = "Hello, Alice!"
    if result == expected:
        print("✅ greet test passed")
    else:
        print("❌ greet test failed")

def test_add_numbers():
    """Test the add_numbers function"""
    result = add_numbers(2, 3)
    expected = 5
    if result == expected:
        print("✅ add_numbers test passed")
    else:
        print("❌ add_numbers test failed")

if __name__ == "__main__":
    print("Running tests...")
    test_greet()
    test_add_numbers()
    print("Tests complete!")
EOF

# Create README file
cat > README.md << EOF
# $project_name

A simple Python project.

## How to run:
\`\`\`
python3 main.py
\`\`\`

## How to test:
\`\`\`
python3 test.py
\`\`\`
EOF

echo "✅ Python project '$project_name' created!"
echo "📁 Run with: cd $project_name && python3 main.py"
```

**📝 Exercise 1: Try it out**
1. Create these two scripts
2. Run `./new_html.sh` and make an HTML project
3. Run `./new_python.sh` and make a Python project
4. Test both projects work correctly

---

## Part 2: Simple Development Servers

### 2.1 Quick HTML Server

**💡 Copilot Prompt:**
```
Create a simple bash script that starts a local web server to view HTML files in the browser.
```

```bash
#!/bin/bash
# Quick HTML Server
# File: serve_html.sh

echo "🌐 Starting local web server..."

# Check if we're in a directory with HTML files
if ls *.html &>/dev/null; then
    echo "📁 Found HTML files in current directory"
else
    echo "⚠️ No HTML files found in current directory"
    echo "Make sure you're in a folder with HTML files"
fi

# Use Python's built-in server
PORT=8000

echo "🚀 Starting server on port $PORT"
echo "📱 Open your browser and go to: http://localhost:$PORT"
echo "🛑 Press Ctrl+C to stop the server"
echo

# Start the server
if command -v python3 &>/dev/null; then
    python3 -m http.server $PORT
else
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi
```

### 2.2 Quick Python Runner

**💡 Copilot Prompt:**
```
Create a simple bash script that finds and runs Python files easily.
```

```bash
#!/bin/bash
# Quick Python Runner
# File: run_python.sh

echo "🐍 Python Script Runner"

# Check if a specific file was provided
if [ -n "$1" ]; then
    # Run the specified file
    if [ -f "$1" ]; then
        echo "▶️ Running $1..."
        python3 "$1"
    else
        echo "❌ File '$1' not found"
        exit 1
    fi
else
    # Look for Python files in current directory
    echo "Looking for Python files..."
    
    # Find all .py files
    python_files=($(ls *.py 2>/dev/null))
    
    if [ ${#python_files[@]} -eq 0 ]; then
        echo "❌ No Python files found in current directory"
        exit 1
    elif [ ${#python_files[@]} -eq 1 ]; then
        # Only one file, run it
        echo "▶️ Running ${python_files[0]}..."
        python3 "${python_files[0]}"
    else
        # Multiple files, let user choose
        echo "Found multiple Python files:"
        for i in "${!python_files[@]}"; do
            echo "$((i+1))) ${python_files[$i]}"
        done
        
        read -p "Which file do you want to run? (1-${#python_files[@]}): " choice
        
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#python_files[@]} ]; then
            selected_file="${python_files[$((choice-1))]}"
            echo "▶️ Running $selected_file..."
            python3 "$selected_file"
        else
            echo "❌ Invalid choice"
            exit 1
        fi
    fi
fi
```

**📝 Exercise 2: Test the servers**
1. Create an HTML project using your script from Part 1
2. Use `serve_html.sh` to view it in your browser
3. Create a Python project and use `run_python.sh` to run it

---

## Part 3: Simple File Helpers

### 3.1 Basic File Counter

**💡 Copilot Prompt:**
```
Create a simple script that counts different types of files in a directory.
```

```bash
#!/bin/bash
# Simple File Counter
# File: count_files.sh

echo "📊 Counting files in current directory..."

# Count different file types
html_count=$(ls *.html 2>/dev/null | wc -l)
python_count=$(ls *.py 2>/dev/null | wc -l)
text_count=$(ls *.txt 2>/dev/null | wc -l)
image_count=$(ls *.jpg *.png *.gif 2>/dev/null | wc -l)
total_files=$(ls -1 2>/dev/null | wc -l)

echo
echo "File counts:"
echo "📄 HTML files: $html_count"
echo "🐍 Python files: $python_count"
echo "📝 Text files: $text_count"
echo "🖼️ Image files: $image_count"
echo "📁 Total files: $total_files"
echo

# Show the biggest files
echo "🔍 Largest files:"
ls -lhS | head -6
```

### 3.2 Quick Backup

**💡 Copilot Prompt:**
```
Create a very simple backup script that copies important files to a backup folder with today's date.
```

```bash
#!/bin/bash
# Quick Backup Script
# File: quick_backup.sh

echo "💾 Quick Backup Tool"

# Create backup folder with today's date
backup_folder="backup_$(date +%Y%m%d)"

# Create the backup directory
mkdir -p "$backup_folder"

echo "📁 Created backup folder: $backup_folder"

# Copy important files
file_count=0

# Backup HTML files
for file in *.html; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_folder/"
        echo "✅ Backed up: $file"
        ((file_count++))
    fi
done

# Backup Python files
for file in *.py; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_folder/"
        echo "✅ Backed up: $file"
        ((file_count++))
    fi
done

# Backup text files
for file in *.txt; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_folder/"
        echo "✅ Backed up: $file"
        ((file_count++))
    fi
done

echo
if [ $file_count -eq 0 ]; then
    echo "⚠️ No files found to backup"
    rmdir "$backup_folder"
else
    echo "🎉 Backup complete! Saved $file_count files to $backup_folder"
fi
```

### 3.3 Clean Downloads

**💡 Copilot Prompt:**
```
Create a simple script that organizes the Downloads folder by moving old files to an archive folder.
```

```bash
#!/bin/bash
# Clean Downloads Script
# File: clean_downloads.sh

echo "🧹 Cleaning Downloads folder..."

# Check if Downloads folder exists
downloads_dir="$HOME/Downloads"
if [ ! -d "$downloads_dir" ]; then
    echo "❌ Downloads folder not found: $downloads_dir"
    exit 1
fi

cd "$downloads_dir"

# Create archive folder
archive_dir="old_downloads_$(date +%Y%m%d)"
mkdir -p "$archive_dir"

echo "📁 Created archive folder: $archive_dir"

# Move files older than 7 days
moved_count=0

# Find files older than 7 days and move them
while read -r file; do
    if [ -f "$file" ]; then
        mv "$file" "$archive_dir/"
        echo "📦 Moved: $file"
        ((moved_count++))
    fi
done < <(find . -maxdepth 1 -type f -mtime +7)

echo
if [ $moved_count -eq 0 ]; then
    echo "✨ Downloads folder is already clean!"
    rmdir "$archive_dir"
else
    echo "🎉 Moved $moved_count old files to $archive_dir"
    echo "💡 You can delete $archive_dir if you don't need those files"
fi
```

**📝 Exercise 3: Try the file helpers**
1. Use `count_files.sh` to see what files you have
2. Use `quick_backup.sh` to backup your work
3. Try `clean_downloads.sh` on your Downloads folder (be careful!)

---

## Part 4: Conclusion

### 4.1 Review

You've learned to create simple automation scripts that help with daily development tasks:

1. **Project Setup Helpers** - Quick ways to start new HTML and Python projects
2. **Development Servers** - Easy ways to test your code locally
3. **File Helpers** - Simple tools to organize and backup your work

These scripts are building blocks - you can modify them as you learn more bash commands!

### 4.2 Next Steps

**Ways to improve these scripts:**
- Add more file types to the project creators
- Make the file counter show more details
- Add error checking to the backup script
- Make the clean script ask before moving files

**🤖 Copilot Tips for Script Writing:**
- Start prompts with "Create a simple bash script that..."
- Ask for explanations: "Explain what each line does"
- Request improvements: "Make this script safer" or "Add user-friendly messages"

### 4.3 Key Takeaways

✅ **Small scripts are powerful** - Even 10-20 lines can save lots of time  
✅ **Automate repetitive tasks** - If you do it twice, consider scripting it  
✅ **Start simple** - You can always make scripts more complex later  
✅ **Use echo for feedback** - Let users know what's happening  

Remember: The best automation script is one you actually use! Start with simple versions and improve them as you get more comfortable with bash.

---

*Lab 2D: Simple Development Helpers - Complete* 🎉
EOF
            ;;
        "python")
            cat >> "$workflow_file" << EOF
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: \${{ env.PYTHON_VERSION }}
        
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run Tests
      run: pytest
      
    - name: Build
      run: python setup.py build
EOF
            ;;
    esac
    
    cat >> "$workflow_file" << EOF

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Production
      run: |
        echo "Deploying to production"
        # Add deployment commands here
        ./scripts/deploy.sh -e prod -s \${{ github.event.repository.name }} -v \${{ github.sha }}
EOF

    echo "Generated GitHub Actions workflow: $workflow_file"
}

# Setup environment-specific scripts
setup_env_scripts() {
    mkdir -p scripts/environments
    
    # Development environment
    cat > scripts/environments/setup-dev.sh << 'EOF'
#!/bin/bash
echo "Setting up development environment..."
export NODE_ENV=development
export DEBUG=true
export LOG_LEVEL=debug
EOF

    # Staging environment
    cat > scripts/environments/setup-staging.sh << 'EOF'
#!/bin/bash
echo "Setting up staging environment..."
export NODE_ENV=staging
export DEBUG=false
export LOG_LEVEL=info
EOF

    # Production environment
    cat > scripts/environments/setup-prod.sh << 'EOF'
#!/bin/bash
echo "Setting up production environment..."
export NODE_ENV=production
export DEBUG=false
export LOG_LEVEL=error
EOF

    chmod +x scripts/environments/*.sh
    echo "Environment setup scripts created in scripts/environments/"
}

# Generate Docker configuration
generate_docker_config() {
    local project_type=$1
    
    # Dockerfile
    case $project_type in
        "nodejs")
            cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

USER node

CMD ["npm", "start"]
EOF
            ;;
        "python")
            cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

USER nobody

CMD ["python", "app.py"]
EOF
            ;;
    esac
    
    # Docker Compose
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    restart: unless-stopped
    
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
EOF

    # .dockerignore
    cat > .dockerignore << 'EOF'
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.nyc_output
EOF

    echo "Docker configuration files generated"
}

# Setup monitoring and logging
setup_monitoring() {
    mkdir -p scripts/monitoring
    
    # Health check script
    cat > scripts/monitoring/health-check.sh << 'EOF'
#!/bin/bash
# Health check script for monitoring

SERVICE_URL=${SERVICE_URL:-"http://localhost:3000"}
HEALTH_ENDPOINT="${SERVICE_URL}/health"
MAX_ATTEMPTS=3
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "Health check attempt $ATTEMPT..."
    
    if curl -f -s "$HEALTH_ENDPOINT" > /dev/null; then
        echo "✅ Service is healthy"
        exit 0
    fi
    
    echo "❌ Health check failed"
    ((ATTEMPT++))
    sleep 5
done

echo "🚨 Service is unhealthy after $MAX_ATTEMPTS attempts"
exit 1
EOF

    # Log rotation script
    cat > scripts/monitoring/rotate-logs.sh << 'EOF'
#!/bin/bash
# Log rotation script

LOG_DIR=${LOG_DIR:-"/var/log/myapp"}
MAX_SIZE=${MAX_SIZE:-"100M"}
MAX_FILES=${MAX_FILES:-10}

find "$LOG_DIR" -name "*.log" -size +$MAX_SIZE -exec gzip {} \;
find "$LOG_DIR" -name "*.log.gz" -mtime +30 -delete

echo "Log rotation completed"
EOF

    chmod +x scripts/monitoring/*.sh
    echo "Monitoring scripts created in scripts/monitoring/"
}

# Main function
main() {
    local project_type=${1:-"nodejs"}
    
    echo "🚀 Setting up CI/CD automation for $project_type project..."
    
    generate_github_workflow "$project_type"
    setup_env_scripts
    generate_docker_config "$project_type"
    setup_monitoring
    
    # Create main automation script
    cat > scripts/automate.sh << 'EOF'
#!/bin/bash
# Main automation script

case $1 in
    "setup")
        echo "🔧 Setting up development environment..."
        ./scripts/environments/setup-dev.sh
        ;;
    "test")
        echo "🧪 Running tests..."
        npm test || python -m pytest
        ;;
    "build")
        echo "🏗️ Building application..."
        ./build.sh
        ;;
    "deploy")
        echo "🚀 Deploying application..."
        ./deploy.sh -e "${2:-dev}" -s "$(basename $(pwd))" -v "${3:-latest}"
        ;;
    "monitor")
        echo "📊 Running health checks..."
        ./scripts/monitoring/health-check.sh
        ;;
    *)
        echo "Usage: $0 {setup|test|build|deploy|monitor}"
        exit 1
        ;;
esac
EOF

    chmod +x scripts/automate.sh
    
    echo "✅ CI/CD automation setup complete!"
    echo "📁 Files created:"
    echo "   - .github/workflows/ci-cd.yml"
    echo "   - scripts/environments/"
    echo "   - scripts/monitoring/"
    echo "   - Dockerfile & docker-compose.yml"
    echo "   - scripts/automate.sh"
}

# Usage
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**📝 Exercise 2: CI/CD Enhancement**
Extend the CI/CD helper script to support:
- Multiple cloud providers
- Database migrations
- Security scanning
- Performance testing

---

## Part 5: Advanced Automation Patterns

### 5.1 Infrastructure as Code Scripts

**💡 Copilot Prompt:**
```
Create a script that generates Terraform configurations for different cloud providers and manages infrastructure deployment with proper state management and rollback capabilities.
```

```bash
#!/bin/bash
# Infrastructure as Code Manager
# File: iac-manager.sh

set -euo pipefail

# Configuration
TERRAFORM_VERSION="1.5.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IAC_DIR="$SCRIPT_DIR/infrastructure"
STATE_BACKEND="local"  # local, s3, azurerm, gcs

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Install Terraform if not present
install_terraform() {
    if command -v terraform &> /dev/null; then
        log "Terraform already installed: $(terraform version -json | jq -r .terraform_version)"
        return 0
    fi
    
    log "Installing Terraform $TERRAFORM_VERSION..."
    
    case "$(uname -s)" in
        "Linux")
            curl -LO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
            unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
            sudo mv terraform /usr/local/bin/
            rm "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
            ;;
        "Darwin")
            curl -LO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_darwin_amd64.zip"
            unzip "terraform_${TERRAFORM_VERSION}_darwin_amd64.zip"
            sudo mv terraform /usr/local/bin/
            rm "terraform_${TERRAFORM_VERSION}_darwin_amd64.zip"
            ;;
    esac
    
    log "Terraform installed successfully"
}

# Generate Terraform configuration for AWS
generate_aws_config() {
    local environment=$1
    local app_name=$2
    
    mkdir -p "$IAC_DIR/aws/$environment"
    
    # Main configuration
    cat > "$IAC_DIR/aws/$environment/main.tf" << EOF
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = "$environment"
      Application = "$app_name"
      ManagedBy   = "terraform"
    }
  }
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "\${var.app_name}-vpc-$environment"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "\${var.app_name}-igw-$environment"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "\${var.app_name}-public-subnet-\${count.index + 1}-$environment"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "\${var.app_name}-public-rt-$environment"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "app" {
  name_prefix = "\${var.app_name}-$environment-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "\${var.app_name}-sg-$environment"
  }
}

---

## ✅ Validation Steps

1. **Script functionality**: All scripts run without errors and produce expected outputs
2. **File organization**: Directory organization works correctly with different file types
3. **Log analysis**: Log analyzer extracts meaningful information from sample log files
4. **Batch processing**: File processing scripts handle multiple files efficiently
5. **Project templates**: Generated projects have correct structure and work as expected
6. **Development workflow**: Server launcher and git helper improve development efficiency

---

## 🎯 Final Exercises

### Exercise 1: Custom Project Template
Extend the project setup script to include:
- React.js project template
- Basic documentation template with multiple markdown files
- Simple Express.js API template

### Exercise 2: Enhanced File Processor
Create additional batch operations:
- Find and remove duplicate files (by content hash)
- Batch rename files with sequence numbers
- Extract metadata from images and create summary reports

### Exercise 3: Development Workflow Enhancement
Add features to the git helper script:
- Automatic code formatting before commits
- Integration with GitHub/GitLab for creating pull requests
- Branch cleanup utilities (delete merged branches)

---

## 🔗 Additional Resources

**Useful Commands Reference:**
```bash
# File operations
find . -name "*.txt" -exec cp {} backup/ \;
grep -r "pattern" --include="*.log" .
sed -i 's/old/new/g' *.txt

# Development servers
python3 -m http.server 8000
npx live-server --port=3000
php -S localhost:8080

# Git workflow
git checkout -b feature/new-feature
git add . && git commit -m "feat: add new feature"
git push -u origin feature/new-feature
```

**🤖 Advanced Copilot Prompts:**
```
Create a script that monitors a directory for new files and automatically processes them based on file type
Generate a simple CI/CD script that runs tests and deploys to a staging server
Build a log rotation script that compresses old logs and maintains disk space
Create a backup script that syncs important files to cloud storage
```

**🔄 Next Steps:**
- Practice creating your own automation scripts for daily tasks
- Explore more advanced bash features like arrays and functions
- Learn about cron jobs for scheduling automated tasks
- Study CI/CD concepts for the next module

---

**📚 Key Takeaways:**
- Simple automation scripts can significantly improve development workflow
- File organization and batch processing save time on repetitive tasks
- Log analysis helps with debugging and monitoring
- Project templates ensure consistent development environments
- Git workflow helpers reduce common development friction
- Start small and gradually build more complex automation solutions
