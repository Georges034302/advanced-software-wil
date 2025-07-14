# Lab 2D: Build Automation and Development Environment Setup

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Create automated build and deployment scripts
- Set up reproducible development environments
- Implement CI/CD preparation scripts
- Use GitHub Copilot to generate complex automation workflows
- Apply advanced scripting techniques for production environments

## 📋 Prerequisites
- Completion of Labs 2A, 2B, and 2C
- Understanding of bash scripting fundamentals
- Basic knowledge of development workflows
- GitHub Copilot enabled

---

## Part 1: Development Environment Automation

### 1.1 Environment Setup Scripts

**💡 Copilot Prompt:**
```
Create a comprehensive development environment setup script that installs common development tools (git, node, python, docker) with version checking and cross-platform support.
```

```bash
#!/bin/bash
# Development Environment Setup Script
# File: setup_dev_env.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$HOME/dev_setup.log"
REQUIRED_TOOLS=("git" "curl" "wget" "unzip")

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
}

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        DISTRO="macOS"
    else
        log "ERROR" "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    log "INFO" "Detected OS: $OS ($DISTRO)"
}

# Check if tool is installed
check_tool() {
    local tool=$1
    if command -v "$tool" &> /dev/null; then
        local version=$(${tool} --version 2>/dev/null | head -1 || echo "Unknown version")
        log "INFO" "$tool is installed: $version"
        return 0
    else
        log "WARN" "$tool is not installed"
        return 1
    fi
}

# Install Node.js and npm
install_nodejs() {
    log "INFO" "Installing Node.js..."
    
    if check_tool "node"; then
        log "INFO" "Node.js already installed"
        return 0
    fi
    
    # Install Node Version Manager (nvm)
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    # Install latest LTS Node.js
    nvm install --lts
    nvm use --lts
    nvm alias default lts/*
    
    log "INFO" "Node.js installation completed"
}

# Install Python and pip
install_python() {
    log "INFO" "Installing Python..."
    
    if check_tool "python3"; then
        log "INFO" "Python3 already installed"
        return 0
    fi
    
    case $OS in
        "linux")
            case $DISTRO in
                "Ubuntu"|"Debian")
                    sudo apt update
                    sudo apt install -y python3 python3-pip python3-venv
                    ;;
                "CentOS"|"RHEL"|"Fedora")
                    sudo yum install -y python3 python3-pip
                    ;;
                *)
                    log "ERROR" "Unsupported Linux distribution: $DISTRO"
                    return 1
                    ;;
            esac
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install python3
            else
                log "ERROR" "Homebrew not found. Please install Homebrew first."
                return 1
            fi
            ;;
    esac
    
    log "INFO" "Python installation completed"
}

# Install Docker
install_docker() {
    log "INFO" "Installing Docker..."
    
    if check_tool "docker"; then
        log "INFO" "Docker already installed"
        return 0
    fi
    
    case $OS in
        "linux")
            # Official Docker installation script
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
            ;;
        "macos")
            log "INFO" "Please install Docker Desktop for Mac from https://docker.com"
            ;;
    esac
    
    log "INFO" "Docker installation completed"
}

# Setup Git configuration
setup_git() {
    log "INFO" "Setting up Git configuration..."
    
    if ! check_tool "git"; then
        case $OS in
            "linux")
                sudo apt install -y git || sudo yum install -y git
                ;;
            "macos")
                xcode-select --install
                ;;
        esac
    fi
    
    # Configure Git if not already configured
    if [ -z "$(git config --global user.name 2>/dev/null)" ]; then
        read -p "Enter your Git username: " git_username
        git config --global user.name "$git_username"
    fi
    
    if [ -z "$(git config --global user.email 2>/dev/null)" ]; then
        read -p "Enter your Git email: " git_email
        git config --global user.email "$git_email"
    fi
    
    # Set up useful Git aliases
    git config --global alias.st status
    git config --global alias.co checkout
    git config --global alias.br branch
    git config --global alias.up "pull --rebase"
    git config --global alias.lg "log --oneline --graph --decorate"
    
    log "INFO" "Git configuration completed"
}

# Install VS Code extensions
install_vscode_extensions() {
    log "INFO" "Installing VS Code extensions..."
    
    if ! check_tool "code"; then
        log "WARN" "VS Code not found, skipping extension installation"
        return 0
    fi
    
    local extensions=(
        "ms-vscode.vscode-typescript-next"
        "ms-python.python"
        "ms-vscode.vscode-json"
        "redhat.vscode-yaml"
        "ms-azuretools.vscode-docker"
        "GitHub.copilot"
        "ms-vscode.powershell"
    )
    
    for ext in "${extensions[@]}"; do
        code --install-extension "$ext" --force
    done
    
    log "INFO" "VS Code extensions installation completed"
}

# Main execution
main() {
    log "INFO" "Starting development environment setup..."
    
    check_os
    
    # Check required tools
    for tool in "${REQUIRED_TOOLS[@]}"; do
        if ! check_tool "$tool"; then
            log "ERROR" "Required tool $tool is missing. Please install it first."
            exit 1
        fi
    done
    
    # Install development tools
    setup_git
    install_python
    install_nodejs
    install_docker
    install_vscode_extensions
    
    log "INFO" "Development environment setup completed!"
    log "INFO" "Please restart your terminal or run 'source ~/.bashrc' to apply changes."
}

# Script usage
usage() {
    cat << EOF
Development Environment Setup Script

Usage: $0 [OPTIONS]

Options:
    -h, --help          Show this help message
    -l, --log-file      Specify log file location (default: $LOG_FILE)
    --skip-docker       Skip Docker installation
    --skip-vscode       Skip VS Code extensions installation

Examples:
    $0                  # Full installation
    $0 --skip-docker    # Install everything except Docker
    $0 -l /tmp/setup.log # Use custom log file
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -l|--log-file)
            LOG_FILE="$2"
            shift 2
            ;;
        --skip-docker)
            SKIP_DOCKER=true
            shift
            ;;
        --skip-vscode)
            SKIP_VSCODE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Run main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**📝 Exercise 1: Customize the environment script**
Modify the above script to include tools specific to your development stack (e.g., Java, Go, Rust, specific databases).

---

## Part 2: Build Automation Scripts

### 2.1 Universal Build Script

**💡 Copilot Prompt:**
```
Create a universal build script that detects project type (Node.js, Python, Java, etc.) and runs appropriate build commands with dependency management, testing, and packaging.
```

```bash
#!/bin/bash
# Universal Build Script
# File: build.sh

