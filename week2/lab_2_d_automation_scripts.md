# Lab 2D: Development Workflow Automation

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Create simple automation scripts for common development tasks
- Build file processing and batch operation scripts
- Automate project setup and organization
- Use GitHub Copilot to generate helpful workflow scripts
- Apply bash scripting to solve real development problems

## 📋 Prerequisites
- Completion of Labs 2A, 2B, and 2C
- Understanding of bash scripting fundamentals
- Basic file operations knowledge
- GitHub Copilot enabled

---

## Part 1: Project Setup Automation

### 1.1 Simple Project Template Generator

**💡 Copilot Prompt:**
```
Create a simple bash script that generates basic project structures for web development projects (HTML/CSS/JS) with common files and folders.
```

```bash
#!/bin/bash
# Project Setup Script
# File: setup_project.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Create basic web project structure
create_web_project() {
    local project_name=$1
    
    print_message $BLUE "Creating web project: $project_name"
    
    # Create main directories
    mkdir -p "$project_name"/{css,js,images,docs}
    
    # Create basic HTML file
    cat > "$project_name/index.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$project_name</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Welcome to $project_name</h1>
    </header>
    
    <main>
        <p>This is your new project!</p>
    </main>
    
    <footer>
        <p>&copy; 2025 $project_name</p>
    </footer>
    
    <script src="js/script.js"></script>
</body>
</html>
EOF

    # Create basic CSS file
    cat > "$project_name/css/style.css" << EOF
/* Basic styles for $project_name */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background-color: #007bff;
    color: white;
    text-align: center;
    padding: 1rem;
}

main {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

footer {
    background-color: #f8f9fa;
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
}
EOF

    # Create basic JavaScript file
    cat > "$project_name/js/script.js" << EOF
// JavaScript for $project_name
console.log('Welcome to $project_name!');

// Add your JavaScript code here
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded successfully');
});
EOF

    # Create README file
    cat > "$project_name/README.md" << EOF
# $project_name

A simple web project created with the project setup script.

## Project Structure
- \`index.html\` - Main HTML file
- \`css/\` - Stylesheets
- \`js/\` - JavaScript files
- \`images/\` - Image assets
- \`docs/\` - Documentation

## Getting Started
1. Open \`index.html\` in your web browser
2. Edit the files to customize your project
3. Add your own images to the \`images/\` folder

## Development
- HTML: Edit \`index.html\`
- CSS: Edit \`css/style.css\`
- JavaScript: Edit \`js/script.js\`
EOF

    print_message $GREEN "✅ Web project '$project_name' created successfully!"
}

# Create Python project structure
create_python_project() {
    local project_name=$1
    
    print_message $BLUE "Creating Python project: $project_name"
    
    # Create directories
    mkdir -p "$project_name"/{src,tests,docs}
    
    # Create main Python file
    cat > "$project_name/src/main.py" << EOF
#!/usr/bin/env python3
"""
Main module for $project_name
"""

def main():
    """Main function"""
    print("Hello from $project_name!")
    
    # Add your code here
    pass

if __name__ == "__main__":
    main()
EOF

    # Create a simple module
    cat > "$project_name/src/utils.py" << EOF
"""
Utility functions for $project_name
"""

def greet(name):
    """Greet a person by name"""
    return f"Hello, {name}!"

def calculate_sum(numbers):
    """Calculate sum of a list of numbers"""
    return sum(numbers)
EOF

    # Create test file
    cat > "$project_name/tests/test_utils.py" << EOF
"""
Tests for utils module
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import greet, calculate_sum

def test_greet():
    """Test greet function"""
    result = greet("World")
    assert result == "Hello, World!"
    print("✅ greet test passed")

def test_calculate_sum():
    """Test calculate_sum function"""
    result = calculate_sum([1, 2, 3, 4, 5])
    assert result == 15
    print("✅ calculate_sum test passed")

if __name__ == "__main__":
    test_greet()
    test_calculate_sum()
    print("All tests passed!")
EOF

    # Create requirements file
    cat > "$project_name/requirements.txt" << EOF
# Add your Python dependencies here
# Example:
# requests>=2.25.0
# numpy>=1.20.0
EOF

    # Create README
    cat > "$project_name/README.md" << EOF
# $project_name

A Python project created with the project setup script.

## Project Structure
- \`src/\` - Source code
- \`tests/\` - Test files
- \`docs/\` - Documentation
- \`requirements.txt\` - Python dependencies

## Getting Started
1. Navigate to the project directory: \`cd $project_name\`
2. Install dependencies: \`pip install -r requirements.txt\`
3. Run the main script: \`python src/main.py\`
4. Run tests: \`python tests/test_utils.py\`

## Development
- Add new modules in the \`src/\` directory
- Add tests in the \`tests/\` directory
- Update \`requirements.txt\` when adding new dependencies
EOF

    print_message $GREEN "✅ Python project '$project_name' created successfully!"
}

# Main function
main() {
    print_message $YELLOW "🚀 Project Setup Script"
    echo
    
    # Get project name
    if [ -z "$1" ]; then
        read -p "Enter project name: " project_name
    else
        project_name=$1
    fi
    
    # Validate project name
    if [ -z "$project_name" ]; then
        print_message $YELLOW "❌ Project name cannot be empty"
        exit 1
    fi
    
    # Check if directory already exists
    if [ -d "$project_name" ]; then
        print_message $YELLOW "⚠️ Directory '$project_name' already exists"
        read -p "Continue anyway? (y/N): " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
    
    # Get project type
    echo "Select project type:"
    echo "1) Web (HTML/CSS/JS)"
    echo "2) Python"
    read -p "Enter choice (1-2): " choice
    
    case $choice in
        1)
            create_web_project "$project_name"
            ;;
        2)
            create_python_project "$project_name"
            ;;
        *)
            print_message $YELLOW "❌ Invalid choice"
            exit 1
            ;;
    esac
    
    echo
    print_message $GREEN "🎉 Project setup complete!"
    print_message $BLUE "📁 Navigate to your project: cd $project_name"
}

# Show usage if help requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [project_name]"
    echo "Creates a new project with basic structure and files"
    echo
    echo "Examples:"
    echo "  $0                    # Interactive mode"
    echo "  $0 my-website        # Create project with name"
    exit 0
fi

# Run main function
main "$@"
```

