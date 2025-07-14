# Lab 1C: GitHub Projects

## 🎯 Objectives
- Create and configure a GitHub Project for team collaboration
- Set up GitHub Pages for project documentation
- Design a comprehensive custom README
- Implement project management workflows
- Configure team collaboration settings

## 📋 Prerequisites
- Completed [Lab 1B: GitHub Practices](lab_1_b_github_practices.md)
- GitHub account with repository access
- Understanding of Markdown syntax
- Basic project management concepts

## 🚀 Creating GitHub Projects

### Step 1: Setting Up a New GitHub Project

1. **Navigate to Projects:**
   - Go to your GitHub repository
   - Click on the **Projects** tab
   - Click **New project**

2. **Choose Project Template:**
   - Select **Team backlog** or **Basic kanban**
   - Give your project a descriptive name: "Advanced Software WIL - Team Project"
   - Add a description: "Collaborative project for Advanced Software WIL course"

3. **Configure Project Settings:**
   - Set visibility (Private for team projects)
   - Add team members
   - Configure access permissions

### Step 2: Customizing Project Views

#### Creating Custom Views

1. **Sprint Planning View:**
   ```markdown
   View Name: Sprint Planning
   Group by: Status
   Filter: Iteration
   Sort: Priority (High to Low)
   ```

2. **Team Board View:**
   ```markdown
   View Name: Team Kanban
   Group by: Assignee
   Filter: Current Sprint
   Sort: Created Date
   ```

3. **Roadmap View:**
   ```markdown
   View Name: Project Roadmap
   Layout: Roadmap
   Group by: Epic/Feature
   Date field: Target Date
   ```

#### Setting Up Custom Fields

Add these custom fields to enhance project tracking:

```markdown
Custom Fields:
- Priority: Single Select (High, Medium, Low, Critical)
- Story Points: Number (1, 2, 3, 5, 8, 13)
- Epic: Single Select (Authentication, Dashboard, API, Testing)
- Sprint: Iteration field
- Reviewer: People field
- Definition of Done: Checkbox
```

### Step 3: Project Workflow Implementation

#### Creating Issue Templates

Navigate to your repository settings and create issue templates:

**1. Feature Request Template:**
```markdown
---
name: Feature Request
about: Propose a new feature for the project
title: '[FEATURE] '
labels: ['enhancement', 'needs-triage']
assignees: ''
---

## Feature Description
<!-- Describe the feature you'd like to see -->

## User Story
As a [type of user], I want [some goal] so that [some reason].

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Additional Context
<!-- Add any other context, screenshots, or examples -->

## Definition of Done
- [ ] Code complete and reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to staging environment
```

**2. Bug Report Template:**
```markdown
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''
---

## Bug Description
<!-- A clear description of what the bug is -->

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
<!-- What you expected to happen -->

## Actual Behavior
<!-- What actually happened -->

## Environment
- OS: [e.g. Windows 10, macOS, Ubuntu]
- Browser: [e.g. Chrome, Firefox, Safari]
- Version: [e.g. 1.0.0]

## Additional Context
<!-- Screenshots, logs, or other relevant information -->
```

#### Setting Up Project Automation

Configure automation rules for your project:

1. **Auto-assign Issues:**
   ```yaml
   When: Issue created
   Then: Add to project
   And: Set status to "Triage"
   ```

2. **Move to In Progress:**
   ```yaml
   When: Pull request opened
   Then: Set status to "In Progress"
   And: Link to related issue
   ```

3. **Move to Done:**
   ```yaml
   When: Pull request merged
   Then: Set status to "Done"
   And: Close linked issues
   ```

### Step 4: Setting Up GitHub Pages

#### Basic Pages Setup

1. **Enable GitHub Pages:**
   - Go to repository **Settings**
   - Scroll to **Pages** section
   - Select source: **Deploy from a branch**
   - Choose branch: **main** and folder: **/ (root)**

