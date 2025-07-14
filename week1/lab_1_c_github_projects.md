# Lab 1C: GitHub Projects

## 🎯 Objectives
- Create project
- Board selection 
- Project workflow 
- Create project README (markdown essentials)
- GitHub Pages setup and integration

## 📋 Prerequisites
- Completed [Lab 1B: GitHub Practices](lab_1_b_github_practices.md)
- GitHub account with repository access
- Understanding of Markdown syntax
- Basic project management concepts

## 🚀 Step-by-Step Instructions

### Step 1: Create Project

1. **Navigate to Projects:**
   - Go to your GitHub repository
   - Click on the **Projects** tab
   - Click **New project**

2. **Choose Project Template:**
   - Select **Team backlog** template
   - Give your project a name: "Advanced Software WIL Project"
   - Add a description: "Project management for Advanced Software WIL course"
   - Set visibility to **Public** (for learning purposes)

3. **Create the Project:**
   - Click **Create project**
   - Your new project board will open

### Step 2: Board Selection 

1. **Explore Default Views:**
   - **Table View:** Spreadsheet-like view for detailed information
   - **Board View:** Kanban-style board for visual workflow
   - **Roadmap View:** Timeline view for planning

2. **Configure Board Features:**
   
   **Add Custom Fields:**
   - Click the **+** next to field headers
   - Add these fields:
     ```
     Priority: Single select (High, Medium, Low, Critical)
     Story Points: Number
     Sprint: Text
     Feature Area: Single select (Frontend, Backend, DevOps, Documentation)
     ```

3. **Set Up Board Columns:**
   - **Backlog** - New items waiting to be prioritized
   - **Ready** - Items ready for development
   - **In Progress** - Currently being worked on
   - **Review** - In code review or testing
   - **Done** - Completed items

### Step 3: Project Workflow 

#### Creating Issues

1. **Create Sample Issues:**
   ```markdown
   Issue 1: Create project homepage
   - Description: Design and implement main landing page (index.html)
   - Labels: frontend, homepage
   - Priority: High
   - Feature Area: Frontend
   
   Issue 2: Write project documentation
   - Description: Create comprehensive README.md file
   - Labels: documentation
   - Priority: Medium
   - Feature Area: Documentation
   
   Issue 3: Set up GitHub Pages
   - Description: Deploy homepage to GitHub Pages
   - Labels: deployment, pages
   - Priority: Low
   - Feature Area: DevOps
   ```

2. **Add Issues to Project:**
   - Go to your repository **Issues** tab
   - Click **New issue**
   - Fill in title and description
   - Add labels and assign to project
   - Repeat for all sample issues

#### Assigning and Movement

1. **Assign Issues:**
   - In the project board, click on an issue
   - Set **Assignees** (assign to yourself for practice)
   - Set **Priority** using custom field
   - Set **Feature Area**

2. **Practice Manual Movement:**
   - Drag issues between columns
   - Move Issue 1 to "In Progress"
   - Move Issue 2 to "Ready"
   - Leave Issue 3 in "Backlog"

#### Automated Movement on PR

1. **Set Up Automation Rules:**
   - In your project, click the **⚙️** (Settings)
   - Go to **Workflows**
   - Click **Add workflow**

2. **Configure PR Automation:**
   ```markdown
   Workflow 1: Move to "In Progress" when PR is opened
   - Trigger: Pull request opened
   - Action: Set status to "In Progress"
   
   Workflow 2: Move to "Review" when PR is ready for review
   - Trigger: Pull request marked ready for review
   - Action: Set status to "Review"
   
   Workflow 3: Move to "Done" when PR is merged
   - Trigger: Pull request merged
   - Action: Set status to "Done"
   ```

3. **Test the Workflow:**
   - Create a new branch: `git checkout -b feature/test-workflow`
   - Make a small change to README
   - Commit and push: `git push origin feature/test-workflow`
   - Create a PR and observe project board changes

### Step 4: Create Project README (Markdown Essentials)