**📝 Exercise 1: Customize the project generator**
Modify the script to add more project types (e.g., basic Node.js project, simple documentation site).

**🤖 Copilot Exercise 1:**
```
Add a "documentation" project type to the setup script that creates a basic documentation structure with multiple markdown files and an index page.
```

---

## Part 2: File Organization and Cleanup Scripts

### 2.1 File Organizer Script

**💡 Copilot Prompt:**
```
Create a simple bash script that organizes files in a directory by their file extensions, moving them into appropriate subdirectories.
```

```bash
#!/bin/bash
# File Organizer Script
# File: organize_files.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to print colored messages
print_msg() {
    echo -e "${1}${2}${NC}"
}

# Function to organize files by extension
organize_files() {
    local target_dir=${1:-.}  # Default to current directory
    local moved_count=0
    
    print_msg $BLUE "🗂️ Organizing files in: $target_dir"
    
    # Change to target directory
    cd "$target_dir" || {
        print_msg $RED "❌ Cannot access directory: $target_dir"
        exit 1
    }
    
    # Create organization directories
    mkdir -p {documents,images,videos,audio,archives,scripts,data,misc}
    
    # Organize different file types
    for file in *; do
        # Skip if it's a directory or already organized
        if [[ -d "$file" ]] || [[ "$file" == "organize_files.sh" ]]; then
            continue
        fi
        
        # Get file extension
        extension="${file##*.}"
        extension_lower=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
        
        case $extension_lower in
            # Documents
            txt|doc|docx|pdf|rtf|odt)
                mv "$file" documents/
                print_msg $GREEN "📄 Moved $file to documents/"
                ;;
            # Images
            jpg|jpeg|png|gif|bmp|svg|webp)
                mv "$file" images/
                print_msg $GREEN "🖼️ Moved $file to images/"
                ;;
            # Videos
            mp4|avi|mkv|mov|wmv|flv|webm)
                mv "$file" videos/
                print_msg $GREEN "🎬 Moved $file to videos/"
                ;;
            # Audio
            mp3|wav|flac|aac|ogg|wma)
                mv "$file" audio/
                print_msg $GREEN "🎵 Moved $file to audio/"
                ;;
            # Archives
            zip|rar|7z|tar|gz|bz2)
                mv "$file" archives/
                print_msg $GREEN "📦 Moved $file to archives/"
                ;;
            # Scripts
            sh|bash|py|js|php|pl|rb)
                mv "$file" scripts/
                print_msg $GREEN "📜 Moved $file to scripts/"
                ;;
            # Data files
            csv|json|xml|yaml|yml|sql)
                mv "$file" data/
                print_msg $GREEN "📊 Moved $file to data/"
                ;;
            # Everything else
            *)
                mv "$file" misc/
                print_msg $YELLOW "❓ Moved $file to misc/"
                ;;
        esac
        
        ((moved_count++))
    done
    
    # Remove empty directories
    for dir in documents images videos audio archives scripts data misc; do
        if [[ -d "$dir" ]] && [[ -z "$(ls -A "$dir")" ]]; then
            rmdir "$dir"
            print_msg $YELLOW "🗑️ Removed empty directory: $dir"
        fi
    done
    
    print_msg $GREEN "✅ Organization complete! Moved $moved_count files."
}

# Function to show current organization
show_organization() {
    local target_dir=${1:-.}
    
    print_msg $BLUE "📋 Current organization in: $target_dir"
    
    for dir in documents images videos audio archives scripts data misc; do
        if [[ -d "$target_dir/$dir" ]]; then
            local count=$(find "$target_dir/$dir" -type f | wc -l)
            if [[ $count -gt 0 ]]; then
                print_msg $GREEN "  $dir: $count files"
            fi
        fi
    done
}

# Main function
main() {
    case "${1:-organize}" in
        organize)
            organize_files "${2:-.}"
            ;;
        show|status)
            show_organization "${2:-.}"
            ;;
        help|-h|--help)
            echo "File Organizer Script"
            echo
            echo "Usage:"
            echo "  $0 [organize] [directory]    # Organize files (default)"
            echo "  $0 show [directory]          # Show current organization"
            echo "  $0 help                      # Show this help"
            echo
            echo "Examples:"
            echo "  $0                           # Organize current directory"
            echo "  $0 organize ~/Downloads      # Organize Downloads folder"
            echo "  $0 show ~/Downloads          # Show Downloads organization"
            ;;
        *)
            print_msg $RED "❌ Unknown command: $1"
            print_msg $YELLOW "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run the script
main "$@"
```

