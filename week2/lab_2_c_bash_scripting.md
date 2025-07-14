# Lab 2C: Basic Bash Scripting

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Write executable bash scripts with proper structure
- Handle command-line arguments and user input
- Implement conditional logic and loops
- Use GitHub Copilot to generate and improve scripts
- Apply best practices for script reliability and maintainability

## 📋 Prerequisites
- Completion of Labs 2A and 2B
- Understanding of basic Unix commands and data processing
- GitHub Copilot enabled

---

## Part 1: Script Fundamentals

### 1.1 Creating Your First Script

**💡 Copilot Prompt:**
```
Create a simple bash script template with shebang, comments, and basic structure. Include examples of variables, user input, and output.
```

```bash
#!/bin/bash
# Basic script template
# Author: Your Name
# Purpose: Demonstrate basic scripting concepts

# Variables
greeting="Hello, World!"
user_name="Student"
current_date=$(date)

# Output
echo "$greeting"
echo "Current user: $user_name"
echo "Today is: $current_date"
```

**Creating and running scripts:**
```bash
# Create script file
nano hello_world.sh

# Make executable
chmod +x hello_world.sh

# Run script
./hello_world.sh
```

### 1.2 Variables and Data Types

```bash
#!/bin/bash

# String variables
name="John Doe"
message='Single quotes preserve literal values'
path="/home/user/documents"

# Numeric variables
age=25
count=0
pi=3.14159

# Arrays
fruits=("apple" "banana" "cherry")
numbers=(1 2 3 4 5)

# Command substitution
current_user=$(whoami)
file_count=$(ls -1 | wc -l)
timestamp=`date +%Y%m%d_%H%M%S`  # Alternative syntax

# Environment variables
echo "Home directory: $HOME"
echo "Current PATH: $PATH"

# Variable operations
full_name="$first_name $last_name"
upper_name=${name^^}           # Convert to uppercase
lower_name=${name,,}           # Convert to lowercase
length=${#name}                # String length
```

**🤖 Copilot Exercise 1:**
```
Create a script that collects system information (hostname, user, date, disk usage) and formats it into a nice report. Use variables for all data collection.
```

---

## Part 2: Input and Output

### 2.1 Command Line Arguments

```bash
#!/bin/bash
# Script: process_args.sh
# Usage: ./process_args.sh arg1 arg2 arg3

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
echo "Process ID: $$"
echo "Exit status of last command: $?"

# Check if arguments provided
if [ $# -eq 0 ]; then
    echo "No arguments provided!"
    echo "Usage: $0 <arg1> <arg2> [arg3]"
    exit 1
fi

# Process arguments
for arg in "$@"; do
    echo "Processing: $arg"
done
```

### 2.2 User Input

```bash
#!/bin/bash
# Interactive input examples

# Simple input
echo "What's your name?"
read user_name
echo "Hello, $user_name!"

# Input with prompt
read -p "Enter your age: " age
read -p "Enter password (hidden): " -s password
echo  # New line after hidden input

# Input with timeout
read -t 10 -p "Enter choice (10 seconds): " choice
if [ $? -ne 0 ]; then
    echo "Timeout! Using default choice."
    choice="default"
fi

# Multiple inputs
echo "Enter your details:"
read -p "Name: " name
read -p "Email: " email
read -p "Phone: " phone

# Input validation
while true; do
    read -p "Enter a number (1-10): " num
    if [[ $num =~ ^[1-9]|10$ ]]; then
        break
    else
        echo "Invalid input! Please enter a number between 1 and 10."
    fi
done
```

### 2.3 Output Formatting

```bash
#!/bin/bash
# Output formatting examples

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${RED}This is red text${NC}"
echo -e "${GREEN}${BOLD}This is bold green text${NC}"

# Formatted output
printf "Name: %-20s Age: %3d\n" "John Doe" 25
printf "Progress: %3d%%\n" 75

# Here documents for multi-line output
cat << EOF
==========================
   System Report
==========================
Hostname: $(hostname)
User: $(whoami)
Date: $(date)
==========================
EOF
```

**📝 Exercise 1: Create an interactive calculator**
```bash
# Create a script that:
# 1. Asks for two numbers
# 2. Asks for operation (+, -, *, /)
# 3. Performs calculation
# 4. Displays formatted result
```

