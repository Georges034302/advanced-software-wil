
# 🚀 Capstone Project: Cloud-Native Microservices Application

## 🎯 Project Overview
This capstone project immerses students in real-world practices for delivering secure, scalable, and automated cloud-native software systems using Azure, GitHub, and DevSecOps principles. Each student is responsible for designing, building, testing and deploying an independent microservice. The team collaborates to deliver a unified system architecture with shared frontend integration.

## 📅 Duration & Assessment
- **Duration:** 10 weeks (due in week 10)  
- **Weight:** 80% of final grade  
- **Type:** Group-based project with individual contributions  
- **Focus:** Azure Cloud-native architecture, CI/CD GitHub Workflow, DevSecOps  

---

## ✅ Core Requirements
Teams must collaboratively design, develop, and deploy cloud-native microservices that demonstrate secure, scalable, and automated delivery using modern DevOps practices. Each student is responsible for an independent microservice integrated into a unified frontend, with deployment to Azure and full CI/CD coverage.

---

## 📦 Project Structure

This is a sample repository structure. Design your team repository following this model for consistency and collaboration:

```
group-capstone-repo/
├── README.md
├── frontend/
├── architecture/
│   ├── frontend/
│   │   ├── system-architecture.md
│   │   └── ci-cd-architecture.md
│   ├── service-a/
│   │   ├── system-architecture.md
│   │   ├── ci-cd-architecture.md
│   │   ├── data-architecture.md
│   │   ├── azure-architecture.md
│   │   ├── copilot-prompts.md
│   │   └── instructions.md
│   └── service-b/ ... etc.
├── .github/
│   └── workflows/
│       ├── ci-frontend.yml
│       ├── ci-service-a.yml
│       ├── codeql-frontend.yml
│       ├── codeql-service-a.yml
│       └── dependabot.yml
├── services/
│   ├── service-a-student1/
│   └── ...
└── project-board/
```

---

## 👥 Team Responsibilities

### ☁️ Azure Resources
- Provision Azure infrastructure for frontend using CLI/ARM
- Deploy app (frontend + services) to Azure App Service or AKS
- Manage shared secrets using GitHub Secrets or Azure Key Vault

### 🧩 System
- Maintain shared GitHub repo with standardized folder layout
- Build and deploy frontend UI integrating all services
- Ensure consistent API design and service integration
- Perform end-to-end testing

### ⚙️ CI/CD & DevOps
- Create and manage shared workflow (`ci-frontend.yml`)
- Automate build, test, deploy, and security scans
- Standardize naming, env variables, status checks
- Enforce CI/CD rules through PR reviews and branch protection

### 📄 Documentation
- Maintain group `README.md`
- Contribute to `/architecture/frontend/`
- Participate in team demo covering architecture, deployment, CI/CD, and DevSecOps

---

## 👤 Individual Responsibilities

### ☁️ Azure Resources
- Provision infrastructure (App Service or AKS, DB, Key Vault)
- Use CLI/ARM for resource setup
- Secure access with GitHub Secrets or Azure Key Vault

### 🧩 System
- Build a containerized microservice (CRUD API)
- Implement backend logic and optional lightweight UI
- Seed DB with ≥ 20 records
- Integrate with frontend and document API

### ⚙️ CI/CD & DevOps
- Create CI/CD workflow (`ci-service-<id>.yml`)
- Automate: build, test, scan, push (ACR), deploy
- Use Service Principal for Azure login
- Configure push/pull_request triggers and error handling

### 📄 Documentation
Located at `/architecture/service-<your-id>/`
- `system-architecture.md`
- `ci-cd-architecture.md`
- `data-architecture.md`
- `azure-architecture.md`
- `copilot-prompts.md`
- `instructions.md`

---

## 🔗 API & Integration Requirements

Each microservice must:
- Expose a RESTful CRUD API
- Return proper status codes and error handling
- Be integrated into the frontend UI
- Be documented in `system-architecture.md`

**Standard Endpoints:**
- `POST /entity`
- `GET /entity`
- `GET /entity/:id`
- `PUT /entity/:id`
- `DELETE /entity/:id`

---

## 📊 Marking Criteria (Total: 80%)

| #  | Area                                              | Weight (%) | Scope      |
|----|---------------------------------------------------|------------|------------|
| 1  | Repository structure and organization             | 2          | Team       |
| 2  | Group README.md                                   | 2          | Team       |
| 3  | GitHub Project Board                              | 2          | Team       |
| 4  | Frontend UI integration                           | 6          | Team       |
| 5  | API integration consistency                       | 4          | Team       |
| 6  | Azure provisioning for frontend                   | 4          | Team       |
| 7  | CI/CD for frontend                                | 6          | Team       |
| 8  | Final team demo                                   | 4          | Team       |
| 9  | Microservice functionality                        | 10         | Individual |
| 10 | REST API quality                                  | 4          | Individual |
| 11 | Azure provisioning (service + DB + Key Vault)     | 6          | Individual |
| 12 | Database integration                              | 5          | Individual |
| 13 | API documentation (system-architecture.md)        | 2          | Individual |
| 14 | CI/CD pipeline (build, test, deploy)              | 6          | Individual |
| 15 | Unit tests in pipeline                            | 3          | Individual |
| 16 | Security scans (CodeQL, Dependabot)               | 3          | Individual |
| 17 | Secret management                                 | 3          | Individual |
| 18 | Copilot usage + reflection                        | 2          | Individual |
| 19 | Technical documentation in /architecture/         | 3          | Individual |
| 20 | Individual presentation                           | 5          | Individual |

---

## ✅ Final Submission Checklist

- [ ] Shared GitHub repo with standard folder structure  
- [ ] Root `README.md` with project overview and deployment link  
- [ ] `/architecture/frontend/` and `/architecture/service-<id>/` docs completed  
- [ ] Project board active and linked  
- [ ] Functional microservice (CRUD + error handling)  
- [ ] Service deployed to Azure (App Service or AKS)  
- [ ] Database created, populated (≥ 20 records), and connected  
- [ ] CI/CD pipeline automates build, test, deploy  
- [ ] Image pushed to ACR, deployed to Azure  
- [ ] CodeQL + Dependabot integrated  
- [ ] Secrets managed securely  
- [ ] Copilot prompts documented with reflection  
- [ ] Frontend integrates all services  
- [ ] Team presentation delivered with live demo
