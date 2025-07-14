# Group Project Template: Capstone Collaboration Guide

## 📋 Project Overview

### 🔍 What It Is
A collaborative capstone project where teams work together to build a cloud-native microservices application. This template guides you through team formation, role assignment, weekly tracking, and effective use of GitHub Projects for project management.

### 🎯 Team Collaboration Objectives
- Form effective development teams with clear roles
- Establish collaborative workflows using GitHub Projects
- Track weekly progress and milestones
- Practice professional project management
- Develop communication and coordination skills
- Learn agile development methodologies

### 🏗️ Generic Project Structure
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Service A     │    │   Service B     │    │   Service C     │
│   (Student 1)   │    │   (Student 2)   │    │   (Student 3)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                       ┌─────────────────┐
                       │   Service D     │
                       │   (Student 4)   │
                       └─────────────────┘
```

## 👥 Team Formation & Sign-Up Process

### Step 1: Team Registration
1. **Create Team Sign-Up Issue**
   - Go to your repository's Issues tab
   - Create a new issue titled "Team Formation - [Your Team Name]"
   - Use the team formation template below

### Team Sign-Up Template
```markdown
## Team Information
**Team Name:** [Choose a creative team name]
**Team Size:** [4 members recommended]

## Team Members
| Name | GitHub Username | Email | Preferred Role |
|------|----------------|-------|----------------|
| [Member 1] | @username1 | email1@example.com | [Role] |
| [Member 2] | @username2 | email2@example.com | [Role] |
| [Member 3] | @username3 | email3@example.com | [Role] |
| [Member 4] | @username4 | email4@example.com | [Role] |

## Service Assignment
**Primary Service:** [Service A/B/C/D]
**Each Student Selects a Service:** [Service: choice]

## Team Agreement
- [ ] All members agree to weekly check-ins
- [ ] Communication channel established (Projects/Teams)
- [ ] GitHub collaboration rules understood
- [ ] Weekly progress tracking committed
```

### Available Team Roles
- **🚀 DevOps Engineer/Developer** - Deployment, CI/CD, infrastructure [Each student in the team must assume this role]

## 📊 GitHub Projects Setup & Management

### Step 1: Create Project Board
1. Navigate to your repository
2. Click **Projects** tab → **New Project**
3. Choose **Team Backlog** template
4. Name it: "[Team Name] - Capstone Project"

### Step 2: Configure Board Columns
```
📋 Backlog          ⏳ Sprint Ready      🏃 In Progress      
👀 Review           ✅ Done             🚫 Blocked
```

### Step 3: Add Custom Fields
- **🏷️ Priority:** High, Medium, Low, Critical
- **📊 Story Points:** 1, 2, 3, 5, 8, 13
- **🎯 Sprint:** Sprint 1, Sprint 2, Sprint 3, Sprint 4
- **👤 Assignee:** Team member names
- **🏷️ Component:** Frontend, Backend, DevOps, Documentation, Testing

### Step 4: Create Issue Templates
Go to Settings → Features → Issues → Set up templates

**Feature Template:**
```markdown
## Feature Description
Brief description of what needs to be built

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Technical Requirements
- [ ] API endpoint created
- [ ] Database schema updated
- [ ] Tests written
- [ ] Documentation updated