1. **Create Comprehensive README:**
   ```markdown
   # Advanced Software WIL Project
   
   ![Project Banner](https://via.placeholder.com/800x200/0366d6/ffffff?text=Advanced+Software+WIL)
   
   ## 📋 Project Overview
   
   This project demonstrates GitHub project management and web development fundamentals including:
   - GitHub Projects and workflow management
   - Professional README documentation
   - GitHub Pages deployment
   - Basic web development with HTML/CSS
   
   ## 🚀 Features
   
   - **Project Management:** GitHub Projects with automated workflows
   - **Documentation:** Comprehensive README with markdown essentials
   - **Web Presence:** Professional homepage with GitHub Pages
   - **Version Control:** Git workflows and collaboration practices
   
   ## 🛠 Technology Stack
   
   | Technology | Purpose |
   |------------|---------|
   | HTML | Web structure |
   | CSS | Styling and design |
   | GitHub Projects | Project management |
   | GitHub Pages | Web hosting |
   | Markdown | Documentation |
   
   ## 📁 Project Structure
   
   ```bash
   advanced-software-wil/
   ├── index.html         # Main homepage
   └── README.md          # Project documentation
   ```
   
   ### Quick Start
   
   1. **Clone the repository:**
      ```bash
      git clone https://github.com/your-username/advanced-software-wil.git
      cd advanced-software-wil
      ```
   
   2. **Open index.html:**
      - Open `index.html` in your web browser
      - Or visit the live site on GitHub Pages
   
   3. **Access the live site:**
      - Homepage: https://your-username.github.io/advanced-software-wil
   
   ## 📊 Project Status
   
   ![GitHub issues](https://img.shields.io/github/issues/your-username/advanced-software-wil)
   ![GitHub pull requests](https://img.shields.io/github/issues-pr/your-username/advanced-software-wil)
   ![GitHub Pages](https://img.shields.io/github/deployments/your-username/advanced-software-wil/github-pages)
   
   ## 🤝 Contributing
   
   1. Fork the repository
   2. Create a feature branch (`git checkout -b feature/amazing-feature`)
   3. Commit your changes (`git commit -m 'Add amazing feature'`)
   4. Push to branch (`git push origin feature/amazing-feature`)
   5. Open a Pull Request
   
   ## 👥 Team
   
   | Name | Role | GitHub |
   |------|------|--------|
   | Student Name | Developer | [@username](https://github.com/username) |
   
   ## 🌐 Live Demo
   
   [![Visit Live Site](https://img.shields.io/badge/Visit-Live%20Site-blue?style=for-the-badge)](https://your-username.github.io/your-repo-name)
   
   [🏠 **Visit Our Homepage**](https://your-username.github.io/your-repo-name)
   
   ## 📄 License
   
   This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
   ```

2. **Markdown Essentials Used:**
   - **Headers:** `#`, `##`, `###`
   - **Emphasis:** `**bold**`, `*italic*`
   - **Links:** `[text](url)`
   - **Images:** `![alt](url)`
   - **Code blocks:** Triple backticks
   - **Tables:** Pipe syntax
   - **Lists:** `-` and numbered
   - **Badges:** Shield.io integration
   - **Blockquotes:** `>`

### Step 5: GitHub Pages Setup and Integration

This step covers creating index.html, deploying to GitHub Pages, adding homepage links to README with clickable images, and integrating everything together.

#### Create index.html

1. **Create index.html in repository root:**
   ```bash
   # Create index.html in the main repository directory
   touch index.html
   ```

2. **Create index.html content:**
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Hello From GitHub Pages</title>
   </head>
   <body>
       <h1>Hello From GitHub Pages</h1>
   </body>
   </html>
   ```

#### Deploy to GitHub Pages

1. **Enable GitHub Pages:**
   - Go to repository **Settings**
   - Scroll to **Pages** section
   - Under **Source**, select **Deploy from a branch**
   - Choose **main** branch and **/ (root)** folder
   - Click **Save**

2. **Wait for Deployment:**
   - GitHub will build and deploy your site
   - You'll get a URL like: `https://your-username.github.io/repository-name`

3. **Test Your Site:**
   - Visit the generated URL
   - Verify that your index.html loads correctly

#### Integrate Homepage with README

1. **Add Homepage Link and Clickable Images to README:**
   ```markdown
   # Advanced Software WIL Project
   
   ![Project Banner](https://via.placeholder.com/800x200/0366d6/ffffff?text=Advanced+Software+WIL)
   
   ## 🌐 Live Demo
   
   [![Visit Live Site](https://via.placeholder.com/400x200/0366d6/ffffff?text=Click+to+Visit)](https://your-username.github.io/your-repo-name)
   
   **[🏠 Visit Our Homepage](https://your-username.github.io/your-repo-name)**
   
   ## 📋 Project Overview
   <!-- Rest of your README content -->
   ```

2. **Create Multiple Clickable Images in README:**
   ```markdown
   ## 🖼️ Project Gallery
   
   <!-- Main project dashboard - clickable -->
   [![Project Dashboard](https://via.placeholder.com/600x300/667eea/ffffff?text=Click+to+Visit+Site)](https://your-username.github.io/your-repo-name)
   
   <!-- Homepage preview - clickable -->
   [![Homepage Preview](https://via.placeholder.com/600x300/764ba2/ffffff?text=Homepage+Preview)](https://your-username.github.io/your-repo-name)
   
   <!-- Project board link - clickable -->
   [![Project Board](https://via.placeholder.com/600x300/28a745/ffffff?text=View+Project+Board)](https://github.com/your-username/your-repo-name/projects)
   ```