### 2.2 Project Backup Script

**💡 Copilot Prompt:**
```
Create a simple backup script that creates compressed backups of project directories with timestamps, excluding common build artifacts and temporary files.
```

```bash
#!/bin/bash
# Project Backup Script
# File: backup_project.sh

# Configuration
BACKUP_DIR="$HOME/project_backups"
DATE_FORMAT=$(date '+%Y%m%d_%H%M%S')

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_msg() {
    echo -e "${1}${2}${NC}"
}

# Function to create backup
create_backup() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    local backup_name="${project_name}_${DATE_FORMAT}.tar.gz"
    local backup_path="$BACKUP_DIR/$backup_name"
    
    # Validate project path
    if [[ ! -d "$project_path" ]]; then
        print_msg $RED "❌ Directory not found: $project_path"
        exit 1
    fi
    
    print_msg $BLUE "📦 Creating backup of: $project_name"
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
    
    # Files and directories to exclude from backup
    local exclude_patterns=(
        --exclude='node_modules'
        --exclude='__pycache__'
        --exclude='*.pyc'
        --exclude='.git'
        --exclude='build'
        --exclude='dist'
        --exclude='target'
        --exclude='*.log'
        --exclude='.DS_Store'
        --exclude='Thumbs.db'
        --exclude='*.tmp'
        --exclude='*.temp'
    )
    
    # Create compressed backup
    if tar czf "$backup_path" "${exclude_patterns[@]}" -C "$(dirname "$project_path")" "$project_name"; then
        local backup_size=$(du -h "$backup_path" | cut -f1)
        print_msg $GREEN "✅ Backup created: $backup_name ($backup_size)"
        print_msg $BLUE "📁 Location: $backup_path"
    else
        print_msg $RED "❌ Backup failed!"
        exit 1
    fi
}

# Function to list backups
list_backups() {
    print_msg $BLUE "📋 Available backups in: $BACKUP_DIR"
    
    if [[ ! -d "$BACKUP_DIR" ]]; then
        print_msg $YELLOW "⚠️ No backup directory found"
        return
    fi
    
    local backup_count=0
    for backup in "$BACKUP_DIR"/*.tar.gz; do
        if [[ -f "$backup" ]]; then
            local size=$(du -h "$backup" | cut -f1)
            local date=$(stat -c %y "$backup" | cut -d' ' -f1)
            print_msg $GREEN "  $(basename "$backup") - $size - $date"
            ((backup_count++))
        fi
    done
    
    if [[ $backup_count -eq 0 ]]; then
        print_msg $YELLOW "⚠️ No backups found"
    else
        print_msg $BLUE "Total backups: $backup_count"
    fi
}

# Function to clean old backups
clean_old_backups() {
    local days=${1:-30}  # Default: keep backups for 30 days
    
    print_msg $BLUE "🧹 Cleaning backups older than $days days"
    
    if [[ ! -d "$BACKUP_DIR" ]]; then
        print_msg $YELLOW "⚠️ No backup directory found"
        return
    fi
    
    local deleted_count=0
    while read -r backup; do
        if [[ -f "$backup" ]]; then
            rm "$backup"
            print_msg $YELLOW "🗑️ Deleted: $(basename "$backup")"
            ((deleted_count++))
        fi
    done < <(find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$days)
    
    if [[ $deleted_count -eq 0 ]]; then
        print_msg $GREEN "✅ No old backups to clean"
    else
        print_msg $GREEN "✅ Cleaned $deleted_count old backups"
    fi
}

# Main function
main() {
    case "${1:-backup}" in
        backup)
            if [[ -z "$2" ]]; then
                create_backup "."
            else
                create_backup "$2"
            fi
            ;;
        list)
            list_backups
            ;;
        clean)
            clean_old_backups "${2:-30}"
            ;;
        help|-h|--help)
            echo "Project Backup Script"
            echo
            echo "Usage:"
            echo "  $0 [backup] [project_path]   # Create backup (default: current dir)"
            echo "  $0 list                      # List all backups"
            echo "  $0 clean [days]              # Clean backups older than X days (default: 30)"
            echo "  $0 help                      # Show this help"
            echo
            echo "Examples:"
            echo "  $0                           # Backup current directory"
            echo "  $0 backup ~/my-project       # Backup specific project"
            echo "  $0 list                      # Show all backups"
            echo "  $0 clean 7                   # Delete backups older than 7 days"
            ;;
        *)
            print_msg $RED "❌ Unknown command: $1"
            print_msg $YELLOW "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"
```