## Definition of Done
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Deployed to staging
- [ ] Documentation updated
```

## 📅 Weekly Tracking & Milestones

### Weekly Sprint Structure

#### 🗓️ Week 1-2: Foundation Sprint
**Focus:** Team setup and planning

**Weekly Tasks:**
- [ ] Team formation and role assignment
- [ ] GitHub repository setup
- [ ] Project board configuration
- [ ] Initial planning and architecture
- [ ] Communication channels established

**Deliverables:**
- [ ] Team charter document
- [ ] Project board with initial backlog
- [ ] Architecture diagram
- [ ] Team communication established

#### 🗓️ Week 3-4: Development Sprint 1
**Focus:** Core implementation begins

**Weekly Tasks:**
- [ ] First service implementation started
- [ ] Development environment setup
- [ ] Basic CRUD operations
- [ ] Initial testing framework
- [ ] Code review process established

**Deliverables:**
- [ ] First working service prototype
- [ ] Test suite foundation
- [ ] Development workflow documented
- [ ] Code standards agreed upon

#### 🗓️ Week 5-6: Development Sprint 2
**Focus:** Testing and performance optimization

**Weekly Tasks:**
- [ ] Unit testing implementation for all services
- [ ] Integration testing between services
- [ ] Performance testing and benchmarking
- [ ] Load testing and stress testing
- [ ] Code quality analysis and optimization
- [ ] Test automation setup
- [ ] Performance monitoring implementation

**Deliverables:**
- [ ] Comprehensive test suite with >80% coverage
- [ ] Performance benchmarks and optimization reports
- [ ] Automated testing pipeline
- [ ] Load testing results and recommendations
- [ ] Performance monitoring dashboard

#### 🗓️ Week 7-8: Development Sprint 3
**Focus:** Security (DevSecOps) and database optimization

**Weekly Tasks:**
- [ ] Security vulnerability assessment
- [ ] Authentication and authorization implementation
- [ ] Database security and access controls
- [ ] Data encryption and secure communication
- [ ] Security scanning integration in CI/CD
- [ ] Database performance optimization
- [ ] Backup and recovery procedures

**Deliverables:**
- [ ] Security audit report and remediation
- [ ] Secure authentication system implemented
- [ ] Database security measures in place
- [ ] Encrypted data transmission
- [ ] DevSecOps pipeline with security gates
- [ ] Database optimization and backup strategy

#### 🗓️ Week 9-10: Final Sprint
**Focus:** Deployment and presentation

**Weekly Tasks:**
- [ ] Production deployment
- [ ] Final testing and bug fixes
- [ ] Presentation preparation
- [ ] Documentation completion
- [ ] Project retrospective

**Deliverables:**
- [ ] Deployed application
- [ ] Final presentation
- [ ] Complete documentation
- [ ] Team retrospective report

### Daily Standups (Recommended)
**Time:** Same time daily (15 minutes max)
**Format:**
- What did I complete yesterday?
- What will I work on today?
- Are there any blockers?
- Do I need help from teammates?

### Weekly Team Reviews
**When:** End of each week
**Duration:** 30-60 minutes
**Agenda:**
1. Review completed work
2. Update project board
3. Plan next week's tasks
4. Address any blockers
5. Update team progress tracking

## 📈 Progress Tracking Templates

### Weekly Progress Report Template
```markdown
# Week [X] Progress Report - [Team Name]

## 📊 Sprint Summary
**Sprint Goal:** [What was the main objective]
**Completed Story Points:** [X out of Y planned]
**Team Velocity:** [Story points per week]

## ✅ Completed This Week
- [ ] Task 1 - @username
- [ ] Task 2 - @username
- [ ] Task 3 - @username

## 🚧 In Progress
- [ ] Task 4 - @username (Expected completion: [date])
- [ ] Task 5 - @username (Expected completion: [date])

## 🚫 Blockers & Challenges
- **Blocker 1:** Description and plan to resolve
- **Blocker 2:** Description and plan to resolve

## 📅 Next Week Plan
- [ ] Priority task 1
- [ ] Priority task 2
- [ ] Priority task 3

## 🎯 Team Health Check
**Communication:** 😊 Excellent / 😐 Good / 😟 Needs Improvement
**Collaboration:** 😊 Excellent / 😐 Good / 😟 Needs Improvement
**Progress:** 😊 On Track / 😐 Slight Delay / 😟 Behind Schedule

## 📝 Notes & Decisions
- Important decisions made this week
- Changes to original plan
- Lessons learned
```

### Individual Contribution Tracking
```markdown
## Personal Weekly Report - [Your Name]

