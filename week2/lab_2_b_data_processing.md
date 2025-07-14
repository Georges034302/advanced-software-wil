# Lab 2B: Data Processing with Pipes and Redirection

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Master I/O redirection and piping concepts
- Process and manipulate text data using Unix tools
- Combine commands effectively for complex data operations
- Use GitHub Copilot to create sophisticated data processing pipelines

## 📋 Prerequisites
- Completion of Lab 2A (Filesystem Navigation)
- Basic understanding of command line interface
- GitHub Copilot enabled

---

## Part 1: I/O Redirection Fundamentals

### 1.1 Understanding Streams
Every Unix process has three standard streams:
- **stdin (0)**: Standard input
- **stdout (1)**: Standard output  
- **stderr (2)**: Standard error

**💡 Copilot Prompt:**
```
Explain the difference between stdout and stderr in Unix, and show me examples of redirecting each to different files.
```

### 1.2 Basic Redirection

```bash
# Output redirection
echo "Hello World" > output.txt           # Redirect stdout to file (overwrites)
echo "Second line" >> output.txt          # Append stdout to file
ls non-existent 2> error.log             # Redirect stderr to file
ls /home > success.log 2> error.log      # Redirect both separately

# Input redirection
sort < unsorted.txt                       # Read input from file
sort < input.txt > sorted.txt            # Input from file, output to file

# Combine stdout and stderr
ls /home /fake 2>&1 > combined.log       # Redirect stderr to stdout, then to file
ls /home /fake &> combined.log           # Shorthand for above (bash)
```

### 1.3 Advanced Redirection

```bash
# Here documents
cat << EOF > multiline.txt
This is line 1
This is line 2
This is line 3
EOF

# Here strings
grep "pattern" <<< "search in this string"

# Null device
ls /fake 2> /dev/null                    # Discard error output
```

**📝 Exercise 1: Create sample data files**
```bash
# Create test data files for the rest of the lab
echo -e "John,25,Engineer\nJane,30,Designer\nBob,35,Manager" > employees.csv
echo -e "apple\nbanana\ncherry\napple\ndate\nbanana" > fruits.txt
seq 1 100 > numbers.txt
```

---

## Part 2: Pipes and Command Chaining

### 2.1 Basic Piping

```bash
# Pipe stdout of one command to stdin of another
ls -l | grep ".txt"                      # List files, filter for .txt
cat file.txt | wc -l                     # Count lines in file
ps aux | grep python                     # Find Python processes

# Chain multiple commands
cat employees.csv | cut -d',' -f1 | sort | uniq
```

### 2.2 Tee Command
Split output to both file and stdout:

```bash
ls -l | tee file_list.txt | grep ".sh"   # Save to file AND continue pipeline
echo "Important log" | tee -a log.txt    # Append to file AND display
```

**🤖 Copilot Exercise 1:**
```
I want to monitor system processes, save the output to a log file, and also see it on screen. Create a command that shows all processes, saves them to processes.log, and displays only Python processes on screen.
```

---

## Part 3: Text Processing Tools

### 3.1 Cut - Column Extraction

```bash
# Extract specific columns
cut -d',' -f1 employees.csv              # First column (delimiter: comma)
cut -d',' -f1,3 employees.csv           # First and third columns
cut -c1-5 employees.csv                  # Characters 1-5 from each line

# Practical examples
ps aux | cut -d' ' -f1,11               # Extract username and command
cat /etc/passwd | cut -d':' -f1,7       # Extract username and shell
```

### 3.2 Grep - Pattern Matching

```bash
# Basic pattern matching
grep "pattern" file.txt                  # Find lines containing pattern
grep -i "pattern" file.txt              # Case-insensitive search
grep -v "pattern" file.txt              # Invert match (lines NOT containing)
grep -n "pattern" file.txt              # Show line numbers
grep -c "pattern" file.txt              # Count matching lines

# Regular expressions
grep "^apple" fruits.txt                 # Lines starting with 'apple'
grep "e$" fruits.txt                     # Lines ending with 'e'
grep "[0-9]" employees.csv               # Lines containing digits
grep -E "(apple|banana)" fruits.txt     # Extended regex (OR pattern)

# Recursive search
grep -r "function" /path/to/code/        # Search in all files recursively
grep -r --include="*.py" "def" ./        # Search only in Python files
```

### 3.3 Sed - Stream Editor