**📝 Exercise 2: Enhanced file operations**
Create a script that:
1. Finds duplicate files in a directory
2. Renames files in batch (e.g., adding prefixes/suffixes)
3. Converts image files to different formats

**🤖 Copilot Exercise 2:**
```
Create a script that finds and reports duplicate files in a directory using file checksums, with options to delete duplicates or move them to a separate folder.
```

---

## Part 3: Deployment Automation

### 3.1 Multi-Environment Deployment Script

```bash
#!/bin/bash
# Multi-Environment Deployment Script
# File: deploy.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/config"
BACKUP_DIR="$SCRIPT_DIR/backups"
LOG_FILE="$SCRIPT_DIR/deploy.log"

# Default values
ENVIRONMENT=""
SERVICE_NAME=""
VERSION=""
DRY_RUN=false
ROLLBACK=false
FORCE=false

# Environment configurations
declare -A ENV_CONFIGS
ENV_CONFIGS[dev]="dev.env"
ENV_CONFIGS[staging]="staging.env"
ENV_CONFIGS[prod]="prod.env"

# Deployment strategies
declare -A DEPLOY_STRATEGIES
DEPLOY_STRATEGIES[blue-green]="blue_green_deploy"
DEPLOY_STRATEGIES[rolling]="rolling_deploy"
DEPLOY_STRATEGIES[recreate]="recreate_deploy"

# Logging with levels
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Load environment configuration
load_env_config() {
    local env=$1
    local config_file="$CONFIG_DIR/${ENV_CONFIGS[$env]}"
    
    if [ ! -f "$config_file" ]; then
        log "ERROR" "Configuration file not found: $config_file"
        return 1
    fi
    
    log "INFO" "Loading configuration for environment: $env"
    source "$config_file"
    
    # Validate required variables
    local required_vars=("DEPLOY_TARGET" "DEPLOY_USER" "SERVICE_PORT")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            log "ERROR" "Required variable $var not set in $config_file"
            return 1
        fi
    done
}

# Pre-deployment checks
pre_deploy_checks() {
    log "INFO" "Running pre-deployment checks..."
    
    # Check if service is running
    if [ "$ROLLBACK" = false ]; then
        check_service_health
    fi
    
    # Check deployment target accessibility
    if ! ping -c 1 "$DEPLOY_TARGET" &>/dev/null; then
        log "ERROR" "Cannot reach deployment target: $DEPLOY_TARGET"
        return 1
    fi
    
    # Check SSH connectivity
    if ! ssh -o ConnectTimeout=10 "$DEPLOY_USER@$DEPLOY_TARGET" "echo 'SSH OK'" &>/dev/null; then
        log "ERROR" "SSH connection failed to $DEPLOY_USER@$DEPLOY_TARGET"
        return 1
    fi
    
    # Check disk space on target
    local available_space=$(ssh "$DEPLOY_USER@$DEPLOY_TARGET" "df / | awk 'NR==2 {print \$4}'")
    if [ "$available_space" -lt 1000000 ]; then  # Less than 1GB
        log "WARN" "Low disk space on target: ${available_space}KB available"
        if [ "$FORCE" = false ]; then
            log "ERROR" "Insufficient disk space. Use --force to override."
            return 1
        fi
    fi
    
    log "INFO" "Pre-deployment checks passed"
}

# Check service health
check_service_health() {
    log "INFO" "Checking service health..."
    
    local health_url="http://$DEPLOY_TARGET:$SERVICE_PORT/health"
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$health_url" &>/dev/null; then
            log "INFO" "Service health check passed"
            return 0
        fi
        
        log "WARN" "Health check attempt $attempt failed"
        ((attempt++))
        sleep 5
    done
    
    log "ERROR" "Service health check failed after $max_attempts attempts"
    return 1
}

# Create backup
create_backup() {
    if [ "$DRY_RUN" = true ]; then
        log "INFO" "[DRY RUN] Would create backup"
        return 0
    fi
    
    log "INFO" "Creating backup..."
    
    local backup_name="${SERVICE_NAME}_${ENVIRONMENT}_$(date +%Y%m%d_%H%M%S)"
    local backup_path="$BACKUP_DIR/$backup_name"
    
    mkdir -p "$backup_path"
    
    # Backup application files
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "tar -czf /tmp/$backup_name.tar.gz -C /opt/$SERVICE_NAME ."
    scp "$DEPLOY_USER@$DEPLOY_TARGET:/tmp/$backup_name.tar.gz" "$backup_path/"
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "rm /tmp/$backup_name.tar.gz"
    
    # Backup database (if applicable)
    if [ -n "${DB_NAME:-}" ]; then
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "pg_dump $DB_NAME | gzip > /tmp/${backup_name}_db.sql.gz"
        scp "$DEPLOY_USER@$DEPLOY_TARGET:/tmp/${backup_name}_db.sql.gz" "$backup_path/"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "rm /tmp/${backup_name}_db.sql.gz"
    fi
    
    echo "$backup_name" > "$BACKUP_DIR/latest_backup"
    log "INFO" "Backup created: $backup_name"
}

# Blue-Green deployment
blue_green_deploy() {
    log "INFO" "Starting blue-green deployment..."
    
    local current_slot=$(ssh "$DEPLOY_USER@$DEPLOY_TARGET" "readlink /opt/$SERVICE_NAME/current" | grep -o '[bg]$')
    local new_slot="g"
    if [ "$current_slot" = "g" ]; then
        new_slot="b"
    fi
    
    log "INFO" "Deploying to slot: $new_slot"
    
    # Deploy to inactive slot
    deploy_to_slot "$new_slot"
    
    # Health check new deployment
    if check_service_health_slot "$new_slot"; then
        # Switch traffic
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "ln -sfn /opt/$SERVICE_NAME/$new_slot /opt/$SERVICE_NAME/current"
        log "INFO" "Traffic switched to new deployment"
    else
        log "ERROR" "Health check failed for new deployment"
        return 1
    fi
}

# Rolling deployment
rolling_deploy() {
    log "INFO" "Starting rolling deployment..."
    
    local instances=($(ssh "$DEPLOY_USER@$DEPLOY_TARGET" "docker ps --format '{{.Names}}' | grep $SERVICE_NAME"))
    
    for instance in "${instances[@]}"; do
        log "INFO" "Updating instance: $instance"
        
        # Update one instance
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "docker stop $instance"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "docker rm $instance"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "docker run -d --name $instance $SERVICE_NAME:$VERSION"
        
        # Wait for health check
        sleep 30
        if ! check_service_health; then
            log "ERROR" "Rolling deployment failed at instance: $instance"
            return 1
        fi
    done
    
    log "INFO" "Rolling deployment completed"
}

# Recreate deployment (simple stop/start)
recreate_deploy() {
    log "INFO" "Starting recreate deployment..."
    
    if [ "$DRY_RUN" = true ]; then
        log "INFO" "[DRY RUN] Would stop service, deploy new version, and start service"
        return 0
    fi
    
    # Stop service
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "systemctl stop $SERVICE_NAME || docker stop $SERVICE_NAME || true"
    
    # Deploy new version
    deploy_application
    
    # Start service
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "systemctl start $SERVICE_NAME || docker start $SERVICE_NAME"
    
    # Health check
    sleep 10
    check_service_health
}

# Deploy application files
deploy_application() {
    log "INFO" "Deploying application files..."
    
    if [ "$DRY_RUN" = true ]; then
        log "INFO" "[DRY RUN] Would deploy application files"
        return 0
    fi
    
    # Create deployment directory
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "mkdir -p /opt/$SERVICE_NAME/releases/$VERSION"
    
    # Upload application package
    if [ -f "dist/$SERVICE_NAME-$VERSION.tar.gz" ]; then
        scp "dist/$SERVICE_NAME-$VERSION.tar.gz" "$DEPLOY_USER@$DEPLOY_TARGET:/tmp/"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "tar -xzf /tmp/$SERVICE_NAME-$VERSION.tar.gz -C /opt/$SERVICE_NAME/releases/$VERSION"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "rm /tmp/$SERVICE_NAME-$VERSION.tar.gz"
    else
        log "ERROR" "Application package not found: dist/$SERVICE_NAME-$VERSION.tar.gz"
        return 1
    fi
    
    # Update configuration
    scp "$CONFIG_DIR/${ENV_CONFIGS[$ENVIRONMENT]}" "$DEPLOY_USER@$DEPLOY_TARGET:/opt/$SERVICE_NAME/releases/$VERSION/.env"
    
    # Set permissions
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "chown -R $DEPLOY_USER:$DEPLOY_USER /opt/$SERVICE_NAME/releases/$VERSION"
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "chmod +x /opt/$SERVICE_NAME/releases/$VERSION/bin/*"
    
    log "INFO" "Application deployment completed"
}

# Rollback deployment
rollback_deployment() {
    log "INFO" "Starting rollback process..."
    
    if [ ! -f "$BACKUP_DIR/latest_backup" ]; then
        log "ERROR" "No backup found for rollback"
        return 1
    fi
    
    local backup_name=$(cat "$BACKUP_DIR/latest_backup")
    local backup_path="$BACKUP_DIR/$backup_name"
    
    if [ ! -d "$backup_path" ]; then
        log "ERROR" "Backup directory not found: $backup_path"
        return 1
    fi
    
    if [ "$DRY_RUN" = true ]; then
        log "INFO" "[DRY RUN] Would rollback to backup: $backup_name"
        return 0
    fi
    
    # Stop current service
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "systemctl stop $SERVICE_NAME || docker stop $SERVICE_NAME || true"
    
    # Restore from backup
    scp "$backup_path/$backup_name.tar.gz" "$DEPLOY_USER@$DEPLOY_TARGET:/tmp/"
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "rm -rf /opt/$SERVICE_NAME/*"
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "tar -xzf /tmp/$backup_name.tar.gz -C /opt/$SERVICE_NAME/"
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "rm /tmp/$backup_name.tar.gz"
    
    # Restore database if applicable
    if [ -f "$backup_path/${backup_name}_db.sql.gz" ] && [ -n "${DB_NAME:-}" ]; then
        scp "$backup_path/${backup_name}_db.sql.gz" "$DEPLOY_USER@$DEPLOY_TARGET:/tmp/"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "gunzip -c /tmp/${backup_name}_db.sql.gz | psql $DB_NAME"
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "rm /tmp/${backup_name}_db.sql.gz"
    fi
    
    # Start service
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "systemctl start $SERVICE_NAME || docker start $SERVICE_NAME"
    
    # Health check
    sleep 10
    check_service_health
    
    log "INFO" "Rollback completed successfully"
}

# Post-deployment tasks
post_deploy_tasks() {
    log "INFO" "Running post-deployment tasks..."
    
    # Run database migrations
    if [ -n "${DB_NAME:-}" ] && [ "$ROLLBACK" = false ]; then
        ssh "$DEPLOY_USER@$DEPLOY_TARGET" "cd /opt/$SERVICE_NAME && ./bin/migrate.sh"
    fi
    
    # Clear caches
    ssh "$DEPLOY_USER@$DEPLOY_TARGET" "cd /opt/$SERVICE_NAME && ./bin/clear-cache.sh || true"
    
    # Update load balancer
    if [ -n "${LOAD_BALANCER_URL:-}" ]; then
        curl -X POST "$LOAD_BALANCER_URL/api/reload" || log "WARN" "Failed to reload load balancer"
    fi
    
    # Send notifications
    send_deployment_notification "success"
    
    log "INFO" "Post-deployment tasks completed"
}

# Send deployment notification
send_deployment_notification() {
    local status=$1
    local webhook_url="${SLACK_WEBHOOK_URL:-}"
    
    if [ -z "$webhook_url" ]; then
        return 0
    fi
    
    local color="good"
    if [ "$status" != "success" ]; then
        color="danger"
    fi
    
    local payload=$(cat << EOF
{
    "attachments": [
        {
            "color": "$color",
            "title": "Deployment $status",
            "fields": [
                {"title": "Service", "value": "$SERVICE_NAME", "short": true},
                {"title": "Environment", "value": "$ENVIRONMENT", "short": true},
                {"title": "Version", "value": "$VERSION", "short": true},
                {"title": "Deployed by", "value": "$(whoami)", "short": true}
            ],
            "ts": $(date +%s)
        }
    ]
}
EOF
    )
    
    curl -X POST -H 'Content-type: application/json' --data "$payload" "$webhook_url" || true
}

# Main deployment process
main() {
    log "INFO" "Starting deployment process..."
    
    # Validate inputs
    if [ -z "$ENVIRONMENT" ] || [ -z "$SERVICE_NAME" ]; then
        log "ERROR" "Environment and service name are required"
        usage
        exit 1
    fi
    
    if [ "$ROLLBACK" = false ] && [ -z "$VERSION" ]; then
        log "ERROR" "Version is required for deployment (not rollback)"
        usage
        exit 1
    fi
    
    # Load environment configuration
    load_env_config "$ENVIRONMENT"
    
    # Set deployment strategy
    local strategy="${DEPLOY_STRATEGY:-recreate}"
    
    if [ "$DRY_RUN" = true ]; then
        log "INFO" "[DRY RUN] Deployment simulation"
    fi
    
    # Execute deployment or rollback
    if [ "$ROLLBACK" = true ]; then
        rollback_deployment
    else
        pre_deploy_checks
        create_backup
        
        # Execute deployment strategy
        if [ -n "${DEPLOY_STRATEGIES[$strategy]:-}" ]; then
            ${DEPLOY_STRATEGIES[$strategy]}
        else
            log "ERROR" "Unknown deployment strategy: $strategy"
            exit 1
        fi
        
        post_deploy_tasks
    fi
    
    log "INFO" "Deployment process completed successfully"
}

# Usage information
usage() {
    cat << EOF
Multi-Environment Deployment Script

Usage: $0 -e ENVIRONMENT -s SERVICE_NAME [-v VERSION] [OPTIONS]

Required Arguments:
    -e, --environment   Target environment (dev/staging/prod)
    -s, --service       Service name to deploy

Optional Arguments:
    -v, --version       Version to deploy (required for deployment)
    -r, --rollback      Rollback to previous version
    -n, --dry-run       Simulate deployment without making changes
    -f, --force         Force deployment despite warnings
    -h, --help          Show this help message

Examples:
    $0 -e dev -s myapp -v 1.2.3                # Deploy version 1.2.3 to dev
    $0 -e prod -s myapp -v 2.0.0 --dry-run    # Simulate prod deployment
    $0 -e staging -s myapp --rollback          # Rollback staging deployment
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -s|--service)
            SERVICE_NAME="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -r|--rollback)
            ROLLBACK=true
            shift
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Error handling
trap 'log "ERROR" "Deployment failed at line $LINENO"; send_deployment_notification "failed"' ERR

# Create necessary directories
mkdir -p "$CONFIG_DIR" "$BACKUP_DIR"

# Run main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**🤖 Copilot Exercise 2:**
```
Create configuration files for the deployment script that support different cloud providers (AWS, Azure, GCP) and container orchestration platforms (Docker, Kubernetes).
```

---

## Part 4: CI/CD Integration Scripts

### 4.1 GitHub Actions Integration

```bash
#!/bin/bash
# CI/CD Integration Helper Script
# File: ci-cd-helper.sh

set -euo pipefail

# Generate GitHub Actions workflow
generate_github_workflow() {
    local project_type=$1
    local workflow_file=".github/workflows/ci-cd.yml"
    
    mkdir -p ".github/workflows"
    
    cat > "$workflow_file" << EOF
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.9'
  
jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Environment
      run: |
        echo "Setting up environment for $project_type"
        
EOF

    case $project_type in
        "nodejs")
            cat >> "$workflow_file" << EOF
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: \${{ env.NODE_VERSION }}
        cache: 'npm'
        
    - name: Install Dependencies
      run: npm ci
      
    - name: Run Tests
      run: npm test
      
    - name: Build
      run: npm run build
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