**💡 Copilot Prompt:**
```
Create an interactive calculator script that takes two numbers and an operation, validates input, performs the calculation, and handles division by zero.
```

---

## Part 3: Conditional Logic

### 3.1 If Statements

```bash
#!/bin/bash
# Conditional logic examples

# Basic if statement
age=18
if [ $age -ge 18 ]; then
    echo "You are an adult"
fi

# If-else
score=85
if [ $score -ge 90 ]; then
    echo "Grade: A"
else
    echo "Grade: B or lower"
fi

# If-elif-else
if [ $score -ge 90 ]; then
    echo "Grade: A"
elif [ $score -ge 80 ]; then
    echo "Grade: B"
elif [ $score -ge 70 ]; then
    echo "Grade: C"
else
    echo "Grade: F"
fi

# String comparisons
name="Alice"
if [ "$name" = "Alice" ]; then
    echo "Hello Alice!"
elif [ "$name" = "Bob" ]; then
    echo "Hello Bob!"
else
    echo "Hello stranger!"
fi

# File tests
filename="test.txt"
if [ -f "$filename" ]; then
    echo "$filename exists and is a regular file"
elif [ -d "$filename" ]; then
    echo "$filename is a directory"
else
    echo "$filename does not exist"
fi
```

### 3.2 Test Operators

```bash
#!/bin/bash
# Common test operators

# Numeric comparisons
# -eq (equal), -ne (not equal), -lt (less than)
# -le (less or equal), -gt (greater than), -ge (greater or equal)

# String comparisons
# = (equal), != (not equal), -z (empty), -n (not empty)

# File tests
# -f (regular file), -d (directory), -r (readable)
# -w (writable), -x (executable), -e (exists)

# Logical operators
if [ $age -ge 18 ] && [ $age -le 65 ]; then
    echo "Working age"
fi

if [ "$status" = "admin" ] || [ "$status" = "manager" ]; then
    echo "Authorized user"
fi

# Advanced test syntax [[ ]]
if [[ $name =~ ^[A-Z][a-z]+$ ]]; then
    echo "Valid name format"
fi
```

### 3.3 Case Statements

```bash
#!/bin/bash
# Case statement examples

read -p "Enter your choice (start/stop/restart/status): " action

case $action in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    status)
        echo "Checking service status..."
        ;;
    *)
        echo "Invalid option: $action"
        echo "Valid options: start, stop, restart, status"
        exit 1
        ;;
esac

# Pattern matching
case $filename in
    *.txt)
        echo "Text file"
        ;;
    *.pdf)
        echo "PDF file"
        ;;
    *.jpg|*.jpeg|*.png)
        echo "Image file"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac
```

**🤖 Copilot Exercise 2:**
```
Create a system health check script that tests various system conditions (disk space, memory usage, CPU load) and reports status with appropriate warnings using conditional logic.
```

---

## Part 4: Loops

### 4.1 For Loops

```bash
#!/bin/bash
# For loop examples

# Basic for loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# Range with brace expansion
for i in {1..10}; do
    echo "Count: $i"
done

# Step increment
for i in {0..20..2}; do
    echo "Even number: $i"
done

# Loop through files
for file in *.txt; do
    if [ -f "$file" ]; then
        echo "Processing: $file"
        wc -l "$file"
    fi
done

# Loop through command line arguments
for arg in "$@"; do
    echo "Argument: $arg"
done

# Array iteration
fruits=("apple" "banana" "cherry" "date")
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# C-style for loop
for ((i=1; i<=10; i++)); do
    echo "Counter: $i"
done
```

### 4.2 While Loops

```bash
#!/bin/bash
# While loop examples

# Basic while loop
counter=1
while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Reading file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < "input.txt"

# Infinite loop with break condition
while true; do
    read -p "Enter 'quit' to exit: " input
    if [ "$input" = "quit" ]; then
        break
    fi
    echo "You entered: $input"
done

# While with condition check
while [ -f "lock.file" ]; do
    echo "Waiting for lock file to be removed..."
    sleep 5
done
```

### 4.3 Until Loops