```bash
# Substitution
sed 's/old/new/' file.txt               # Replace first occurrence per line
sed 's/old/new/g' file.txt              # Replace all occurrences
sed 's/old/new/gi' file.txt             # Global, case-insensitive

# Line operations
sed '2d' file.txt                        # Delete line 2
sed '1,3d' file.txt                      # Delete lines 1-3
sed -n '2,4p' file.txt                   # Print only lines 2-4

# In-place editing
sed -i 's/old/new/g' file.txt           # Modify file directly
sed -i.bak 's/old/new/g' file.txt       # Create backup before modifying
```

### 3.4 Awk - Text Processing Language

```bash
# Basic syntax: awk 'pattern { action }' file
awk '{print $1}' employees.csv          # Print first field
awk -F',' '{print $1, $3}' employees.csv # Set field separator to comma

# Built-in variables
awk '{print NR, $0}' file.txt           # NR = line number, $0 = whole line
awk '{print NF, $NF}' file.txt          # NF = number of fields, $NF = last field

# Conditional processing
awk -F',' '$2 > 30 {print $1}' employees.csv     # Print names where age > 30
awk 'length($0) > 5' fruits.txt                   # Lines longer than 5 characters

# Calculations
awk -F',' '{sum += $2} END {print "Average age:", sum/NR}' employees.csv
```

**🤖 Copilot Exercise 2:**
```
I have a CSV file with columns: name,age,department,salary. Create an awk command to find the average salary by department and display it formatted nicely.
```

---

## Part 4: Data Sorting and Manipulation

### 4.1 Sort - Arranging Data

```bash
# Basic sorting
sort file.txt                           # Alphabetical sort
sort -n numbers.txt                      # Numerical sort
sort -r file.txt                        # Reverse sort
sort -u file.txt                        # Sort and remove duplicates

# Field-based sorting
sort -t',' -k2 employees.csv            # Sort by 2nd field (comma-separated)
sort -t',' -k2n employees.csv           # Numerical sort by 2nd field
sort -t',' -k2nr employees.csv          # Reverse numerical sort by 2nd field

# Multiple fields
sort -t',' -k3,3 -k2n employees.csv     # Sort by 3rd field, then by 2nd numerically
```

### 4.2 Head and Tail - Limiting Output

```bash
# First/last lines
head -n 5 file.txt                      # First 5 lines
tail -n 5 file.txt                      # Last 5 lines
head -n -5 file.txt                     # All except last 5 lines
tail -n +5 file.txt                     # From line 5 to end

# Following files (useful for logs)
tail -f /var/log/syslog                 # Follow file changes
tail -f --pid=1234 logfile.txt          # Follow until process 1234 dies
```

### 4.3 Paste - Joining Files

```bash
# Join files side by side
paste file1.txt file2.txt               # Default tab separator
paste -d',' file1.txt file2.txt         # Comma separator
paste -s file.txt                       # Join lines of single file

# Practical example
paste -d',' <(cut -d',' -f1 employees.csv) <(cut -d',' -f3 employees.csv)
```

**📝 Exercise 2: Data Pipeline Practice**
Create a pipeline that:
1. Takes the employees.csv file
2. Filters for employees older than 25
3. Sorts by age
4. Extracts only names and departments
5. Saves to a new file

**💡 Copilot Prompt:**
```
Create a command pipeline to process employees.csv: filter age > 25, sort by age, show only name and department, save to filtered_employees.txt
```

---

## Part 5: Advanced Data Processing Scenarios

### 5.1 Log Analysis

**Scenario:** Analyze web server logs

**💡 Copilot Prompt:**
```
I have Apache access logs with this format: IP - - [timestamp] "METHOD /path HTTP/1.1" status size. Create commands to find the top 10 most requested pages and the most common error codes.
```

```bash
# Sample log analysis commands
# Find top 10 IP addresses
cut -d' ' -f1 access.log | sort | uniq -c | sort -nr | head -10

# Find 404 errors
grep " 404 " access.log | cut -d' ' -f7 | sort | uniq -c | sort -nr

# Requests per hour
cut -d'[' -f2 access.log | cut -d':' -f2 | sort | uniq -c
```

### 5.2 System Monitoring

