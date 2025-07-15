# Lab 3C: Full-Stack Integration - PlayerApp with Docker Compose

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Use GitHub Copilot to create Docker Compose configurations
- Build a complete PlayerApp with frontend, backend, and database
- Configure container networking and dependencies
- Deploy a full-stack application with one command

## 📋 Prerequisites
- Completion of Labs 3A (Frontend) and 3B (Backend)
- Understanding of Docker containers

---

## Part 1: Project Setup with Copilot

### 1.1 Create Full-Stack Project

**💡 Ask Copilot Chat:**
```
Show me how to create a Docker Compose file that connects a frontend (nginx), backend (Flask API), and database (MySQL) for a simple player app.
```

**📝 Exercise 1:** Create project structure:
```bash
mkdir playerapp-fullstack
cd playerapp-fullstack

# Create directories for each component
mkdir frontend backend database
```

### 1.2 Copy Files from Previous Labs

**Copy your work from previous labs:**
```bash
# Copy frontend files from Lab 3A
cp ../playerapp-frontend/* frontend/

# Copy backend files from Lab 3B  
cp ../playerapp-backend/* backend/

# Database will be set up automatically via Docker Compose
```

---

## Part 2: Create Docker Compose with Copilot

### 2.1 Main Docker Compose File

**💡 Ask Copilot Chat:**
```
Create a docker-compose.yml file for a playerapp with frontend (port 3000), backend (port 5000), and MySQL database with proper networking and dependencies.
```

**📝 Exercise 2:** Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  # MySQL Database
  database:
    image: mysql:8.0
    container_name: playerapp-database
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: playerdb
      MYSQL_USER: player
      MYSQL_PASSWORD: playerpass
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - playerapp-network

  # Flask Backend API
  backend:
    build: ./backend
    container_name: playerapp-backend
    environment:
      - DB_HOST=database
      - DB_PORT=3306
      - DB_USER=player
      - DB_PASSWORD=playerpass
      - DB_NAME=playerdb
    ports:
      - "5000:5000"
    depends_on:
      - database
    networks:
      - playerapp-network

  # Frontend Web Server
  frontend:
    build: ./frontend
    container_name: playerapp-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - playerapp-network

volumes:
  mysql_data:

networks:
  playerapp-network:
    driver: bridge
```

---

## Part 3: Update Backend for Container Environment

### 3.1 Update Backend Configuration

**💡 Ask Copilot Chat:**
```
Update my Flask app to use environment variables for database connection and work in Docker containers.
```

**📝 Exercise 3:** Update `backend/app.py`:
```python
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'player'),
    'password': os.getenv('DB_PASSWORD', 'playerpass'),
    'database': os.getenv('DB_NAME', 'playerdb')
}

def get_db_connection():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    return jsonify({
        "message": "PlayerApp API - Full Stack!", 
        "endpoints": ["/players", "/players/<id>"]
    })

@app.route('/players', methods=['GET'])
def get_players():
    """Get all players sorted by score"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM players ORDER BY score DESC")
        players = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({"players": players})
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """Get single player by ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM players WHERE id = %s", (player_id,))
        player = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if player:
            return jsonify({"player": player})
        else:
            return jsonify({"error": "Player not found"}), 404
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting PlayerApp API...")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## Part 4: Update Frontend for API Integration

### 4.1 Update Frontend JavaScript

**💡 Ask Copilot Chat:**
```
Update my frontend JavaScript to fetch player data from a backend API and display it in a table.
```

**📝 Exercise 4a:** Update `frontend/index.html` for table layout:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Player App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>&#127918; Player Scoreboard</h1>
    
    <div class="stats-container">
        <div id="stats">Loading...</div>
        <button id="refresh-btn">🔄 Refresh</button>
    </div>
    
    <table class="scoreboard">
        <thead>
            <tr>
                <th>Rank</th>
                <th>ID</th>
                <th>Name</th>
                <th>Score</th>
            </tr>
        </thead>
        <tbody id="players-body">
            <tr><td colspan="4">Loading players...</td></tr>
        </tbody>
    </table>
    
    <script src="app.js"></script>