```bash
#!/bin/bash
# Until loop examples

# Wait until condition becomes true
until [ -f "ready.flag" ]; do
    echo "Waiting for ready flag..."
    sleep 2
done

# Countdown
countdown=10
until [ $countdown -eq 0 ]; do
    echo "Countdown: $countdown"
    ((countdown--))
    sleep 1
done
echo "Launch!"
```

**📝 Exercise 2: File processor**
Create a script that:
1. Loops through all .log files in a directory
2. For each file, counts lines, words, and characters
3. Displays a summary report

**💡 Copilot Prompt:**
```
Create a script that processes all log files in a directory, extracts error counts, and generates a summary report with totals and percentages.
```

---

## Part 5: Functions and Script Organization

### 5.1 Function Basics

```bash
#!/bin/bash
# Function examples

# Simple function
greet() {
    echo "Hello, World!"
}

# Function with parameters
greet_user() {
    local name=$1
    local time=$2
    echo "Good $time, $name!"
}

# Function with return value
add_numbers() {
    local num1=$1
    local num2=$2
    local result=$((num1 + num2))
    echo $result
}

# Function with local variables
process_file() {
    local filename=$1
    local line_count
    local word_count
    
    if [ -f "$filename" ]; then
        line_count=$(wc -l < "$filename")
        word_count=$(wc -w < "$filename")
        echo "File: $filename, Lines: $line_count, Words: $word_count"
        return 0
    else
        echo "Error: File $filename not found"
        return 1
    fi
}

# Using functions
greet
greet_user "Alice" "morning"
result=$(add_numbers 10 20)
echo "Sum: $result"

process_file "example.txt"
if [ $? -eq 0 ]; then
    echo "File processed successfully"
fi
```

### 5.2 Error Handling

```bash
#!/bin/bash
# Error handling examples

# Exit on error
set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error
set -o pipefail  # Pipe failure causes script to fail

# Custom error handling
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Validate input
validate_file() {
    local file=$1
    if [ -z "$file" ]; then
        error_exit "No filename provided"
    fi
    
    if [ ! -f "$file" ]; then
        error_exit "File '$file' does not exist"
    fi
    
    if [ ! -r "$file" ]; then
        error_exit "File '$file' is not readable"
    fi
}

# Trap for cleanup
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/script_temp_*
}
trap cleanup EXIT

# Safe command execution
safe_run() {
    local command="$1"
    if ! $command; then
        error_exit "Command failed: $command"
    fi
}
```

**🤖 Copilot Exercise 3:**
```
Create a robust backup script with functions for validation, compression, and cleanup. Include proper error handling and logging.
```

---

## Part 6: Practical Script Examples

### 6.1 System Administration Script

```bash
#!/bin/bash
# System monitoring script

# Configuration
LOG_FILE="/var/log/system_monitor.log"
EMAIL="admin@example.com"
DISK_THRESHOLD=80
MEMORY_THRESHOLD=90

# Functions
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_disk_usage() {
    local usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ $usage -gt $DISK_THRESHOLD ]; then
        log_message "WARNING: Disk usage is ${usage}%"
        return 1
    fi
    log_message "INFO: Disk usage is ${usage}%"
    return 0
}

check_memory_usage() {
    local usage=$(free | awk 'NR==2 {printf "%.0f", $3/$2*100}')
    if [ $usage -gt $MEMORY_THRESHOLD ]; then
        log_message "WARNING: Memory usage is ${usage}%"
        return 1
    fi
    log_message "INFO: Memory usage is ${usage}%"
    return 0
}

# Main execution
log_message "Starting system check"
check_disk_usage
check_memory_usage
log_message "System check completed"
```

### 6.2 Development Helper Script

```bash
#!/bin/bash
# Development project setup script

setup_project() {
    local project_name=$1
    local project_type=$2
    
    echo "Setting up $project_type project: $project_name"
    
    # Create directory structure
    mkdir -p "$project_name"/{src,tests,docs,config}
    
    case $project_type in
        "python")
            touch "$project_name"/requirements.txt
            touch "$project_name"/README.md
            touch "$project_name"/src/__init__.py
            echo "print('Hello from $project_name')" > "$project_name"/src/main.py
            ;;
        "node")
            cd "$project_name"
            npm init -y
            mkdir -p public src
            echo "console.log('Hello from $project_name');" > src/index.js
            ;;
        "bash")
            touch "$project_name"/src/main.sh
            chmod +x "$project_name"/src/main.sh
            echo "#!/bin/bash" > "$project_name"/src/main.sh
            echo "echo 'Hello from $project_name'" >> "$project_name"/src/main.sh
            ;;
    esac
    
    echo "Project $project_name created successfully!"
}

# Usage check
if [ $# -ne 2 ]; then
    echo "Usage: $0 <project_name> <project_type>"
    echo "Project types: python, node, bash"
    exit 1
fi

setup_project "$1" "$2"
```

