# Lab 2D: Simple Development Helpers

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Create basic automation scripts for daily development tasks
- Build simple project setup helpers
- Use bash scripting to solve common problems
- Start development servers easily

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

## Part 3: Conclusion

### 3.1 Review

You've learned to create simple automation scripts that help with daily development tasks:

1. **Project Setup Helpers** - Quick ways to start new HTML and Python projects
2. **Development Servers** - Easy ways to test your code locally

These scripts are building blocks - you can modify them as you learn more bash commands!

### 3.2 Next Steps

**Ways to improve these scripts:**
- Add more file types to the project creators
- Make the servers handle errors better
- Add command line options to the scripts
- Create templates for other languages

**🤖 Copilot Tips for Script Writing:**
- Start prompts with "Create a simple bash script that..."
- Ask for explanations: "Explain what each line does"
- Request improvements: "Make this script safer" or "Add user-friendly messages"

### 3.3 Key Takeaways

✅ **Small scripts are powerful** - Even 10-20 lines can save lots of time  
✅ **Automate repetitive tasks** - If you do it twice, consider scripting it  
✅ **Start simple** - You can always make scripts more complex later  
✅ **Use echo for feedback** - Let users know what's happening  

Remember: The best automation script is one you actually use! Start with simple versions and improve them as you get more comfortable with bash.

### 3.4 Validation

**Lab Complete! Check that you can:**
- ✅ Create a new HTML project using your script
- ✅ Create a new Python project using your script
- ✅ Start a local web server to view HTML files
- ✅ Run Python scripts easily with your runner script
- ✅ Understand how each script works line by line

**Next Lab Preview:**
In the next module, you'll learn about more advanced automation concepts and explore real-world development workflows.

---

*Lab 2D: Simple Development Helpers - Complete* 🎉
