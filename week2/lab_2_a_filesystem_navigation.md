# Lab 2A: Filesystem Navigation and Permissions

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Navigate the Unix filesystem efficiently using basic CLI commands
- Understand and manage file permissions and ownership
- Use globbing patterns for file operations
- Leverage GitHub Copilot for command discovery and troubleshooting

## 📋 Prerequisites
- GitHub Codespace or Unix/Linux terminal access
- GitHub Copilot enabled
- Completion of Lab 1A (Environment Setup)

---

## Part 1: Basic Navigation Commands

### 1.1 Getting Started with Copilot Chat
Before diving into commands, let's set up Copilot to help us learn:

**💡 Copilot Prompt:**
```
I'm learning Unix CLI commands for filesystem navigation. Can you explain the difference between absolute and relative paths, and show me examples of each?
```

### 1.2 Directory Navigation
Practice these fundamental navigation commands:

```bash
# Print current working directory
pwd

# List directory contents
ls
ls -l        # Long format
ls -la       # Include hidden files
ls -lh       # Human-readable file sizes

# Change directories
cd /home     # Absolute path
cd ..        # Parent directory
cd ~         # Home directory
cd -         # Previous directory

# Create directories
mkdir test_lab
mkdir -p projects/week2/scripts  # Create nested directories
```

**🤖 Copilot Exercise 1:**
Ask Copilot to generate a command that lists all files modified in the last 7 days:
```
@workspace /terminal Generate a command to list all files in the current directory that were modified in the last 7 days
```

### 1.3 File Content Operations

```bash
# View file contents
cat filename.txt           # Display entire file
less filename.txt          # Page through file (q to quit)
head filename.txt          # First 10 lines
head -n 5 filename.txt     # First 5 lines
tail filename.txt          # Last 10 lines
tail -f logfile.txt        # Follow file changes (real-time)

# Create and edit files
touch newfile.txt          # Create empty file
echo "Hello World" > file.txt        # Write to file (overwrites)
echo "Second line" >> file.txt       # Append to file
```

**📝 Exercise 1: Create a sample file structure**
```bash
# Create this structure using mkdir and touch
# Use Copilot to help generate the commands
projects/
├── web/
│   ├── index.html
│   └── style.css
├── scripts/
│   ├── backup.sh
│   └── deploy.sh
└── docs/
    ├── README.md
    └── notes.txt
```

**💡 Copilot Prompt:**
```
Generate bash commands to create the directory structure above with all the files
```

---

## Part 2: File Operations (Copy, Move, Remove)

### 2.1 Copying Files and Directories

```bash
# Copy files
cp source.txt destination.txt           # Copy file
cp source.txt /path/to/destination/     # Copy to directory
cp -r directory/ new_directory/         # Copy directory recursively
cp *.txt backup/                        # Copy all .txt files

# Copy with preservation
cp -p file.txt backup/                  # Preserve timestamps and permissions
```

### 2.2 Moving and Renaming

```bash
# Move/rename files
mv oldname.txt newname.txt              # Rename file
mv file.txt /path/to/destination/       # Move file
mv *.log logs/                          # Move all .log files
```

### 2.3 Removing Files and Directories

```bash
# Remove files
rm filename.txt                         # Remove file
rm -i filename.txt                      # Interactive removal (asks confirmation)
rm *.tmp                               # Remove all .tmp files

# Remove directories
rmdir empty_directory/                  # Remove empty directory
rm -r directory/                        # Remove directory and contents
rm -rf directory/                       # Force remove (be careful!)
```

**🤖 Copilot Exercise 2:**
Ask Copilot to create a safe file cleanup script:
```
Create a bash script that safely removes temporary files older than 7 days from a project directory, with user confirmation
```

---

## Part 3: File Permissions and Ownership

### 3.1 Understanding Permissions

```bash
# View detailed permissions
ls -l filename.txt

# Permission format: -rwxrwxrwx
# - : file type (- = file, d = directory, l = link)
# rwx : owner permissions (read, write, execute)
# rwx : group permissions
# rwx : others permissions
```

### 3.2 Changing Permissions

```bash
# Symbolic method
chmod u+x script.sh                    # Add execute for user
chmod g-w file.txt                     # Remove write for group
chmod o+r file.txt                     # Add read for others
chmod a+r file.txt                     # Add read for all

# Numeric method
chmod 755 script.sh                    # rwxr-xr-x
chmod 644 file.txt                     # rw-r--r--
chmod 600 private.txt                  # rw-------
```

