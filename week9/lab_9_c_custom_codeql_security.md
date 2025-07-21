# 🔐 Lab 9C: Custom CodeQL Security Queries and Dependabot

## 🎯 Objective
Create custom CodeQL queries to detect specific security issues in a simple Python app, plus automated dependency management.

- Build simple Flask app with security vulnerabilities
- Write custom CodeQL queries for SQL injection detection
- Write custom CodeQL queries for hardcoded secrets detection
- Configure Dependabot for dependency updates
- Test security detection and fixes

## 🗂 Structure
```
lab9d/
├── .github/
│   ├── workflows/
│   │   └── custom-security.yml
│   └── dependabot.yml
├── .codeql/
│   └── queries/
│       ├── sql-injection.ql
│       └── hardcoded-secrets.ql
├── app.py
├── requirements.txt
└── README.md
```

## ✅ Step 1: Simple Python App

### `app.py`
```python
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# ❌ Hardcoded secrets for CodeQL to detect
API_KEY = "sk-1234567890abcdef1234567890abcdef"
DATABASE_PASSWORD = "MySecretPassword123"
SECRET_TOKEN = "hardcoded-jwt-secret-key"

@app.route('/')
def home():
    return '''
    <h1>Simple Blog App</h1>
    <form action="/search" method="post">
        <input name="query" placeholder="Search posts">
        <button type="submit">Search</button>
    </form>
    <form action="/login" method="post">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/search', methods=['POST'])
def search_posts():
    query = request.form.get('query')
    
    # ❌ SQL injection vulnerability for CodeQL to detect
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Dangerous: direct string concatenation
    sql = f"SELECT * FROM posts WHERE title LIKE '%{query}%'"
    cursor.execute(sql)
    
    results = cursor.fetchall()
    conn.close()
    
    html = "<h2>Search Results:</h2><ul>"
    for post in results:
        html += f"<li>{post[1]} - {post[2]}</li>"
    html += "</ul>"
    
    return html

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # ❌ Another SQL injection vulnerability
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Dangerous: user input directly in SQL
    sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(sql)
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return f"Welcome {user[1]}! Your API key is: {API_KEY}"
    else:
        return "Login failed"

if __name__ == '__main__':
    # Create test database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
                     (id INTEGER, title TEXT, content TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER, username TEXT, password TEXT)''')
    
    cursor.execute("INSERT OR IGNORE INTO posts VALUES (1, 'Hello World', 'First post')")
    cursor.execute("INSERT OR IGNORE INTO posts VALUES (2, 'Python Tips', 'Learn Python')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123')")
    
    conn.commit()
    conn.close()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### `requirements.txt`
```
Flask==2.3.0
requests==2.28.0
```

## ✅ Step 2: Custom CodeQL Query for SQL Injection

### `.codeql/queries/sql-injection.ql`
```ql
/**
 * @name SQL injection in Python
 * @description Detects SQL injection vulnerabilities from user input
 * @kind path-problem
 * @problem.severity error
 * @security-severity 9.0
 * @precision high
 * @id python/sql-injection-custom
 * @tags security
 *       external/cwe/cwe-89
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking

/**
 * A data flow source for user input from Flask requests.
 */
class FlaskUserInput extends DataFlow::Node {
  FlaskUserInput() {
    exists(Attribute attr, Name request |
      this.asExpr() = attr and
      attr.getObject() = request and
      request.getId() = "request" and
      attr.getName() in ["form", "args", "json", "data"]
    )
  }
}

/**
 * A data flow sink for SQL execution.
 */
class SqlExecution extends DataFlow::Node {
  SqlExecution() {
    exists(Call call |
      this.asExpr() = call and
      call.getFunc().(Attribute).getName() = "execute" and
      call.getReceiver().getType().getName() = "Cursor"
    )
  }
}

/**
 * Taint tracking configuration for SQL injection.
 */
class SqlInjectionConfig extends TaintTracking::Configuration {
  SqlInjectionConfig() { this = "SqlInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof FlaskUserInput
  }

  override predicate isSink(DataFlow::Node sink) {
    sink instanceof SqlExecution
  }
}

from SqlInjectionConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink, 
  "SQL injection: user input from $@ flows to SQL execution.", 
  source.getNode(), "Flask request"
```

## ✅ Step 3: Custom CodeQL Query for Hardcoded Secrets

### `.codeql/queries/hardcoded-secrets.ql`
```ql
/**
 * @name Hardcoded secrets in Python
 * @description Finds hardcoded API keys, passwords, and secrets
 * @kind problem
 * @problem.severity error
 * @security-severity 8.0
 * @precision high
 * @id python/hardcoded-secrets-custom
 * @tags security
 *       external/cwe/cwe-798
 */

import python

/**
 * A string literal that looks like a secret.
 */
class PotentialSecret extends StrConst {
  PotentialSecret() {
    exists(string value | value = this.getText() |
      // Look for common secret patterns
      (
        // API keys (starts with specific prefixes)
        value.regexpMatch("sk-[A-Za-z0-9]{32,}") or
        value.regexpMatch("pk_[A-Za-z0-9]{24,}") or
        value.regexpMatch("[A-Za-z0-9]{32,}") or
        // Passwords with common patterns
        value.regexpMatch(".*[Pp]assword.*") or
        value.regexpMatch(".*[Ss]ecret.*") or
        value.regexpMatch(".*[Tt]oken.*") or
        value.regexpMatch(".*[Kk]ey.*")
      ) and
      value.length() > 10 and
      // Exclude obvious test/example values
      not value.regexpMatch(".*(?i)(example|test|demo|placeholder|sample|your_|<|>|\\{|\\}).*")
    )
  }
}

/**
 * An assignment to a variable with a suspicious name.
 */
class SuspiciousAssignment extends Assign {
  SuspiciousAssignment() {
    exists(Name target |
      this.getTarget() = target and
      target.getId().regexpMatch(".*(?i)(api_key|apikey|secret|password|passwd|token|key).*")
    )
  }
}

from SuspiciousAssignment assign, PotentialSecret secret
where assign.getValue() = secret
select secret, 
  "Hardcoded secret assigned to variable '" + 
  assign.getTarget().(Name).getId() + "'"
```

## ✅ Step 4: GitHub Actions with Custom CodeQL

### `.github/workflows/custom-security.yml`
```yaml
name: "Custom Security Analysis"

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  custom-codeql:
    name: Custom CodeQL Analysis
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: python
        queries: ./.codeql/queries/

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
      with:
        category: "/language:python"

  test-app:
    name: Test Application
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Test app startup
      run: |
        python app.py &
        sleep 3
        curl -f http://localhost:5000 || exit 1
        echo "App started successfully"
```

### `.github/dependabot.yml`
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "deps"
    reviewers:
      - "security-team"
```

## ✅ Step 5: Test the Application

### Run Locally
```bash
# Create project directory
mkdir lab9d
cd lab9d

# Create all the files above
# Then install and run

pip install -r requirements.txt
python app.py
```

### Test Vulnerabilities
```bash
# Open http://localhost:5000

# Test SQL injection in search:
# Enter: '; DROP TABLE posts; --

# Test SQL injection in login:
# Username: admin' OR '1'='1
# Password: anything
```

## ✅ Step 6: Setup GitHub Repository

### Initialize Repository
```bash
# Initialize git
git init
git branch -M main

# Create GitHub repository and add remote
git remote add origin https://github.com/your-username/lab9d-custom-codeql.git

# Create directory structure
mkdir -p .github/workflows
mkdir -p .codeql/queries

# Add all files
git add .
git commit -m "feat: add simple app with custom CodeQL queries

- Flask app with SQL injection vulnerabilities
- Custom CodeQL query for SQL injection detection
- Custom CodeQL query for hardcoded secrets detection
- Dependabot configuration for dependency updates"

# Push to GitHub
git push -u origin main
```

## ✅ Step 7: View Custom CodeQL Results

### Check Security Alerts
1. Go to GitHub repository
2. Click **"Security"** tab
3. Wait for CodeQL analysis (5-10 minutes)
4. View **"Code scanning alerts"**

### Expected Custom Detections
Your custom CodeQL queries should find:

