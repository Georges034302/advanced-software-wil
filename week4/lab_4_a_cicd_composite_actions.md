# 🧪 Lab 4A: CI/CD Composite Actions
Build a GitHub Composite Action that analyzes text files for vowel frequency, logs contributions, and automatically publishes results to GitHub Pages using Node.js and Bash scripts.

## 🎯 Objective
- Analyze text files for vowel frequency using Node.js
- Convert analysis results to JSON format for processing
- Log contributor activities and timestamps using Bash
- Generate dynamic HTML reports with automated updates
- Deploy results to GitHub Pages via CI/CD automation

## 🛠️ Tech Stack
- Node.js (v18+)
- Bash
- GitHub Actions
- Git CLI
- GitHub Pages

---

## 🚀 Setup Instructions

### Step 1: Create Repository Structure
```bash
# Create new repository
mkdir vowel-analyzer-web
cd vowel-analyzer-web

# Create folder structure
mkdir -p .github/actions/analyzer/scripts
mkdir -p .github/workflows

# Create data file
cat > data.txt << 'EOF'
Hello GitHub Actions and Copilot!
This is our sample data file for vowel analysis.
We will count vowels and create a web report.
Automation makes development efficient and reliable.
EOF
```

### 📁 Folder Structure

```
root/
├── data.txt
├── README.md
├── changelog.md
├── index.html
├── render.js
├── .github/
│   ├── workflows/
│   │   └── analyze.yml
│   └── actions/
│       └── analyzer/
│           ├── action.yml
│           └── scripts/
│               ├── analyzer.js
│               ├── parser.js
│               ├── logger.sh
│               └── updateHTML.sh
```

---

### Step 2: 💻 Script Implementations

### 📝 `analyzer.js`

```javascript
const fs = require('fs');

/**
 * Analyzes text file for vowel frequency
 * Usage: node analyzer.js <input-file>
 */

function countVowels(text) {
    const vowels = 'aeiouAEIOU';
    const counts = { a: 0, e: 0, i: 0, o: 0, u: 0, total: 0 };
    
    for (const char of text) {
        const lowerChar = char.toLowerCase();
        if (vowels.includes(char)) {
            counts[lowerChar] = (counts[lowerChar] || 0) + 1;
            counts.total++;
        }
    }
    
    return counts;
}

function analyzeFile(inputFile) {
    try {
        console.log(`🔍 Analyzing file: ${inputFile}`);
        
        if (!fs.existsSync(inputFile)) {
            throw new Error(`File not found: ${inputFile}`);
        }
        
        const content = fs.readFileSync(inputFile, 'utf8');
        const vowelCounts = countVowels(content);
        const wordCount = content.trim().split(/\s+/).length;
        const charCount = content.length;
        
        const analysis = {
            file: inputFile,
            timestamp: new Date().toISOString(),
            vowel_counts: vowelCounts,
            total_vowels: vowelCounts.total,
            word_count: wordCount,
            character_count: charCount
        };
        
        fs.writeFileSync('analysis.json', JSON.stringify(analysis, null, 2));
        console.log(`✅ Analysis complete! Found ${vowelCounts.total} vowels in ${wordCount} words`);
        
        return analysis;
        
    } catch (error) {
        console.error('❌ Error analyzing file:', error.message);
        process.exit(1);
    }
}

// Main execution
if (require.main === module) {
    const inputFile = process.argv[2] || 'data.txt';
    analyzeFile(inputFile);
}

module.exports = { countVowels, analyzeFile };
```

### 🔄 `parser.js`

```javascript
const fs = require('fs');

/**
 * Parses analysis JSON and creates result format for HTML
 * Usage: node parser.js [analysis-file]
 */

function parseAnalysis(analysisFile = 'analysis.json') {
    try {
        console.log(`📋 Parsing analysis: ${analysisFile}`);
        
        if (!fs.existsSync(analysisFile)) {
            throw new Error(`Analysis file not found: ${analysisFile}`);
        }
        
        const analysis = JSON.parse(fs.readFileSync(analysisFile, 'utf8'));
        
        // Create result format optimized for HTML display
        const result = {
            processed_at: new Date().toISOString(),
            source_file: analysis.file,
            vowel_counts: analysis.vowel_counts,
            total_vowels: analysis.total_vowels,
            word_count: analysis.word_count,
            character_count: analysis.character_count,
            metrics: {
                vowels_per_word: Math.round((analysis.total_vowels / analysis.word_count) * 100) / 100,
                vowel_density: Math.round((analysis.total_vowels / analysis.character_count) * 100 * 100) / 100 + '%'
            }
        };
        
        fs.writeFileSync('result.json', JSON.stringify(result, null, 2));
        console.log(`✅ Result created: result.json`);
        console.log(`📊 Metrics: ${result.metrics.vowels_per_word} vowels/word, ${result.metrics.vowel_density} density`);
        
        return result;
        
    } catch (error) {
        console.error('❌ Error parsing analysis:', error.message);
        process.exit(1);
    }
}

// Main execution
if (require.main === module) {
    const analysisFile = process.argv[2] || 'analysis.json';
    parseAnalysis(analysisFile);
}

module.exports = { parseAnalysis };
```