### 3.3 Changing Ownership

```bash
# Change owner (requires sudo for others' files)
sudo chown username file.txt
sudo chown username:groupname file.txt
sudo chown -R username:group directory/   # Recursive
```

**📝 Exercise 2: Permission Practice**
```bash
# Create these files with specific permissions using Copilot assistance:
# 1. A script file that only you can read/write/execute
# 2. A config file that everyone can read but only you can write
# 3. A log file that your group can read/write but others can only read
```

---

## Part 4: Globbing and Pattern Matching

### 4.1 Basic Globbing Patterns

```bash
# Wildcards
ls *.txt                               # All .txt files
ls file?.txt                           # file1.txt, fileA.txt, etc.
ls file[123].txt                       # file1.txt, file2.txt, file3.txt
ls file[a-z].txt                       # filea.txt, fileb.txt, etc.
ls file[!0-9].txt                      # Files NOT ending with numbers

# Brace expansion
touch file{1,2,3}.txt                  # Creates file1.txt, file2.txt, file3.txt
touch test{A..Z}.txt                   # Creates testA.txt through testZ.txt
mkdir {2024..2026}-{01..12}            # Creates year-month directories
```

### 4.2 Advanced Globbing

```bash
# Extended globbing (enable with: shopt -s extglob)
ls !(*.txt)                            # Everything except .txt files
ls *(*.sh|*.py)                        # Only .sh or .py files
ls +([0-9]).txt                        # Files with one or more digits
```

**🤖 Copilot Exercise 3:**
```
I need to find all configuration files in my project. They might end with .conf, .config, .cfg, or .ini. Generate a command using globbing to list all of them.
```

---

## Part 5: Practical Scenarios with Copilot

### 5.1 Project Organization

**Scenario:** You have a messy download folder with various file types that need organizing.

**💡 Copilot Prompt:**
```
I have a directory with mixed files (.pdf, .jpg, .txt, .zip, .mp4). Create commands to organize them into subdirectories by file type using mkdir, mv, and globbing patterns.
```

### 5.2 Backup Operations

**Scenario:** Create a backup of important configuration files.

**💡 Copilot Prompt:**
```
Generate commands to backup all .conf and .cfg files from /etc/ to a backup directory with today's date, preserving permissions and directory structure.
```

### 5.3 Development Cleanup

**Scenario:** Clean up development artifacts and temporary files.

**💡 Copilot Prompt:**
```
Create commands to safely remove common development temporary files (*.tmp, *.log, *.cache, node_modules/, __pycache__/) but ask for confirmation before deletion.
```

---

## Part 6: Lab Challenges

### Challenge 1: File System Explorer
Create a directory structure for a web development project and populate it with sample files:

**💡 Copilot Prompt:**
```
Generate commands to create a complete web project structure with HTML, CSS, JS files, and set appropriate permissions for a development environment.
```

### Challenge 2: Permission Management
Set up a shared project directory where:
- Owner can read/write/execute everything
- Group members can read/execute but not write
- Others have no access

### Challenge 3: Bulk Operations
You have 100+ image files with inconsistent naming. Use globbing to:
- Rename all .jpeg files to .jpg
- Move all images to an images/ subdirectory
- Create thumbnails directory with proper permissions

**🤖 Copilot Exercise 4:**
```
I have image files with names like IMG_001.jpeg, photo_001.JPEG, picture001.jpg. Create commands to standardize them all to lowercase .jpg extensions and organize them by date if possible.
```

---

## ✅ Validation Steps

1. Navigate to different directories using both absolute and relative paths
2. Create, copy, move, and delete files and directories
3. Successfully change file permissions using both symbolic and numeric methods
4. Use globbing patterns to operate on multiple files
5. Demonstrate safe file operations with appropriate confirmations

---

## 🔗 Additional Resources

- **Copilot Prompts for Further Learning:**
  ```
  Explain the difference between hard links and soft links in Unix
  Show me advanced find command examples for file management
  Generate a script to monitor disk usage and clean up when needed
  ```

- **Next Steps**: This lab prepares you for Lab 2B where you'll learn data processing with pipes and redirection.

---

**📚 Key Takeaways:**
- Master basic filesystem navigation and file operations
- Understand Unix permission system for security
- Use globbing patterns for efficient bulk operations
- Leverage Copilot for command discovery and script generation