### This Week's Contributions
- **Code Commits:** [Number] commits
- **Issues Closed:** [Number] issues
- **Pull Requests:** [Number] PRs created/reviewed
- **Team Meetings:** [Number] attended

### Key Accomplishments
1. [Specific achievement 1]
2. [Specific achievement 2]
3. [Specific achievement 3]

### Challenges Faced
- [Challenge 1 and how you addressed it]
- [Challenge 2 and how you addressed it]

### Support Needed
- [Areas where you need team help]
- [Technical guidance needed]

### Next Week Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]
```

## 🤝 Collaboration Best Practices

### GitHub Workflow
1. **Branch Strategy**
   ```
   main (production)
   ├── develop (integration)
   │   ├── feature/service-a-auth
   │   ├── feature/service-b-crud
   │   └── bugfix/login-validation
   ```

2. **Pull Request Process**
   - Create feature branch from `develop`
   - Make changes and commit regularly
   - Open PR with detailed description
   - Request review from 2+ team members
   - Address feedback and iterate
   - Merge only after approval

3. **Commit Message Standards**
   ```
   feat: add user authentication endpoint
   fix: resolve database connection timeout
   docs: update API documentation
   test: add unit tests for validation
   refactor: improve error handling logic
   ```

### Communication Guidelines
- **Daily Updates:** Post brief status in team channel
- **Weekly Meetings:** Mandatory team sync every week
- **Issue Discussion:** Use GitHub issues for technical discussions
- **Decision Making:** Document important decisions in GitHub wiki
- **Help Requests:** Tag relevant team members for assistance

### Conflict Resolution
1. **Technical Disagreements**
   - Schedule team discussion
   - Present pros/cons of each approach
   - Vote if needed
   - Document decision rationale

2. **Workload Issues**
   - Discuss in weekly team meeting
   - Redistribute tasks if needed
   - Ask for instructor mediation if required

3. **Communication Problems**
   - Address directly and professionally
   - Use team lead as mediator
   - Escalate to instructor if unresolved

## 🎯 Success Metrics

### Team Collaboration Metrics
- **Meeting Attendance:** >90% attendance rate
- **Response Time:** <24 hours for team communications
- **Code Review Participation:** All team members reviewing PRs
- **Issue Resolution:** Average resolution time <3 days

### GitHub Activity Metrics
- **Commit Frequency:** Regular commits from all members
- **PR Quality:** Detailed descriptions and proper reviews
- **Issue Management:** All issues properly labeled and tracked
- **Documentation:** README and wiki kept up-to-date

### Project Progress Metrics
- **Sprint Completion:** Meeting sprint goals consistently
- **Velocity Tracking:** Stable or improving story point completion
- **Quality Metrics:** Low bug rate, good test coverage
- **Deployment Success:** Successful weekly deployments

## 🚀 Getting Started Checklist

### Phase 1: Team Formation (Week 1)
- [ ] Fill out team sign-up issue
- [ ] Get instructor approval for team composition
- [ ] Exchange contact information
- [ ] Set up communication channel (Discord/Slack)
- [ ] Schedule weekly meeting time
- [ ] Assign preliminary roles

### Phase 2: Project Setup (Week 1-2)
- [ ] Create GitHub repository (if not provided)
- [ ] Set up GitHub Projects board
- [ ] Configure issue templates
- [ ] Create initial project backlog
- [ ] Define team working agreements
- [ ] Set up development environment

### Phase 3: Development Kickoff (Week 2)
- [ ] Define technical architecture
- [ ] Create first sprint backlog
- [ ] Start first development tasks
- [ ] Begin weekly progress tracking
- [ ] Establish code review process
- [ ] Document team decisions

---

**Remember:** This capstone project is as much about learning to work effectively in teams as it is about technical implementation. Focus on communication, collaboration, and consistent progress tracking!
---

**Remember:** This capstone project is as much about learning to work effectively in teams as it is about technical implementation. Focus on communication, collaboration, and consistent progress tracking!