set -euo pipefail

# Configuration
BUILD_DIR="./build"
DIST_DIR="./dist"
LOG_FILE="./build.log"
VERBOSE=false
CLEAN=false
TEST=true
PACKAGE=false

# Project detection
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "nodejs"
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
        echo "python"
    elif [ -f "pom.xml" ]; then
        echo "maven"
    elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
        echo "gradle"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Dockerfile" ]; then
        echo "docker"
    else
        echo "unknown"
    fi
}

# Logging
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%H:%M:%S')
    
    if [ "$VERBOSE" = true ] || [ "$level" != "DEBUG" ]; then
        echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
    fi
}

# Clean build artifacts
clean_build() {
    log "INFO" "Cleaning build artifacts..."
    
    rm -rf "$BUILD_DIR" "$DIST_DIR"
    
    case $PROJECT_TYPE in
        "nodejs")
            rm -rf node_modules/.cache
            ;;
        "python")
            find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
            find . -type f -name "*.pyc" -delete 2>/dev/null || true
            rm -rf .pytest_cache build dist *.egg-info
            ;;
        "java"|"maven")
            mvn clean &>/dev/null || true
            ;;
        "gradle")
            ./gradlew clean &>/dev/null || true
            ;;
        "rust")
            cargo clean &>/dev/null || true
            ;;
        "go")
            go clean -cache &>/dev/null || true
            ;;
    esac
    
    log "INFO" "Clean completed"
}

# Install dependencies
install_dependencies() {
    log "INFO" "Installing dependencies for $PROJECT_TYPE project..."
    
    case $PROJECT_TYPE in
        "nodejs")
            if [ -f "package-lock.json" ]; then
                npm ci
            else
                npm install
            fi
            ;;
        "python")
            if [ -f "requirements.txt" ]; then
                pip install -r requirements.txt
            elif [ -f "pyproject.toml" ]; then
                pip install -e .
            fi
            ;;
        "maven")
            mvn dependency:resolve
            ;;
        "gradle")
            ./gradlew build --refresh-dependencies
            ;;
        "rust")
            cargo fetch
            ;;
        "go")
            go mod download
            ;;
    esac
    
    log "INFO" "Dependencies installed"
}

# Run tests
run_tests() {
    if [ "$TEST" = false ]; then
        log "INFO" "Skipping tests"
        return 0
    fi
    
    log "INFO" "Running tests..."
    
    case $PROJECT_TYPE in
        "nodejs")
            npm test
            ;;
        "python")
            if command -v pytest &> /dev/null; then
                pytest
            elif [ -f "test.py" ]; then
                python test.py
            else
                python -m unittest discover
            fi
            ;;
        "maven")
            mvn test
            ;;
        "gradle")
            ./gradlew test
            ;;
        "rust")
            cargo test
            ;;
        "go")
            go test ./...
            ;;
    esac
    
    log "INFO" "Tests completed"
}