3. **Add Interactive Elements Section:**
   ```markdown
   ## 🔗 Quick Access Links
   
   | Resource | Link | Description |
   |----------|------|-------------|
   | 🏠 Homepage | [Visit Site](https://your-username.github.io/your-repo-name) | Live project homepage |
   | 📋 Project Board | [View Board](https://github.com/your-username/your-repo-name/projects) | Project management |
   | 📁 Repository | [View Code](https://github.com/your-username/your-repo-name) | Source code |
   | 📄 Documentation | [Read Docs](README.md) | Project documentation |
   ```

4. **Embed Live Site in README:**
   
   You can embed your live GitHub Pages site directly into your README using HTML iframe or by creating preview links:

   **Option 1: Create a Preview Section in README:**
   ```markdown
   ## 🌐 Live Site Preview
   
   [![Live Site](https://img.shields.io/badge/🌐_Live_Site-Visit_Now-blue?style=for-the-badge)](https://your-username.github.io/your-repo-name)
   
   **Quick Access:** [https://your-username.github.io/your-repo-name](https://your-username.github.io/your-repo-name)
   
   ### Site Features:
   - Simple "Hello From GitHub Pages" message
   - Deployed automatically from main branch
   - Accessible worldwide via GitHub Pages
   ```

   **Option 2: Add Site Status to Project Overview:**
   ```markdown
   ## 📊 Project Status & Links
   
   | Component | Status | Link |
   |-----------|--------|------|
   | 🌐 Live Site | [![Deployed](https://img.shields.io/badge/Status-Live-green)](https://your-username.github.io/your-repo-name) | [Visit Site](https://your-username.github.io/your-repo-name) |
   | 📋 Project Board | [![Active](https://img.shields.io/badge/Status-Active-blue)](https://github.com/your-username/your-repo-name/projects) | [View Board](https://github.com/your-username/your-repo-name/projects) |
   | 📁 Repository | [![Public](https://img.shields.io/badge/Status-Public-brightgreen)](https://github.com/your-username/your-repo-name) | [View Code](https://github.com/your-username/your-repo-name) |
   ```

   **Option 3: Create Quick Links Section:**
   ```markdown
   ## 🚀 Quick Links
   
   - 🏠 **Homepage:** [your-username.github.io/your-repo-name](https://your-username.github.io/your-repo-name)
   - 📋 **Project Board:** [GitHub Projects](https://github.com/your-username/your-repo-name/projects)
   - 📁 **Source Code:** [Repository](https://github.com/your-username/your-repo-name)
   - 📄 **Documentation:** [README.md](README.md)
   ```

## 🔍 Validation Checklist

Your GitHub project setup is complete when:

**Project Creation:**
- [ ] GitHub Project created with proper name and description
- [ ] Project visibility set appropriately
- [ ] Project linked to repository

**Board Configuration:**
- [ ] Custom fields added (Priority, Story Points, Sprint, Feature Area)
- [ ] Board columns configured (Backlog, Ready, In Progress, Review, Done)
- [ ] Multiple views available (Table, Board, Roadmap)

**Workflow Implementation:**
- [ ] Sample issues created and added to project
- [ ] Issues properly assigned and labeled
- [ ] Manual movement between columns works
- [ ] Automation rules configured for PR workflow
- [ ] Automation tested with sample PR

**README Creation:**
- [ ] README.md created with all markdown essentials
- [ ] Project overview and features documented
- [ ] Technology stack table included
- [ ] Simple getting started instructions provided
- [ ] Team information added
- [ ] Badges and status indicators included

**GitHub Pages Setup:**
- [ ] index.html created with professional design in repository root
- [ ] GitHub Pages enabled and deployed from main branch / (root)
- [ ] Homepage accessible via generated URL
- [ ] Clickable images implemented in both index.html and README
- [ ] Homepage link added to README with title and clickable image

## 🎯 Practice Exercises

1. **Advanced Project Management:**
   - Create a sprint planning session
   - Practice moving issues through the workflow
   - Set up milestone tracking

2. **README Enhancement:**
   - Add more badges and shields
   - Include code examples
   - Add troubleshooting section

3. **Pages Customization:**
   - Enhance the CSS styling
   - Add more interactive elements
   - Include project screenshots

## 🎉 Next Steps

With your project infrastructure ready, proceed to:
- [Lab 1D: Copilot Onboarding](lab_1_d_copilot_onboarding.md)

## 📚 Additional Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)
- [HTML/CSS Basics](https://developer.mozilla.org/en-US/docs/Web/HTML)

---

**Pro Tip:** Keep your project board updated regularly and use automation to streamline your workflow!