### 📝 `logger.sh`

```bash
#!/bin/bash
set -e

# logger.sh - Logs analysis activities to changelog.md
# Usage: ./logger.sh [username]

USERNAME="${1:-unknown}"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
CHANGELOG_FILE="changelog.md"

echo "📝 Logging analysis by: $USERNAME"
echo "⏰ Timestamp: $TIMESTAMP"

# Create changelog if it doesn't exist
if [[ ! -f "$CHANGELOG_FILE" ]]; then
    cat > "$CHANGELOG_FILE" << 'EOF'
# Vowel Analysis Changelog

This file tracks all vowel analysis activities.

---

EOF
fi

# Extract data from result.json if available
TOTAL_VOWELS="N/A"
WORD_COUNT="N/A"
VOWEL_DENSITY="N/A"

if [[ -f "result.json" ]]; then
    if command -v jq >/dev/null 2>&1; then
        TOTAL_VOWELS=$(jq -r '.total_vowels // "N/A"' result.json 2>/dev/null)
        WORD_COUNT=$(jq -r '.word_count // "N/A"' result.json 2>/dev/null)
        VOWEL_DENSITY=$(jq -r '.metrics.vowel_density // "N/A"' result.json 2>/dev/null)
    fi
fi

# Create log entry
LOG_ENTRY="
## 📊 Analysis - $(date -u +"%Y-%m-%d")

**Contributor**: @$USERNAME  
**Timestamp**: $TIMESTAMP  
**Results**:
- 🔤 Total Vowels: $TOTAL_VOWELS
- 📝 Word Count: $WORD_COUNT
- 📊 Vowel Density: $VOWEL_DENSITY

---
"

# Add entry to changelog
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/^---$/a\
'"$LOG_ENTRY"'
' "$CHANGELOG_FILE"
else
    sed -i '/^---$/a\'"$LOG_ENTRY" "$CHANGELOG_FILE"
fi

echo "✅ Changelog updated: $CHANGELOG_FILE"
echo "👤 Logged contribution by: $USERNAME"
```

---

### 🔧 `updateHTML.sh`

```bash
#!/bin/bash
set -e

# Check if result.json exists
if [[ ! -f "result.json" ]]; then
    echo "❌ Error: result.json not found!"
    exit 1
fi

# Read JSON and validate it
json=$(cat result.json)
if ! echo "$json" | jq . >/dev/null 2>&1; then
    echo "❌ Error: Invalid JSON in result.json"
    exit 1
fi

# Update render.js with the JSON result
cat > render.js << EOF
// This file is auto-updated by updateHTML.sh
// Generated on: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

const result = $json;

window.onload = () => {
  const output = document.getElementById("output");
  if (!result || Object.keys(result).length === 0) {
    output.innerHTML = "<p>No data available.</p>";
    return;
  }
  
  // Create a nice display of vowel frequencies
  let html = "<h3>📊 Vowel Frequency Analysis</h3>";
  html += "<div class='stats'>";
  
  if (result.vowel_counts) {
    html += "<h4>Vowel Breakdown:</h4><ul>";
    Object.entries(result.vowel_counts).forEach(([vowel, count]) => {
      if (vowel !== 'total') {
        html += \`<li><strong>\${vowel.toUpperCase()}:</strong> \${count}</li>\`;
      }
    });
    html += "</ul>";
    
    html += \`<p><strong>Total Vowels:</strong> \${result.total_vowels || result.vowel_counts.total}</p>\`;
    html += \`<p><strong>Total Words:</strong> \${result.word_count}</p>\`;
  } else {
    html += "<ul>";
    Object.entries(result).forEach(([k, v]) => {
      html += \`<li><strong>\${k}:</strong> \${v}</li>\`;
    });
    html += "</ul>";
  }
  
  html += "</div>";
  html += \`<p class='timestamp'>Last updated: \${new Date().toLocaleString()}</p>\`;
  
  output.innerHTML = html;
};
EOF

echo "✅ Updated render.js with JSON result"
echo "📊 Analysis data loaded successfully"
```