🚨 **Hardcoded Secrets** (from hardcoded-secrets.ql):
- `API_KEY = "sk-1234567890abcdef1234567890abcdef"`
- `DATABASE_PASSWORD = "MySecretPassword123"`
- `SECRET_TOKEN = "hardcoded-jwt-secret-key"`

🚨 **SQL Injection** (from sql-injection.ql):
- Search function: `f"SELECT * FROM posts WHERE title LIKE '%{query}%'"`
- Login function: `f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"`

## ✅ Step 8: Fix Security Issues

### `app-secure.py` (Fixed Version)
```python
import os
import secrets
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# ✅ Fixed: Use environment variables
API_KEY = os.environ.get('API_KEY', secrets.token_urlsafe(32))
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
SECRET_TOKEN = os.environ.get('JWT_SECRET', secrets.token_hex(32))

@app.route('/')
def home():
    return '''
    <h1>Secure Blog App</h1>
    <form action="/search" method="post">
        <input name="query" placeholder="Search posts">
        <button type="submit">Search</button>
    </form>
    <form action="/login" method="post">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/search', methods=['POST'])
def search_posts():
    query = request.form.get('query')
    
    # ✅ Fixed: Use parameterized queries
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Safe: parameterized query
    cursor.execute("SELECT * FROM posts WHERE title LIKE ?", (f"%{query}%",))
    
    results = cursor.fetchall()
    conn.close()
    
    html = "<h2>Search Results:</h2><ul>"
    for post in results:
        html += f"<li>{post[1]} - {post[2]}</li>"
    html += "</ul>"
    
    return html

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # ✅ Fixed: Use parameterized queries
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Safe: parameterized query
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return f"Welcome {user[1]}!"
    else:
        return "Login failed"

if __name__ == '__main__':
    # Create test database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
                     (id INTEGER, title TEXT, content TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER, username TEXT, password TEXT)''')
    
    cursor.execute("INSERT OR IGNORE INTO posts VALUES (1, 'Hello World', 'First post')")
    cursor.execute("INSERT OR IGNORE INTO posts VALUES (2, 'Python Tips', 'Learn Python')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123')")
    
    conn.commit()
    conn.close()
    
    app.run(host='127.0.0.1', port=5000, debug=False)
```

### Commit Security Fixes
```bash
# Replace vulnerable app with secure version
cp app-secure.py app.py

# Commit fixes
git add app.py
git commit -m "fix: resolve SQL injection and hardcoded secrets

- Use parameterized queries to prevent SQL injection
- Move secrets to environment variables
- Disable debug mode and restrict host"

# Push fixes
git push origin main
```

### Verify Fixes
- Wait for new CodeQL analysis
- Custom queries should no longer detect issues
- Security alerts should be resolved

## 🎓 Lab Complete

### What You Built
✅ **Simple Flask App** - Blog app with search and login (~80 lines)  
✅ **Custom SQL Injection Query** - Detects unsafe SQL execution from Flask requests  
✅ **Custom Hardcoded Secrets Query** - Finds API keys, passwords, and tokens in code  
✅ **Dependabot Integration** - Weekly dependency updates  
✅ **Security Fixes** - Demonstrated parameterized queries and environment variables  

### Custom CodeQL Queries Created
- **SQL Injection Detection**: Tracks Flask user input to SQL execution
- **Hardcoded Secrets Detection**: Finds suspicious string assignments
- **Accurate Results**: Custom queries target specific vulnerabilities in your app

### Key Skills Learned
- Writing custom CodeQL queries for specific security patterns
- Understanding dataflow analysis for SQL injection detection
- Pattern matching for hardcoded secrets detection
- Integrating custom security analysis into CI/CD pipelines
- Fixing real vulnerabilities detected by custom queries

### Architecture Validation ✅
- **Simple App**: Focused Flask application with clear vulnerabilities
- **Custom CodeQL**: SQL injection and hardcoded secrets detection
- **Dependabot**: Automated dependency management
- **Practical Security**: Real vulnerabilities with working fixes

Your custom CodeQL queries successfully detect and help fix security issues in your application!
