# Lab 1B: GitHub Practices

## 🎯 Objectives
- Master essential Git commands and workflows
- Practice creating meaningful commits
- Learn branching and merging strategies
- Create and manage Pull Requests
- Understand collaborative development workflows

## 📋 Prerequisites
- Completed [Lab 1A: Environment Setup](lab_1_a_environment_setup.md)
- GitHub account and repository access
- Basic understanding of version control concepts

## 🚀 Git Fundamentals

### Step 1: Repository Setup and Initial Configuration

```bash
# Configure Git with your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Step 2: Basic Git Commands

Let's practice the fundamental Git operations:

```bash
# Check repository status
git status

# View commit history
git log --oneline

# Check current branch
git branch
```

### Step 3: Making Meaningful Commits

Good commit practices are essential for project maintainability:

```bash
# Create a new file for practice
echo "# My Practice File" > practice.md

# Stage the file
git add practice.md

# Create a commit with a meaningful message
git commit -m "feat: add practice markdown file for Git exercises"

# View the commit
git log --oneline -1
```

#### Commit Message Best Practices

Follow the conventional commit format:
- `feat:` - new feature
- `fix:` - bug fix
- `docs:` - documentation changes
- `style:` - formatting changes
- `refactor:` - code restructuring
- `test:` - adding tests
- `chore:` - maintenance tasks

### Step 4: Branching Strategy

#### Creating and Working with Branches

```bash
# Create and switch to a new branch
git checkout -b feature/add-documentation

# Alternative modern syntax
git switch -c feature/add-documentation

# List all branches
git branch -a

# Check current branch
git branch --show-current
```

#### Working on the Feature Branch

```bash
# Make changes to your files
echo "## Documentation Section" >> practice.md
echo "This file demonstrates Git practices." >> practice.md

# Stage and commit changes
git add practice.md
git commit -m "docs: add documentation section to practice file"

# View branch history
git log --oneline --graph
```

### Step 5: Merging Strategies

#### Fast-Forward Merge

```bash
# Switch back to main branch
git checkout main

# Merge feature branch (fast-forward)
git merge feature/add-documentation

# View the merged history
git log --oneline --graph
```

#### Creating a Merge Commit

```bash
# Create another feature branch
git checkout -b feature/add-examples

# Make changes
echo "## Examples" >> practice.md
echo "- Example 1: Basic Git workflow" >> practice.md
echo "- Example 2: Branch management" >> practice.md

git add practice.md
git commit -m "feat: add examples section with Git workflow examples"

# Switch to main and merge with no fast-forward
git checkout main
git merge --no-ff feature/add-examples -m "merge: integrate examples feature"
```

### Step 6: Pull Request Workflow

#### Creating a Pull Request

1. **Push your branch to remote:**
   ```bash
   git checkout -b feature/improve-readme
   
   # Make some changes
   echo "## Additional Resources" >> practice.md
   echo "- [Git Documentation](https://git-scm.com/doc)" >> practice.md
   
   git add practice.md
   git commit -m "docs: add additional resources section"
   
   # Push branch to remote
   git push origin feature/improve-readme
   ```

2. **Create PR via GitHub Web Interface:**
   - Navigate to your repository on GitHub
   - Click "Compare & pull request" button
   - Fill in PR title and description
   - Assign reviewers if working in a team
   - Add labels and link issues if applicable

3. **PR Best Practices:**
   - Write clear, descriptive titles
   - Include detailed descriptions
   - Reference related issues
   - Keep PRs focused and small
   - Respond to review feedback promptly

#### Managing Pull Requests

```bash
# Update your PR branch with latest main
git checkout main
git pull origin main
git checkout feature/improve-readme
git rebase main

# Push updated branch (may need force push after rebase)
git push origin feature/improve-readme --force-with-lease
```

### Step 7: Collaborative Workflows

#### Handling Conflicts

Create a merge conflict scenario:

```bash
# On main branch, modify the same line
git checkout main
echo "Main branch content" >> practice.md
git add practice.md
git commit -m "fix: update content from main branch"

# On feature branch, modify the same line differently
git checkout feature/improve-readme
echo "Feature branch content" >> practice.md
git add practice.md
git commit -m "feat: update content from feature branch"

# Try to merge - this will create a conflict
git checkout main
git merge feature/improve-readme
```

Resolve the conflict:
1. Open the conflicted file
2. Edit to resolve conflicts (remove conflict markers)
3. Stage the resolved file: `git add practice.md`
4. Complete the merge: `git commit`

### Step 8: Advanced Git Operations

#### Interactive Rebase

```bash
# Clean up commit history before merging
git checkout feature/improve-readme
git rebase -i HEAD~3

# In the interactive editor, you can:
# - squash commits together
# - reorder commits
# - edit commit messages
# - drop unwanted commits
```

#### Cherry-picking

```bash
# Apply specific commits from another branch
git cherry-pick <commit-hash>
```

## 🔍 Validation Checklist

Your Git skills are ready when you can:
- [ ] Create meaningful commit messages
- [ ] Create and manage branches effectively
- [ ] Merge branches using different strategies
- [ ] Create and manage Pull Requests
- [ ] Resolve merge conflicts
- [ ] Collaborate effectively using Git workflows
- [ ] Use advanced Git operations (rebase, cherry-pick)

## 🎯 Practice Exercises

1. **Commit Message Practice:**
   - Create 5 different commits using various conventional commit types
   - Practice writing clear, descriptive commit messages

2. **Branching Exercise:**
   - Create a feature branch
   - Make several commits
   - Practice different merge strategies

3. **Collaboration Simulation:**
   - Work with a partner or simulate multiple developers
   - Practice resolving conflicts
   - Review each other's Pull Requests

## 🎉 Next Steps

With Git fundamentals mastered, continue to:
- [Lab 1C: GitHub Projects](lab_1_c_github_projects.md)

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)

---

**Pro Tip:** Practice these Git workflows regularly - they form the foundation of professional software development!
