# Lab 1A: Environment Setup

## 🎯 Objectives
- Set up GitHub Codespaces development environment
- Install and configure Azure CLI
- Install and configure GitHub Copilot
- Verify all tools are working correctly

## 📋 Prerequisites
- GitHub account with access to Codespaces
- GitHub Copilot subscription (or trial)
- Basic understanding of command line interfaces

## 🚀 Getting Started

### Step 1: Launch GitHub Codespaces

1. Navigate to your repository on GitHub
2. Click the **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**
5. Wait for the environment to initialize

### Step 2: Verify Base Environment

Once your Codespace is ready, open a terminal and verify the basic tools:

```bash
# Check Node.js
node --version

# Check Python
python --version

# Check Git
git --version

# Check Docker
docker --version
```

### Step 3: Install Azure CLI

The Azure CLI might already be installed in your Codespace. Let's check and install if needed:

```bash
# Check if Azure CLI is installed
az --version

# If not installed, install it
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Verify the installation:
```bash
az --version
```

### Step 4: Login to Azure CLI

```bash
# Login to Azure (this will open a browser for authentication)
az login

# Verify login and list subscriptions
az account list --output table
```

### Step 5: Configure GitHub Copilot

1. Ensure GitHub Copilot extension is installed in VS Code
2. Sign in to GitHub Copilot when prompted
3. Test Copilot functionality:
   - Create a new file called `test.py`
   - Start typing a comment like `# Function to calculate fibonacci`
   - Observe Copilot suggestions

### Step 6: Test Copilot Code Generation

Create a simple test to verify Copilot is working:

```python
# Create a function that calculates the factorial of a number
def factorial(n):
    # Let Copilot complete this function
```

### Step 7: Environment Verification Checklist

Create a verification script to ensure everything is working:

```bash
#!/bin/bash
echo "=== Environment Setup Verification ==="
echo "Node.js: $(node --version)"
echo "Python: $(python --version)"
echo "Git: $(git --version)"
echo "Docker: $(docker --version)"
echo "Azure CLI: $(az --version | head -1)"
echo "GitHub CLI: $(gh --version | head -1)"
echo "=== Verification Complete ==="
```

## 🔍 Validation

Your environment is ready when:
- [ ] Codespace launches successfully
- [ ] All basic tools are available and working
- [ ] Azure CLI is installed and authenticated
- [ ] GitHub Copilot is active and providing suggestions
- [ ] You can create and edit files in VS Code
- [ ] Terminal commands execute properly

## 🎉 Next Steps

With your environment set up, you're ready to proceed to:
- [Lab 1B: GitHub Practices](lab_1_b_github_practices.md)

## 📚 Additional Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

---

**Note:** Keep your Codespace running as you'll use it for the remaining labs in this week.
