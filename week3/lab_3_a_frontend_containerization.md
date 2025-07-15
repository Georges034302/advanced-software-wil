# Lab 3A: Frontend Containerization - Simple Player List

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Use GitHub Copilot to create a simple web application
- Containerize a web app using Docker
- Run and access containerized applications in Codespaces

## 📋 Prerequisites
- Frontend Web Application Knowledge

---

## Part 1: Use Copilot to Create a Simple Player App

### 1.1 Project Setup

**📝 Create project folder:**
```bash
mkdir playerapp-frontend
cd playerapp-frontend
```

### 1.2 Generate HTML with Copilot

**💡 Ask Copilot Chat:**
```
Create a simple HTML page for a player scoreboard. Include basic structure with links to external CSS and JS files. Keep it minimal - just heading, player list div, and a button.
```

**📝 Exercise 1:** Create `index.html` and let Copilot generate:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Player App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>🎮 Player List</h1>
    <div id="players"></div>
    <button onclick="generatePlayers()">Generate Players</button>
    <script src="app.js"></script>
</body>
</html>
```

### 1.3 Generate CSS with Copilot

**💡 Ask Copilot Chat:**
```
Create simple CSS for a player list app. Include basic styling for body, h1, player divs, and a button. Use light colors and simple layout.
```

**📝 Exercise 2:** Create `style.css`:
```css
body {
    font-family: Arial;
    margin: 40px;
    background: #f5f5f5;
}

h1 {
    color: #333;
    text-align: center;
}

.player {
    padding: 10px;
    background: white;
    border: 1px solid #ddd;
    margin: 5px 0;
    border-radius: 5px;
}

button {
    padding: 10px 20px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    display: block;
    margin: 20px auto;
}
```

### 1.4 Generate JavaScript with Copilot

**💡 Ask Copilot Chat:**
```
Create simple JavaScript to generate 5 random players with ID (3 digits), name (Player-XXXXXX format), and score (0-100). Display them in a div with ID "players".
```

**📝 Exercise 3:** Create `app.js`:
```javascript
function generatePlayers() {
    const players = [];
    
    for (let i = 0; i < 5; i++) {
        players.push({
            id: Math.floor(Math.random() * 900) + 100,
            name: `Player-${Math.floor(Math.random() * 900) + 100}`,
            score: Math.floor(Math.random() * 101)
        });
    }
    
    document.getElementById('players').innerHTML = players
        .map(p => `<div class="player">ID: ${p.id} | ${p.name} | Score: ${p.score}</div>`)
        .join('');
}

generatePlayers();
```

---

## Part 2: Containerize with Docker (using Copilot)

### 2.1 Create Dockerfile with Copilot

**💡 Ask Copilot Chat:**
```
Create a simple Dockerfile to serve this HTML file using nginx. Keep it minimal.
```

**📝 Exercise 4:** Create `Dockerfile`:
```dockerfile
# Simple nginx container for HTML app
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
EXPOSE 80
```

```bash
# Build the image
docker build -t player-app .

# Run the container
docker run -d --name player-frontend -p 3000:80 player-app

# Check if it's running
docker ps
```

---

## Part 3: Test in Codespaces

### 3.1 Access Your App

**💡 In GitHub Codespaces:**
1. **Ports tab** shows port 3000
2. **Click "Open in Browser"**
3. **Test the button**

**💡 For Local Development:**
1. **Open browser** and go to `http://localhost:3000`
2. **Test the button** to generate random players
3. **Refresh the page** to see new random players generated


### 3.2 Troubleshooting with Copilot

**Ask Copilot if issues occur:**
```
My Docker container isn't accessible on port 3000. What should I check?
```

### 3.3 Docker Management with Copilot

**💡 Ask Copilot for container management commands:**
```
Show me useful Docker commands to manage my player-app container (start, stop, remove, logs).
```

**📝 Exercise 5:** Practice stopping, starting, and checking container logs

```bash
# View running containers
docker ps

# Stop the container
docker stop player-frontend

# Start it again
docker start player-frontend

# Remove the container
docker rm player-frontend

# View logs
docker logs player-frontend

# Remove the image
docker rmi player-app
```

---

## ✅ Conclusion

✅ **Used Copilot effectively** - Generated code, Dockerfile, and commands  
✅ **Created a simple web app** - Three separate files (HTML, CSS, JS)  
✅ **Containerized the app** - Built and ran with Docker  
✅ **Tested in Codespaces** - Accessed through port forwarding  


**🔮 Next:** Lab 3B - Backend API Development with Flask!

---

*Lab 3A: Frontend Containerization (with Copilot) - Complete* 🎉