# Build project
build_project() {
    log "INFO" "Building $PROJECT_TYPE project..."
    
    mkdir -p "$BUILD_DIR"
    
    case $PROJECT_TYPE in
        "nodejs")
            if grep -q "\"build\":" package.json; then
                npm run build
            else
                log "WARN" "No build script found in package.json"
            fi
            ;;
        "python")
            if [ -f "setup.py" ]; then
                python setup.py build
            else
                log "INFO" "No build step required for Python project"
            fi
            ;;
        "maven")
            mvn compile
            ;;
        "gradle")
            ./gradlew build
            ;;
        "rust")
            cargo build --release
            ;;
        "go")
            go build -o "$BUILD_DIR/" ./...
            ;;
        "docker")
            docker build -t $(basename $(pwd)):latest .
            ;;
    esac
    
    log "INFO" "Build completed"
}

# Package project
package_project() {
    if [ "$PACKAGE" = false ]; then
        log "INFO" "Skipping packaging"
        return 0
    fi
    
    log "INFO" "Packaging project..."
    
    mkdir -p "$DIST_DIR"
    
    case $PROJECT_TYPE in
        "nodejs")
            if grep -q "\"pack\":" package.json; then
                npm run pack
            else
                npm pack --pack-destination="$DIST_DIR"
            fi
            ;;
        "python")
            python setup.py sdist bdist_wheel
            mv dist/* "$DIST_DIR/" 2>/dev/null || true
            ;;
        "maven")
            mvn package
            cp target/*.jar "$DIST_DIR/" 2>/dev/null || true
            ;;
        "gradle")
            ./gradlew assemble
            cp build/libs/*.jar "$DIST_DIR/" 2>/dev/null || true
            ;;
        "rust")
            cargo build --release
            cp target/release/* "$DIST_DIR/" 2>/dev/null || true
            ;;
        "go")
            go build -o "$DIST_DIR/" ./...
            ;;
    esac
    
    log "INFO" "Packaging completed"
}

# Generate build report
generate_report() {
    local end_time=$(date)
    local build_status="SUCCESS"
    
    cat > build-report.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Build Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .success { color: green; }
        .error { color: red; }
        .info { color: blue; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Build Report</h1>
    <p><strong>Project Type:</strong> $PROJECT_TYPE</p>
    <p><strong>Build Time:</strong> $end_time</p>
    <p><strong>Status:</strong> <span class="success">$build_status</span></p>
    
    <h2>Build Log</h2>
    <pre>$(cat "$LOG_FILE")</pre>
    
    <h2>Build Artifacts</h2>
    <ul>
EOF

    if [ -d "$BUILD_DIR" ]; then
        find "$BUILD_DIR" -type f | while read file; do
            echo "        <li>$file</li>" >> build-report.html
        done
    fi
    
    if [ -d "$DIST_DIR" ]; then
        find "$DIST_DIR" -type f | while read file; do
            echo "        <li>$file</li>" >> build-report.html
        done
    fi
    
    cat >> build-report.html << EOF
    </ul>
</body>
</html>
EOF
    
    log "INFO" "Build report generated: build-report.html"
}

# Main build process
main() {
    local start_time=$(date)
    log "INFO" "Starting build process at $start_time"
    
    # Detect project type
    PROJECT_TYPE=$(detect_project_type)
    log "INFO" "Detected project type: $PROJECT_TYPE"
    
    if [ "$PROJECT_TYPE" = "unknown" ]; then
        log "ERROR" "Unable to detect project type"
        exit 1
    fi
    
    # Execute build steps
    if [ "$CLEAN" = true ]; then
        clean_build
    fi
    
    install_dependencies
    run_tests
    build_project
    package_project
    generate_report
    
    log "INFO" "Build process completed successfully"
}

# Usage information
usage() {
    cat << EOF
Universal Build Script

Usage: $0 [OPTIONS]

Options:
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output
    -c, --clean         Clean build artifacts before building
    --no-test          Skip running tests
    -p, --package      Create distribution packages
    --type TYPE        Force project type detection (nodejs, python, maven, etc.)

Examples:
    $0                  # Basic build
    $0 -c -p           # Clean build with packaging
    $0 --no-test -v    # Build without tests, verbose output
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        --no-test)
            TEST=false
            shift
            ;;
        -p|--package)
            PACKAGE=true
            shift
            ;;
        --type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Error handling
trap 'log "ERROR" "Build failed at line $LINENO"' ERR

# Run main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**🤖 Copilot Exercise 1:**
```
Extend the build script to support additional project types (PHP, Ruby, .NET Core) and add performance monitoring to track build times for optimization.
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

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "\${var.app_name}-alb-$environment"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.app.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = false
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "\${var.app_name}-cluster-$environment"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}
EOF

    # Variables
    cat > "$IAC_DIR/aws/$environment/variables.tf" << EOF
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "$app_name"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}
EOF

    # Outputs
    cat > "$IAC_DIR/aws/$environment/outputs.tf" << EOF
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "security_group_id" {
  value = aws_security_group.app.id
}

output "load_balancer_dns" {
  value = aws_lb.main.dns_name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}
EOF

    log "AWS Terraform configuration generated for $environment"
}

# Terraform operations
terraform_init() {
    local provider=$1
    local environment=$2
    
    cd "$IAC_DIR/$provider/$environment"
    
    log "Initializing Terraform for $provider/$environment..."
    terraform init
}

terraform_plan() {
    local provider=$1
    local environment=$2
    
    cd "$IAC_DIR/$provider/$environment"
    
    log "Creating Terraform plan for $provider/$environment..."
    terraform plan -out="tfplan"
}

terraform_apply() {
    local provider=$1
    local environment=$2
    
    cd "$IAC_DIR/$provider/$environment"
    
    log "Applying Terraform plan for $provider/$environment..."
    terraform apply "tfplan"
}

terraform_destroy() {
    local provider=$1
    local environment=$2
    
    cd "$IAC_DIR/$provider/$environment"
    
    log "Destroying infrastructure for $provider/$environment..."
    terraform destroy -auto-approve
}

# Main function
main() {
    local action=$1
    local provider=${2:-"aws"}
    local environment=${3:-"dev"}
    local app_name=${4:-"myapp"}
    
    case $action in
        "init")
            install_terraform
            ;;
        "generate")
            case $provider in
                "aws")
                    generate_aws_config "$environment" "$app_name"
                    ;;
                *)
                    log "Unsupported provider: $provider"
                    exit 1
                    ;;
            esac
            ;;
        "plan")
            terraform_init "$provider" "$environment"
            terraform_plan "$provider" "$environment"
            ;;
        "apply")
            terraform_apply "$provider" "$environment"
            ;;
        "destroy")
            terraform_destroy "$provider" "$environment"
            ;;
        *)
            echo "Usage: $0 {init|generate|plan|apply|destroy} [provider] [environment] [app_name]"
            exit 1
            ;;
    esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**🤖 Copilot Exercise 3:**
```
Extend the IaC manager to support Azure Resource Manager templates and Google Cloud Deployment Manager, with cross-cloud resource mapping and cost estimation.
```

---

## Part 6: Lab Challenges

### Challenge 1: Complete DevOps Pipeline
Create a comprehensive automation suite that:
- Sets up development environments automatically
- Builds and tests applications across multiple platforms
- Deploys to multiple environments with different strategies
- Monitors deployments and handles rollbacks
- Generates reports and notifications

### Challenge 2: Multi-Cloud Deployment
Build scripts that:
- Deploy the same application to AWS, Azure, and GCP
- Handle cloud-specific configurations
- Manage secrets across different platforms
- Implement disaster recovery procedures

### Challenge 3: Microservices Automation
Create automation for:
- Setting up microservices architectures
- Managing service dependencies
- Orchestrating deployments across services
- Monitoring service health and performance

**💡 Copilot Prompt for All Challenges:**
```
For each challenge, create production-ready scripts with comprehensive error handling, logging, monitoring, and documentation. Include performance optimization and security best practices.
```

---

## 🎯 Lab Deliverables

Submit the following:

1. **Complete Automation Suite**: Collection of scripts covering setup, build, deployment, and monitoring

2. **Infrastructure Code**: Terraform/CloudFormation templates for at least two cloud providers

3. **CI/CD Workflows**: GitHub Actions or similar CI/CD configurations

4. **Documentation**: Comprehensive guides for using your automation scripts

5. **Performance Analysis**: Benchmarks and optimization reports for your automation

---

## ✅ Validation Steps

1. Scripts execute successfully across different environments
2. Error handling prevents failures and provides useful feedback
3. Logging and monitoring provide visibility into automation processes
4. Rollback procedures work correctly
5. Performance meets acceptable standards for production use

---

## 🔗 Additional Resources

**Advanced Copilot Prompts:**
```
Create a script that automatically scales infrastructure based on application metrics
Generate automation for compliance scanning and security hardening
Build a script that manages feature flags across multiple environments
Create disaster recovery automation with RTO/RPO targets
```

**Course Integration**: These automation skills prepare you for the upcoming Docker, CI/CD, and Azure modules where you'll apply these concepts at scale.

---

**📚 Key Takeaways:**
- Automate repetitive development and deployment tasks
- Create reproducible and reliable infrastructure deployments
- Implement comprehensive monitoring and rollback procedures
- Use Infrastructure as Code for consistent environments
- Leverage Copilot for complex automation script generation
