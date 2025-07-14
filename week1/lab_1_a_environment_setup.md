# Lab 1A: Environment Setup

## 🎯 Objectives
- GitHub sign up
- GitHub repository creation
- GitHub Codespaces
- GitHub CLI setup
- Azure CLI setup
- GitHub Copilot setup
- Environment verification

## 📋 Prerequisites
- A computer with internet access
- Web browser (Chrome, Firefox, Safari, or Edge)
- Basic understanding of command line interfaces
- Azure account with active subscription

## 🚀 Step-by-Step Instructions

### Step 1: GitHub Sign Up

1. **Navigate to GitHub:**
   - Open your web browser
   - Go to [https://github.com](https://github.com)

2. **Create Account:**
   - Click the **"Sign up"** button in the top-right corner
   - Enter your email address
   - Create a strong password (minimum 8 characters)
   - Choose a unique username
   - Verify you're not a robot (if prompted)
   - Click **"Create account"**

3. **Verify Email:**
   - Check your email inbox for verification email from GitHub
   - Click the verification link in the email
   - Complete any additional setup steps

4. **Choose Plan:**
   - Select the **Free** plan (sufficient for this course)
   - Complete the welcome survey (optional)

### Step 2: GitHub Repository Creation

1. **Create New Repository:**
   - From your GitHub dashboard, click the **"New"** button (green button)
   - Or go to [https://github.com/new](https://github.com/new)

2. **Repository Settings:**
   - **Repository name:** `advanced-software-wil-labs`
   - **Description:** `Lab exercises for Advanced Software WIL course`
   - **Visibility:** Choose **Public** (recommended for learning)
   - **Initialize repository:**
     - ✅ Check "Add a README file"
     - ✅ Check "Add .gitignore" and select **"Node"**
     - ✅ Check "Choose a license" and select **"MIT License"**

3. **Create Repository:**
   - Click **"Create repository"** button
   - Your repository is now created and ready to use

### Step 3: GitHub Codespaces

1. **Access GitHub Codespaces:**
   - In your newly created repository, click the **"Code"** button
   - Select the **"Codespaces"** tab
   - Click **"Create codespace on main"**
   - Wait for the environment to initialize (this may take 2-3 minutes)

2. **Explore Codespaces Interface:**
   - VS Code interface opens in your browser
   - Terminal is available at the bottom panel
   - File explorer shows your repository contents
   - Extensions panel on the left sidebar

3. **Test Codespaces Functionality:**
   - Open the terminal (Terminal → New Terminal)
   - Navigate through your repository files
   - Create a test file to verify write permissions
   ```bash
   # Test basic functionality
   echo "Hello from Codespaces!" > test.txt
   cat test.txt
   ```

### Step 4: GitHub CLI Setup

1. **Verify GitHub CLI Installation:**
   ```bash
   # Check if GitHub CLI is already installed (should be pre-installed in Codespaces)
   gh --version
   ```

2. **Install GitHub CLI (if needed):**
   ```bash
   # For Ubuntu/Debian systems (Codespaces uses Ubuntu)
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   
   sudo apt update
   sudo apt install gh
   ```

3. **Authenticate GitHub CLI:**
   ```bash
   # Login to GitHub CLI
   gh auth login
   
   # Follow the interactive prompts:
   # 1. Choose "GitHub.com"
   # 2. Choose "HTTPS"
   # 3. Authenticate via web browser
   # 4. Complete the authentication in your browser
   ```

4. **Verify GitHub CLI Authentication:**
   ```bash
   # Check authentication status
   gh auth status
   
   # Test CLI functionality
   gh repo view
   ```

### Step 5: Azure CLI Setup

1. **Check Azure CLI Installation:**
   ```bash
   # Back in your GitHub Codespace terminal
   az --version
   ```

2. **Install Azure CLI (if needed):**
   ```bash
   # Install Azure CLI for Ubuntu/Debian
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

3. **Verify Installation:**
   ```bash
   # Check Azure CLI version
   az --version
   ```

4. **Login to Azure CLI:**
   ```bash
   # Login to Azure (will open browser for authentication)
   az login
   
   # If browser doesn't open automatically, copy the URL and open manually
   # Complete authentication in browser using your Azure credentials
   ```

5. **Verify Azure CLI Authentication:**
   ```bash
   # List your Azure subscriptions
   az account list --output table
   
   # Show current subscription details
   az account show
   ```

### Step 6: GitHub Copilot Setup

1. **Get GitHub Copilot Access:**
   - In your browser, go to [https://github.com/features/copilot](https://github.com/features/copilot)
   - Click **"Start free trial"** or **"Get Copilot"**
   - Choose **Individual** plan
   - Start free trial (if eligible) or purchase subscription

2. **Install Copilot Extension in VS Code:**
   - In your Codespace (VS Code), click the **Extensions** icon (left sidebar)
   - Search for **"GitHub Copilot"**
   - Click **"Install"** on the official GitHub Copilot extension
   - Wait for installation to complete

3. **Authenticate Copilot:**
   - VS Code will prompt you to sign in to GitHub Copilot
   - Click **"Sign in to GitHub"**
   - Complete authentication in browser
   - Return to VS Code and wait for confirmation

4. **Test Copilot Functionality:**
   - Create a new file: `test.py`
   - Type the following comment and wait for suggestions:
   ```python
   # Function to calculate the factorial of a number
   def factorial(n):
       # Copilot should suggest implementation here
   ```
   - Press **Tab** to accept suggestions or **Esc** to dismiss

5. **Verify Copilot Status:**
   - Check the status bar at bottom of VS Code
   - Should show **"Copilot: Ready"** or similar
   - The Copilot icon should be visible and active

### Step 7: Environment Verification

1. **Create Verification Script:**
   ```bash
   # Create a verification script
   cat > verify-environment.sh << 'EOF'
   #!/bin/bash
   echo "========================================"
   echo "  Environment Setup Verification"
   echo "========================================"
   echo
   
   echo "✅ System Information:"
   echo "   OS: $(lsb_release -d | cut -f2)"
   echo "   User: $(whoami)"
   echo
   
   echo "✅ Development Tools:"
   echo "   Node.js: $(node --version 2>/dev/null || echo 'Not installed')"
   echo "   Python: $(python3 --version 2>/dev/null || echo 'Not installed')"
   echo "   Git: $(git --version 2>/dev/null || echo 'Not installed')"
   echo "   Docker: $(docker --version 2>/dev/null || echo 'Not installed')"
   echo
   
   echo "✅ GitHub Tools:"
   echo "   GitHub CLI: $(gh --version 2>/dev/null | head -1 || echo 'Not installed')"
   echo "   GitHub Auth: $(gh auth status 2>/dev/null && echo 'Authenticated' || echo 'Not authenticated')"
   echo
   
   echo "✅ Azure Tools:"
   echo "   Azure CLI: $(az --version 2>/dev/null | head -1 || echo 'Not installed')"
   echo "   Azure Auth: $(az account show --query 'user.name' -o tsv 2>/dev/null || echo 'Not authenticated')"
   echo
   
   echo "✅ VS Code Extensions:"
   echo "   GitHub Copilot: $(code --list-extensions 2>/dev/null | grep -q 'github.copilot' && echo 'Installed' || echo 'Not installed')"
   echo
   
   echo "========================================"
   echo "  Verification Complete"
   echo "========================================"
   EOF
   
   # Make script executable
   chmod +x verify-environment.sh
   ```

2. **Run Verification Script:**
   ```bash
   # Execute the verification script
   ./verify-environment.sh
   ```

3. **Manual Verification Checklist:**
   
   **GitHub Account & Repository:**
   - [ ] GitHub account created successfully
   - [ ] Repository `advanced-software-wil-labs` created
   - [ ] Can access repository via web browser
   
   **GitHub Codespaces:**
   - [ ] Codespace launches successfully
   - [ ] VS Code interface loads properly
   - [ ] Terminal access is working
   - [ ] Can create and edit files
   
   **GitHub CLI:**
   - [ ] GitHub CLI installed and working
   - [ ] Successfully authenticated with GitHub
   - [ ] Can run `gh repo view` without errors
   
   **Azure Account:**
   - [ ] Azure account created successfully
   - [ ] Can access Azure Portal at portal.azure.com
   - [ ] Free subscription is active
   
   **Azure CLI:**
   - [ ] Azure CLI installed and working
   - [ ] Successfully authenticated with Azure
   - [ ] Can list Azure subscriptions
   
   **GitHub Copilot:**
   - [ ] Copilot subscription active
   - [ ] Extension installed in VS Code
   - [ ] Copilot status shows "Ready"
   - [ ] Copilot provides code suggestions

## 🔧 Troubleshooting

### Common Issues and Solutions:

**GitHub CLI Authentication Issues:**
```bash
# Clear existing auth and retry
gh auth logout
gh auth login
```

**Azure CLI Login Problems:**
```bash
# Use device code flow if browser doesn't work
az login --use-device-code
```

**Copilot Not Working:**
- Check VS Code status bar for Copilot status
- Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
- Reinstall Copilot extension if needed

**Codespace Issues:**
- Try creating a new Codespace if current one has problems
- Check GitHub status page for service issues

## 🎉 Next Steps

With your environment fully set up, you're ready to proceed to:
- [Lab 1B: GitHub Practices](lab_1_b_github_practices.md)

## 📚 Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Azure CLI Documentation](https://docs.microsoft.com/cli/azure/)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [VS Code Documentation](https://code.visualstudio.com/docs)

## 💡 Tips for Success

1. **Save Your Credentials:** Store your GitHub and Azure login information securely
2. **Bookmark Important URLs:** Keep Azure Portal and GitHub dashboard bookmarked
3. **Practice CLI Commands:** Regular use of CLI tools will improve your efficiency
4. **Explore Copilot:** Experiment with different prompts to understand Copilot capabilities
5. **Keep Codespace Active:** Use your Codespace regularly to maintain familiarity

---

**🏁 Completion:** Once all verification steps pass, you have successfully set up your development environment for the Advanced Software WIL course!