**📝 Exercise 3: Personal project script**
Create a script that solves a real problem you face. Ideas:
- File organizer
- Git repository manager
- System backup tool
- Development environment setup

---

## Part 7: Advanced Scripting Techniques

### 7.1 Configuration Files

```bash
#!/bin/bash
# Script with configuration file support

CONFIG_FILE="$HOME/.myscript.conf"

# Default configuration
DEFAULT_BACKUP_DIR="/backup"
DEFAULT_LOG_LEVEL="INFO"
DEFAULT_MAX_BACKUPS=5

# Load configuration
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    else
        # Create default config
        cat > "$CONFIG_FILE" << EOF
# My Script Configuration
BACKUP_DIR="$DEFAULT_BACKUP_DIR"
LOG_LEVEL="$DEFAULT_LOG_LEVEL"
MAX_BACKUPS=$DEFAULT_MAX_BACKUPS
EOF
    fi
}

# Use configuration
load_config
echo "Backup directory: $BACKUP_DIR"
echo "Log level: $LOG_LEVEL"
echo "Max backups: $MAX_BACKUPS"
```

### 7.2 Signal Handling

```bash
#!/bin/bash
# Signal handling example

# Signal handler
handle_signal() {
    echo "Received signal, cleaning up..."
    # Cleanup code here
    exit 0
}

# Register signal handlers
trap handle_signal SIGINT SIGTERM

# Main loop
while true; do
    echo "Running... (Press Ctrl+C to stop)"
    sleep 5
done
```

**🤖 Copilot Exercise 4:**
```
Create a comprehensive deployment script that reads configuration from a file, handles different environments (dev/staging/prod), includes rollback functionality, and proper logging.
```

---

## Part 8: Lab Challenges

### Challenge 1: Log Analyzer
Create a script that:
- Processes web server log files
- Extracts statistics (top IPs, error codes, popular pages)
- Generates HTML report
- Handles large files efficiently

### Challenge 2: Backup Manager
Create a backup script that:
- Supports multiple backup strategies (full, incremental)
- Compresses and encrypts backups
- Manages retention policies
- Sends notifications on success/failure

### Challenge 3: Development Workflow Automation
Create a script that:
- Sets up development environments
- Manages dependencies
- Runs tests and builds
- Deploys to different environments

**💡 Copilot Prompt for All Challenges:**
```
For each challenge, create a complete script with proper structure, error handling, logging, and documentation. Include usage examples and configuration options.
```

---

## 🎯 Lab Deliverables

Submit the following:

1. **Three Complete Scripts**: One for each major section (system admin, development, personal utility)

2. **Script Documentation**: README files explaining usage, configuration, and examples

3. **Error Handling Examples**: Demonstration of robust error handling in your scripts

4. **Performance Analysis**: Comparison of different scripting approaches for the same task

---

## ✅ Validation Steps

1. All scripts execute without syntax errors
2. Proper handling of command-line arguments and user input
3. Effective use of conditional logic and loops
4. Functions are used appropriately for code organization
5. Error handling prevents script crashes
6. Scripts follow bash best practices

---

## 🔗 Additional Resources

**Advanced Copilot Prompts:**
```
Show me how to create a bash script that interfaces with REST APIs
Generate a script for automated testing of other bash scripts
Create a script that manages multiple concurrent processes
Explain how to optimize bash scripts for performance
```

**Next Steps**: This lab prepares you for Lab 2D where you'll learn build automation and deployment scripting.

---

**📚 Key Takeaways:**
- Structure scripts with proper organization and error handling
- Use functions to create reusable and maintainable code
- Implement robust input validation and user interaction
- Apply conditional logic and loops effectively
- Leverage Copilot for script generation and optimization