</body>
</html>
```

**📝 Exercise 4b:** Update `frontend/style.css` for table styling:
```css
body {
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f5f5f5;
}

h1 {
    color: #333;
    text-align: center;
    margin-bottom: 30px;
}

.stats-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 15px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

#stats {
    font-size: 18px;
    font-weight: bold;
    color: #333;
}

button {
    padding: 10px 20px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
}

button:hover {
    background: #45a049;
}

.scoreboard {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.scoreboard th,
.scoreboard td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.scoreboard th {
    background: #4CAF50;
    color: white;
    font-weight: bold;
    text-align: center;
}

.scoreboard td {
    text-align: center;
}

.scoreboard tr:hover {
    background: #f5f5f5;
}

.rank-1 {
    background: #fff9c4 !important;
    font-weight: bold;
}

.rank-2 {
    background: #f0f8ff !important;
}

.rank-3 {
    background: #f5f5dc !important;
}
```

**📝 Exercise 4c:** Update `frontend/app.js`:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏆 PlayerApp Full Stack loaded!');
    
    // API base URL - robust Codespaces detection
    let API_BASE;
    
    if (window.location.protocol === 'https:') {
        // We're in Codespaces - construct the backend URL
        const hostname = window.location.hostname;
        if (hostname.includes('-3000.app.github.dev')) {
            API_BASE = `https://${hostname.replace('-3000.app.github.dev', '-5000.app.github.dev')}`;
        } else if (hostname.includes('-3000.githubpreview.dev')) {
            API_BASE = `https://${hostname.replace('-3000.githubpreview.dev', '-5000.githubpreview.dev')}`;
        } else if (hostname.includes('-3000.github.dev')) {
            API_BASE = `https://${hostname.replace('-3000.github.dev', '-5000.github.dev')}`;
        } else {
            // Fallback construction for any Codespaces variant
            API_BASE = window.location.origin.replace('-3000', '-5000').replace(':3000', ':5000');
        }
    } else {
        // Local development
        API_BASE = 'http://localhost:5000';
    }
    
    console.log('🌍 Current URL:', window.location.href);
    console.log('🔗 API Base URL:', API_BASE);
    
    // Load players when page loads
    loadPlayers();
    
    // Refresh button event
    document.getElementById('refresh-btn').addEventListener('click', loadPlayers);
    
    async function loadPlayers() {
        try {
            console.log('📡 Fetching players from API...');
            console.log('🔗 Using API URL:', `${API_BASE}/players`);
            
            const response = await fetch(`${API_BASE}/players`);
            console.log('📊 Response status:', response.status);
            console.log('📊 Response ok:', response.ok);
            
            if (response.ok) {
                const data = await response.json();
                console.log('📦 Received data:', data);
                displayPlayers(data.players);
                console.log(`✅ Loaded ${data.players.length} players`);
            } else {
                console.error('❌ API request failed with status:', response.status);
                showError(`Failed to load players (Status: ${response.status})`);
            }
        } catch (error) {
            console.error('💥 Error fetching players:', error);
            showError('Cannot connect to API - Check console for details');
        }
    }
    
    function displayPlayers(players) {
        const tbody = document.getElementById('players-body');
        tbody.innerHTML = '';
        
        if (players.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4">No players found</td></tr>';
            return;
        }
        
        players.forEach((player, index) => {
            const row = document.createElement('tr');
            
            // Highlight top 3 players
            if (index === 0) row.className = 'rank-1';
            else if (index === 1) row.className = 'rank-2';
            else if (index === 2) row.className = 'rank-3';
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${player.id}</td>
                <td>${player.name}</td>
                <td>${player.score}</td>
            `;
            
            tbody.appendChild(row);
        });
        
        // Update stats
        updateStats(players);
    }
    
    function updateStats(players) {
        if (players.length > 0) {
            const avgScore = (players.reduce((sum, p) => sum + p.score, 0) / players.length).toFixed(1);
            const topScore = Math.max(...players.map(p => p.score));
            
            document.getElementById('stats').innerHTML = `
                📊 ${players.length} players | 🎯 Avg: ${avgScore} | 🥇 Top: ${topScore}
            `;
        }
    }
    
    function showError(message) {
        const tbody = document.getElementById('players-body');
        tbody.innerHTML = `<tr><td colspan="4" style="color: red;">❌ ${message}</td></tr>`;
    }
});
```

---

## Part 5: Database Initialization

### 5.1 Create Database Init Script

**💡 Ask Copilot Chat:**
```
Create a MySQL initialization script for a players table with sample data.
```

**📝 Exercise 5:** Create `database/init.sql`:
```sql
-- PlayerApp Database Initialization
USE playerdb;

-- Create players table
CREATE TABLE players (
    id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    score INT NOT NULL CHECK (score >= 0 AND score <= 100)
);

-- Insert 10 sample players
INSERT INTO players (id, name, score) VALUES
(847, 'Player-001', 73),
(293, 'Player-002', 88),
(615, 'Player-003', 42),
(739, 'Player-004', 95),
(162, 'Player-005', 67),
(584, 'Player-006', 81),
(928, 'Player-007', 56),
(371, 'Player-008', 92),
(456, 'Player-009', 34),
(803, 'Player-010', 79);

-- Verify data
SELECT COUNT(*) as total_players FROM players;
SELECT 'PlayerApp database initialized!' as status;
```

---

## Part 6: Deploy and Test Full Stack

### 6.1 Deploy with Docker Compose

**💡 Ask Copilot Chat:**
```
Show me commands to deploy and test a full-stack application with Docker Compose.
```

**📝 Exercise 6:** Deploy the application:
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs
```

### 6.2 Test the Application

**Test each component:**
```bash
# Test database
docker-compose exec database mysql -u player -pplayerpass playerdb -e "SELECT COUNT(*) FROM players;"

# Test backend API
curl http://localhost:5000/players

# Test frontend (open in browser)
# http://localhost:3000
```

**Create simple test script `test.sh`:**
```bash
#!/bin/bash
echo "🧪 Testing PlayerApp Full Stack..."

# Test backend
if curl -s http://localhost:5000/players | grep -q "players"; then
    echo "✅ Backend API working"
else
    echo "❌ Backend API failed"
fi

# Test frontend
if curl -s http://localhost:3000 | grep -q "Player Scoreboard"; then
    echo "✅ Frontend working"
else
    echo "❌ Frontend failed"
fi

# Test database
if docker-compose exec -T database mysql -u player -pplayerpass playerdb -e "SELECT COUNT(*) FROM players;" 2>/dev/null | grep -q "10"; then
    echo "✅ Database working (10 players)"
else
    echo "❌ Database failed"
fi

echo ""
echo "🎉 Full Stack Application Status:"
echo "📊 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000/players"  
echo "🗄️  Database: MySQL with 10 players"
echo ""
echo "✨ Lab 3C Full-Stack Integration: COMPLETE!"
```
else
    echo "❌ Frontend failed"
fi

echo "🎉 Open http://localhost:3000 in your browser!"
```

---

## Part 7: Application Management

### 7.1 Common Commands

**💡 Ask Copilot Chat:**
```
Show me essential Docker Compose commands for managing a multi-container application.
```

**Essential commands:**
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart backend

# View logs
docker-compose logs frontend
docker-compose logs backend
docker-compose logs database

# Rebuild and restart
docker-compose up --build -d

# Clean up everything
docker-compose down --volumes
```

### 7.2 Troubleshooting

**Common issues:**
```bash
# Issue: Backend can't connect to database
# Check: Container networking
docker-compose exec backend ping database

# Issue: Frontend shows API errors
# Check: Backend is running
curl http://localhost:5000/players

# Issue: No data showing
# Check: Database has data
docker-compose exec database mysql -u player -pplayerpass playerdb -e "SELECT * FROM players;"
```

---

## Part 8: Conclusion

### 8.1 What You Built

✅ **Complete PlayerApp Stack** - Frontend + Backend + Database  
✅ **Docker Compose Integration** - All components connected  
✅ **Container Networking** - Services communicate properly  
✅ **Data Flow** - Database → API → Frontend  

### 8.2 Application Architecture

```
┌─────────────┐    HTTP    ┌─────────────┐    SQL     ┌─────────────┐
│  Frontend   │ ---------> │   Backend   │ ---------> │  Database   │
│  (nginx)    │    :3000   │   (Flask)   │    :3306   │   (MySQL)   │
│   Lab 3A    │            │   Lab 3B    │            │ Integrated  │
└─────────────┘            └─────────────┘            └─────────────┘
```

### 8.3 Access Your Application

**🌐 In GitHub Codespaces (IMPORTANT):**

**Method 1: Using Ports Tab (Recommended)**
1. **Look at the bottom panel** in VS Code
2. **Click the "PORTS" tab** (next to Terminal, Problems, etc.)
3. **Find port 3000** in the ports list
4. **Click the globe icon (🌐)** or "Open in Browser" button
5. **This opens in a new browser tab** with the correct HTTPS URL

**Method 2: Manual URL Construction**
If port forwarding isn't automatic, the URLs will be:
- Frontend: `https://your-codespace-name-3000.app.github.dev`
- Backend API: `https://your-codespace-name-5000.app.github.dev/players`

**⚠️ Important Notes:**
- **You CAN use VS Code's Simple Browser** for testing once ports are configured properly
- **The application automatically detects Codespaces** and uses HTTPS URLs for API calls
- **Check browser console** (F12) for debugging information if issues occur
- **Port 5000 MUST be public** for frontend-backend communication
- **Both ports 3000 and 5000** must be forwarded for full functionality

**� CRITICAL: Make Backend Port Public in Codespaces**

**⚠️ IMPORTANT:** For the frontend to communicate with the backend in Codespaces, you **MUST** make port 5000 public:

```bash
# Make port 5000 public (REQUIRED for API communication)
gh codespace ports visibility 5000:public

# Verify port visibility
gh codespace ports
```

**Or manually in VS Code:**
1. Go to **PORTS** tab (next to TERMINAL)
2. Find port **5000** (backend)
3. Right-click → **"Change Port Visibility"** → **"Public"**

**💡 Why This is Required:**
- **Private ports** = Only accessible within Codespaces environment
- **Public ports** = Accessible for cross-origin requests (frontend ↔ backend)
- Without public visibility, you'll see "❌ Cannot connect to API" errors

**�💡 Troubleshooting in Codespaces:**
```bash
# Check if all containers are running
docker-compose ps

# Verify API is accessible (should return JSON)
curl https://your-codespace-name-5000.app.github.dev/players

# Check frontend is serving
curl https://your-codespace-name-3000.app.github.dev

# Test specific endpoint
curl https://your-codespace-name-5000.app.github.dev/
```

### 8.4 Key Commands

```bash
# Deploy everything
docker-compose up -d --build

# Check status
docker-compose ps

# Stop everything
docker-compose down
```

---

*Lab 3C: Full-Stack Integration (with Copilot) - Complete* 🎉

**🎉 Congratulations! You've completed the Week 3 Docker series:**
- **Lab 3A**: Frontend containerization ✅  
- **Lab 3B**: Backend API development ✅
- **Lab 3C**: Full-stack integration ✅

You now have the skills to containerize and deploy complete web applications!