2. **Create Basic Documentation Structure:**
   ```bash
   # Create docs directory
   mkdir docs
   cd docs
   
   # Create index page
   cat > index.md << 'EOF'
   # Advanced Software WIL Project
   
   Welcome to our team project documentation.
   
   ## Navigation
   - [Project Overview](overview.md)
   - [Getting Started](getting-started.md)
   - [API Documentation](api.md)
   - [Team Information](team.md)
   EOF
   ```

3. **Configure _config.yml:**
   ```yaml
   # docs/_config.yml
   theme: jekyll-theme-minimal
   title: Advanced Software WIL
   description: Team project for Advanced Software course
   
   plugins:
     - jekyll-feed
     - jekyll-sitemap
   
   navbar:
     - title: Home
       url: /
     - title: Documentation
       url: /docs/
     - title: API
       url: /api/
   ```

#### Advanced Pages Configuration

Create a comprehensive documentation site:

**1. Overview Page (docs/overview.md):**
```markdown
# Project Overview

## Mission Statement
Our mission is to develop a comprehensive software solution that demonstrates advanced development practices, DevOps integration, and cloud deployment strategies.

## Architecture
![Architecture Diagram](images/architecture.png)

## Technology Stack
- **Frontend:** React.js with TypeScript
- **Backend:** Node.js with Express
- **Database:** PostgreSQL
- **Cloud:** Azure App Service
- **CI/CD:** GitHub Actions
- **Monitoring:** Azure Application Insights

## Project Timeline
- Week 1-2: Setup and Planning
- Week 3-4: Core Development
- Week 5-6: Integration and Testing
- Week 7-8: Deployment and Documentation
- Week 9-10: Final Polish and Presentation
```

**2. Getting Started Guide (docs/getting-started.md):**
```markdown
# Getting Started

## Prerequisites
- Node.js 18+
- Docker
- Azure CLI
- Git

## Local Development Setup

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/your-org/advanced-software-wil.git
cd advanced-software-wil
\`\`\`

### 2. Install Dependencies
\`\`\`bash
npm install
\`\`\`

### 3. Environment Configuration
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 4. Start Development Server
\`\`\`bash
npm run dev
\`\`\`

## Contributing
Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.
```

### Step 5: Creating a Comprehensive README

Replace your repository's README.md with a professional template:

```markdown
# 🚀 Advanced Software WIL - Team Project

[![Build Status](https://github.com/your-org/advanced-software-wil/workflows/CI/badge.svg)](https://github.com/your-org/advanced-software-wil/actions)
[![Deploy Status](https://github.com/your-org/advanced-software-wil/workflows/Deploy/badge.svg)](https://github.com/your-org/advanced-software-wil/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive software development project demonstrating modern DevOps practices, cloud integration, and collaborative development workflows.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)

## 🎯 Overview

This project serves as a capstone for the Advanced Software WIL course, integrating:
- Modern web development practices
- Cloud-native architecture
- Automated CI/CD pipelines
- Comprehensive testing strategies
- Professional project management

## ✨ Features

- 🔐 **Authentication & Authorization** - Secure user management
- 📊 **Dashboard Analytics** - Real-time data visualization
- 🔄 **API Integration** - RESTful API with OpenAPI documentation
- 🐳 **Containerization** - Docker-based development and deployment
- ☁️ **Cloud Deployment** - Azure App Service integration
- 📈 **Monitoring** - Application performance monitoring
- 🧪 **Testing** - Unit, integration, and E2E testing

## 🛠 Technology Stack

### Frontend
- **Framework:** React 18 with TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Redux Toolkit
- **Testing:** Jest + React Testing Library

### Backend
- **Runtime:** Node.js 18
- **Framework:** Express.js
- **Database:** PostgreSQL with Prisma ORM
- **Authentication:** JWT with refresh tokens
- **Documentation:** Swagger/OpenAPI

### DevOps & Cloud
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud Platform:** Microsoft Azure
- **Monitoring:** Azure Application Insights
- **Infrastructure:** Azure Resource Manager templates

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Docker](https://www.docker.com/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)
- [Git](https://git-scm.com/)

### Quick Start

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/your-org/advanced-software-wil.git
   cd advanced-software-wil
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Set up environment**
   \`\`\`bash
   cp .env.example .env
   # Configure your environment variables
   \`\`\`

4. **Start development environment**
   \`\`\`bash
   docker-compose up -d
   npm run dev
   \`\`\`

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📁 Project Structure

\`\`\`
advanced-software-wil/
├── apps/
│   ├── frontend/          # React frontend application
│   └── backend/           # Node.js backend API
├── packages/
│   ├── shared/            # Shared utilities and types
│   └── ui/                # Shared UI components
├── infrastructure/
│   ├── docker/            # Docker configurations
│   └── azure/             # Azure Resource Manager templates
├── .github/
│   └── workflows/         # GitHub Actions workflows
├── docs/                  # Project documentation
└── scripts/               # Build and deployment scripts
\`\`\`

## 🔄 Development Workflow

### Branch Strategy
- \`main\` - Production ready code
- \`develop\` - Integration branch
- \`feature/*\` - Feature development
- \`hotfix/*\` - Critical fixes

### Commit Conventions
We follow [Conventional Commits](https://www.conventionalcommits.org/):
- \`feat:\` - New features
- \`fix:\` - Bug fixes
- \`docs:\` - Documentation changes
- \`style:\` - Code style changes
- \`refactor:\` - Code refactoring
- \`test:\` - Test additions/changes
- \`chore:\` - Maintenance tasks

### Pull Request Process
1. Create feature branch from \`develop\`
2. Implement changes with tests
3. Ensure all checks pass
4. Submit PR with detailed description
5. Address review feedback
6. Merge after approval

## 🚀 Deployment

### Staging Environment
Automatic deployment to staging on push to \`develop\` branch.
- URL: https://advanced-software-wil-staging.azurewebsites.net

### Production Environment
Manual deployment to production via GitHub Actions.
- URL: https://advanced-software-wil.azurewebsites.net

### Infrastructure as Code
\`\`\`bash
# Deploy infrastructure
az deployment group create \\
  --resource-group rg-advanced-software-wil \\
  --template-file infrastructure/azure/main.bicep \\
  --parameters @infrastructure/azure/parameters.json
\`\`\`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 👥 Team

| Name | Role | GitHub | Email |
|------|------|--------|-------|
| Team Lead | Full-Stack Developer | [@teamlead](https://github.com/teamlead) | teamlead@example.com |
| Developer 1 | Frontend Developer | [@dev1](https://github.com/dev1) | dev1@example.com |
| Developer 2 | Backend Developer | [@dev2](https://github.com/dev2) | dev2@example.com |
| Developer 3 | DevOps Engineer | [@dev3](https://github.com/dev3) | dev3@example.com |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Additional Resources

- [Project Documentation](https://your-org.github.io/advanced-software-wil/)
- [API Documentation](https://your-org.github.io/advanced-software-wil/api/)
- [Architecture Decision Records](docs/adr/)
- [Deployment Guide](docs/deployment.md)

---

**Built with ❤️ by the Advanced Software WIL Team**
```

## 🔍 Validation Checklist

Your GitHub project setup is complete when:
- [ ] GitHub Project is created and configured
- [ ] Custom fields and views are set up
- [ ] Issue templates are configured
- [ ] Project automation rules are active
- [ ] GitHub Pages is enabled and accessible
- [ ] Comprehensive README is in place
- [ ] Team members have appropriate access
- [ ] Documentation structure is established

## 🎯 Practice Exercises

1. **Project Management:**
   - Create 10 sample issues using your templates
   - Practice moving issues through the workflow
   - Set up a sprint planning session

2. **Documentation:**
   - Customize the GitHub Pages theme
   - Add team photos and bios
   - Create API documentation pages

3. **Collaboration:**
   - Invite team members to the project
   - Practice reviewing and merging PRs
   - Set up team notification preferences

## 🎉 Next Steps

With your project infrastructure ready, proceed to:
- [Lab 1D: Copilot Onboarding](lab_1_d_copilot_onboarding.md)

## 📚 Additional Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Project Management Best Practices](https://www.atlassian.com/agile/project-management)

---

**Pro Tip:** Regularly update your project documentation and keep your project board current to maintain team alignment!