---

### 🌐 `index.html` - Web Page

```html
<!DOCTYPE html>
<html>
<head>
  <title>Vowel Frequency Report</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .container {
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 {
      color: #333;
      text-align: center;
      margin-bottom: 30px;
    }
    .stats {
      background: #f8f9fa;
      padding: 20px;
      border-radius: 5px;
      margin: 20px 0;
    }
    .stats ul {
      list-style: none;
      padding: 0;
    }
    .stats li {
      padding: 5px 0;
      border-bottom: 1px solid #eee;
    }
    .timestamp {
      color: #666;
      font-size: 0.9em;
      text-align: center;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>📊 Vowel Analysis Report</h1>
    <div id="output">Loading analysis results...</div>
  </div>
  <script src="render.js"></script>
</body>
</html>
```

---

### 🧩 `action.yml` - Composite Action

```yaml
name: "Node.js File Analyzer with HTML Output"
description: "Counts vowels, logs contributor, and updates HTML report"
inputs:
  file:
    description: 'Path to the data file to analyze'
    required: true
  user:
    description: 'GitHub username for logging'
    required: true

runs:
  using: "composite"
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    
    - name: Run Analyzer
      shell: bash
      run: node .github/actions/analyzer/scripts/analyzer.js ${{ inputs.file }}
    
    - name: Parse Results
      shell: bash
      run: node .github/actions/analyzer/scripts/parser.js
    
    - name: Log Activity
      shell: bash
      run: bash .github/actions/analyzer/scripts/logger.sh "${{ inputs.user }}"
    
    - name: Update HTML
      shell: bash
      run: bash .github/actions/analyzer/scripts/updateHTML.sh
```

---

### 🔧 `analyze.yml` - Workflow

```yaml
name: Vowel File Analysis and Web Report

on:
  push:
    paths:
      - data.txt

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Needed for GitHub Pages deployment
      pages: write     # Needed for GitHub Pages deployment
      id-token: write  # Needed for GitHub Pages deployment
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Run Vowel Analyzer
        uses: ./.github/actions/analyzer
        with:
          file: data.txt
          user: ${{ github.actor }}
      
      - name: Commit Updated Files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add render.js changelog.md
          if ! git diff --cached --quiet; then
            git commit -m "📊 Update analysis results - by @${{ github.actor }}"
            git push
          fi

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
          publish_branch: gh-pages
```

---

## Step 3: 🧪 Testing & Deployment

### Local Testing
```bash
# Make scripts executable
chmod +x .github/actions/analyzer/scripts/*.sh

# Test locally
cd .github/actions/analyzer/scripts
node analyzer.js ../../../../data.txt
node parser.js
bash logger.sh "test-user"
bash updateHTML.sh

# Check generated files
ls -la ../../../../*.json ../../../../render.js
```

### GitHub Deployment
```bash
# Initialize repository
git init
git add .
git commit -m "🎉 Initial commit: Vowel analyzer with web output"

# Create GitHub repository
gh repo create vowel-analyzer-web --public
git remote add origin https://github.com/YOUR_USERNAME/vowel-analyzer-web.git
git push -u origin main

# Enable GitHub Pages
gh api repos/:owner/:repo --method PATCH --field has_pages=true
```

### Trigger Analysis
```bash
# Update data.txt to trigger workflow
echo "Additional test content for vowel analysis!" >> data.txt
git add data.txt
git commit -m "📝 Update data - trigger analysis"
git push
```

---

## ✅ Expected Output
- `result.json`: JSON-formatted analysis
- `changelog.md`: Contributor + timestamp log
- `render.js`: JavaScript-rendered result
- `index.html`: Live vowel report
- Published via GitHub Pages

---

## 🎓 Learning Outcomes

By completing this lab, students will have learned:

### Technical Skills
- **Node.js**: File processing, JSON manipulation, error handling
- **Bash Scripting**: Text processing, conditional logic, file operations
- **GitHub Actions**: Composite actions, workflow triggers, permissions
- **Web Development**: HTML, CSS, JavaScript, dynamic content generation
- **Git Operations**: Automated commits, branch management, CI/CD integration

### Professional Concepts
- **CI/CD Pipeline Design**: Chaining multiple processing steps
- **Automation Patterns**: File-triggered workflows, automated reporting
- **Web Deployment**: GitHub Pages, static site generation
- **Code Organization**: Modular scripts, reusable actions
- **Documentation**: Technical writing, README creation

---