```bash
# Process monitoring
ps aux | awk '$3 > 1.0 {print $1, $2, $3, $11}' | sort -k3nr

# Memory usage by user
ps aux | awk '{sum[$1] += $4} END {for (user in sum) print user, sum[user]"%"}' | sort -k2nr

# Disk usage analysis
du -h /home | sort -hr | head -20
```

### 5.3 Data Transformation

**🤖 Copilot Exercise 3:**
```
I have a file with email addresses on each line. Create a pipeline to extract just the domain names, count how many times each domain appears, and show the top 5 most common domains.
```

---

## Part 6: Real-World Data Processing Projects

### 6.1 CSV Data Analysis

Create a comprehensive analysis script:

**💡 Copilot Prompt:**
```
Create a bash pipeline to analyze a sales CSV with columns: date,product,category,price,quantity. I want to see: 1) Total sales by category, 2) Best selling products, 3) Daily sales trends.
```

### 6.2 Configuration File Processing

**Scenario:** Extract and process configuration values

```bash
# Extract configuration values
grep -v "^#" config.file | grep -v "^$" | cut -d'=' -f2

# Process multiple config files
find /etc -name "*.conf" | xargs grep "port" | cut -d':' -f2 | sort -u
```

### 6.3 Code Analysis

**💡 Copilot Prompt:**
```
Create commands to analyze Python source code files: count total lines of code (excluding comments and blank lines), find most common function names, and list files with most imports.
```

---

## Part 7: Performance and Optimization

### 7.1 Efficient Processing

```bash
# Use appropriate tools for the job
# For large files, prefer awk over multiple cut/grep combinations
awk -F',' '$2 > 30 && $3 == "Engineer" {print $1}' large_file.csv

# Buffer output for better performance
sort large_file.txt | uniq -c | sort -nr | head -100

# Parallel processing (if available)
cat large_file.txt | parallel --pipe --block 10M sort | sort -m
```

### 7.2 Memory Considerations

```bash
# Stream processing for large files
# Instead of: sort huge_file.txt > sorted.txt
# Use: sort huge_file.txt -o sorted.txt

# Process in chunks
split -l 10000 huge_file.txt chunk_
for chunk in chunk_*; do process_chunk "$chunk"; done
```

**🤖 Copilot Exercise 4:**
```
I need to process a 10GB log file to find error patterns. Create a memory-efficient pipeline that processes the file in chunks and aggregates results.
```

---

## Part 8: Lab Challenges

### Challenge 1: Weather Data Analysis
Given a CSV with weather data (date,temperature,humidity,pressure), create pipelines to:
- Find the hottest and coldest days
- Calculate monthly averages
- Identify days with extreme weather conditions

### Challenge 2: Server Log Processing
Process web server logs to:
- Identify security threats (multiple failed login attempts)
- Generate hourly traffic reports
- Find most accessed resources

### Challenge 3: Code Metrics
Analyze a codebase to:
- Count lines of code by file type
- Find most complex functions (by line count)
- Generate dependency reports

**💡 Copilot Prompt for All Challenges:**
```
For each challenge, create complete command pipelines with error handling and output formatting. Include comments explaining each step.
```

---

## 🎯 Lab Deliverables

Submit the following:

1. **Data Processing Scripts**: Three bash scripts demonstrating different data processing scenarios

2. **Command Reference**: Documented collection of useful command combinations discovered during the lab

3. **Performance Analysis**: Comparison of different approaches to the same data processing task

4. **Real-World Example**: Analysis of actual data (log files, CSV data, etc.) using the techniques learned

---

## ✅ Validation Steps

1. Successfully redirect input/output and handle errors appropriately
2. Create complex pipelines combining multiple commands
3. Process structured data (CSV, logs) efficiently
4. Use regular expressions effectively with grep and sed
5. Demonstrate understanding of when to use each tool (cut vs awk, grep vs sed)

---

## 🔗 Additional Resources

**Advanced Copilot Prompts:**
```
Show me how to use named pipes (FIFOs) for real-time data processing
Create a pipeline to process JSON data using only standard Unix tools
Generate commands for parallel data processing using GNU parallel
Explain how to handle binary data in Unix pipelines
```

**Next Steps**: This lab prepares you for Lab 2C where you'll learn bash scripting fundamentals.

---

**📚 Key Takeaways:**
- Master I/O redirection for flexible data flow
- Combine Unix tools effectively for complex processing
- Choose the right tool for each text processing task
- Use Copilot to discover advanced processing techniques
- Understand performance implications of different approaches
