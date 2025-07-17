# 🎮 Lab 4C: Multi-Container Python APIs + Frontend UI with GitHub Actions

## 🧭 Objective

Build a **multi-container system** using Docker Compose with GitHub Copilot assistance, featuring:

- **Two Python Flask APIs**:
  - `player-app-api`: Add new players with random scores
  - `game-api`: Fetch players and retrieve top scores
- **Static HTML + JavaScript frontend** for user interaction
- **Docker orchestration** with `docker-compose.yml` and `entrypoint.sh`
- **GitHub Actions CI workflow** for automated build and validation

---

## 🧱 System Architecture

| Component         | Description                                      | Port |
|------------------|--------------------------------------------------|------|
| `player-app-api` | REST API to add players with ID and random score | 5000 |
| `game-api`       | REST API to get all players and top 3 scorers    | 5001 |
| `frontend/`      | JavaScript UI to interact with both APIs         | 8080 |
| `entrypoint.sh`  | Orchestrates local startup using Docker          | -    |
| GitHub Actions   | Builds, tests, and validates the entire system   | -    |

---

## 🎯 Learning Objectives

- Build multiple Python Flask APIs with **GitHub Copilot**
- Implement **inter-service communication** between APIs
- Use **Docker Compose** for multi-container orchestration
- Create a **frontend** that consumes multiple backend services
- Set up **CI/CD pipeline** for containerized applications
- Practice **service discovery** and **container networking**

---

## 📁 Folder Structure

```
lab4c-multicontainer/
├── player-app-api/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── game-api/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   └── Dockerfile
├── entrypoint.sh
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml
```

---

## ✅ Step 1: Create Player App API

### 1.1 Create `player-app-api/app.py`

> *Copilot Prompt:\
> Create a Flask API in `player-app-api/app.py` with:\
> - A global `players` list to store player data\
> - POST `/add` endpoint that accepts JSON with player name\
> - Auto-generates player ID as "Player-001", "Player-002", etc.\
> - Assigns random score between 0-100\
> - Returns the created player as JSON\
> - GET `/players` endpoint to return all players\
> - Runs on host 0.0.0.0 port 5000*

**✅ Expected Outcome:**

```python
from flask import Flask, request, jsonify
import random

app = Flask(__name__)
players = []

@app.route('/add', methods=['POST'])
def add_player():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    player_id = f"Player-{len(players)+1:03d}"
    score = random.randint(0, 100)
    player = {
        "id": player_id,
        "name": data["name"],
        "score": score
    }
    players.append(player)
    return jsonify(player), 201

@app.route('/players', methods=['GET'])
def get_players():
    return jsonify(players)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "players_count": len(players)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 1.2 Create `player-app-api/requirements.txt`

```txt
Flask==2.3.3
```

### 1.3 Create `player-app-api/Dockerfile`

> *Copilot Prompt:\
> Create a Dockerfile for the Flask app that:\
> - Uses python:3.9-slim as base image\
> - Sets working directory to /app\
> - Copies requirements.txt and installs dependencies\
> - Copies app.py\
> - Exposes port 5000\
> - Runs the Flask app*

**✅ Expected Outcome:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## ✅ Step 2: Create Game API

### 2.1 Create `game-api/app.py`

> *Copilot Prompt:\
> Create a Flask API in `game-api/app.py` that:\
> - Makes HTTP requests to player-app-api to get player data\
> - GET `/players` endpoint that fetches from http://player-app-api:5000/players\
> - GET `/top3` endpoint that gets players and returns top 3 by score\
> - GET `/health` endpoint for health checks\
> - Includes proper error handling for API calls\
> - Runs on host 0.0.0.0 port 5000*

**✅ Expected Outcome:**

```python
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Service discovery - use environment variable or default
PLAYER_API_URL = os.getenv('PLAYER_API_URL', 'http://player-app-api:5000')

@app.route('/players', methods=['GET'])
def get_all_players():
    try:
        response = requests.get(f'{PLAYER_API_URL}/players', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch players: {str(e)}"}), 500

@app.route('/top3', methods=['GET'])
def get_top_players():
    try:
        response = requests.get(f'{PLAYER_API_URL}/players', timeout=5)
        response.raise_for_status()
        players = response.json()
        
        if not players:
            return jsonify([])
        
        # Sort by score descending and take top 3
        top_players = sorted(players, key=lambda p: p['score'], reverse=True)[:3]
        return jsonify(top_players)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to compute top 3: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    try:
        # Check if player-app-api is reachable
        response = requests.get(f'{PLAYER_API_URL}/health', timeout=3)
        player_api_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        player_api_status = "unreachable"
    
    return jsonify({
        "status": "healthy",
        "player_api_status": player_api_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 2.2 Create `game-api/requirements.txt`

```txt
Flask==2.3.3
requests==2.31.0
```

### 2.3 Create `game-api/Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## ✅ Step 3: Create Frontend UI

### 3.1 Create `frontend/index.html`

> *Copilot Prompt:\
> Create an HTML file with JavaScript that:\
> - Has a clean, modern UI with CSS styling\
> - Input field for player name and "Add Player" button\
> - Buttons for "Show All Players" and "Top 3"\
> - Results display area with formatted JSON\
> - Calls APIs at localhost:5000 (player-app) and localhost:5001 (game-api)\
> - Includes error handling and loading states*

**✅ Expected Outcome:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Game Leaderboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .input-section {
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            background: #4CAF50;
            color: white;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        button:hover {
            background: #45a049;
        }
        button:disabled {
            background: #cccccc;
            cursor: not-allowed;
        }
        .actions {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .output {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            min-height: 200px;
            overflow-y: auto;
        }
        .loading {
            color: #ffd700;
        }
        .error {
            color: #ff6b6b;
        }
        .success {
            color: #51cf66;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 Game Leaderboard</h1>
        
        <div class="input-section">
            <input type="text" id="playerName" placeholder="Enter player name..." />
            <button onclick="addPlayer()">Add Player</button>
        </div>
        
        <div class="actions">
            <button onclick="getAllPlayers()">Show All Players</button>
            <button onclick="getTopPlayers()">Top 3 Players</button>
            <button onclick="checkHealth()">Health Check</button>
        </div>
        
        <div class="output" id="output">Welcome! Add some players to get started...</div>
    </div>

    <script>
        const playerAPI = "http://localhost:5000";
        const gameAPI = "http://localhost:5001";
        const output = document.getElementById('output');

        function displayResult(data, type = 'info') {
            output.className = `output ${type}`;
            output.textContent = JSON.stringify(data, null, 2);
        }

        function displayLoading(message) {
            output.className = 'output loading';
            output.textContent = `Loading... ${message}`;
        }

        async function addPlayer() {
            const name = document.getElementById('playerName').value.trim();
            if (!name) {
                displayResult({error: "Please enter a player name"}, 'error');
                return;
            }

            try {
                displayLoading('Adding player...');
                const response = await fetch(`${playerAPI}/add`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name })
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                displayResult(data, 'success');
                document.getElementById('playerName').value = '';
            } catch (error) {
                displayResult({error: `Failed to add player: ${error.message}`}, 'error');
            }
        }

        async function getAllPlayers() {
            try {
                displayLoading('Fetching all players...');
                const response = await fetch(`${gameAPI}/players`);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                displayResult(data, 'success');
            } catch (error) {
                displayResult({error: `Failed to fetch players: ${error.message}`}, 'error');
            }
        }

        async function getTopPlayers() {
            try {
                displayLoading('Fetching top 3 players...');
                const response = await fetch(`${gameAPI}/top3`);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                displayResult(data, 'success');
            } catch (error) {
                displayResult({error: `Failed to fetch top players: ${error.message}`}, 'error');
            }
        }

        async function checkHealth() {
            try {
                displayLoading('Checking service health...');
                
                const [playerHealth, gameHealth] = await Promise.allSettled([
                    fetch(`${playerAPI}/health`),
                    fetch(`${gameAPI}/health`)
                ]);

                const healthStatus = {
                    player_api: playerHealth.status === 'fulfilled' && playerHealth.value.ok ? 'healthy' : 'unhealthy',
                    game_api: gameHealth.status === 'fulfilled' && gameHealth.value.ok ? 'healthy' : 'unhealthy',
                    timestamp: new Date().toISOString()
                };

                displayResult(healthStatus, healthStatus.player_api === 'healthy' && healthStatus.game_api === 'healthy' ? 'success' : 'error');
            } catch (error) {
                displayResult({error: `Health check failed: ${error.message}`}, 'error');
            }
        }

        // Allow Enter key to add player
        document.getElementById('playerName').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addPlayer();
            }
        });
    </script>
</body>
</html>
```

### 3.2 Create `frontend/Dockerfile`

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## ✅ Step 4: Docker Orchestration

### 4.1 Create `docker-compose.yml`

> *Copilot Prompt:\
> Create a docker-compose.yml file that:\
> - Defines services for player-app, game-api, and frontend\
> - Maps appropriate ports (5000, 5001, 8080)\
> - Sets up service dependencies\
> - Includes environment variables for service URLs\
> - Uses build context for each service*

**✅ Expected Outcome:**

```yaml
version: '3.8'

services:
  player-app-api:
    build: ./player-app-api
    container_name: player-app-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - game-network

  game-api:
    build: ./game-api
    container_name: game-api
    ports:
      - "5001:5000"
    environment:
      - FLASK_ENV=development
      - PLAYER_API_URL=http://player-app-api:5000
    depends_on:
      player-app-api:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - game-network

  frontend:
    build: ./frontend
    container_name: frontend
    ports:
      - "8080:80"
    depends_on:
      - player-app-api
      - game-api
    networks:
      - game-network

networks:
  game-network:
    driver: bridge
```

### 4.2 Create `entrypoint.sh`

> *Copilot Prompt:\
> Create an entrypoint.sh script that:\
> - Makes the script executable\
> - Builds and starts all containers using docker-compose\
> - Shows container status\
> - Provides useful information about accessing the services*

**✅ Expected Outcome:**

```bash
#!/bin/bash

# Multi-Container Game System Entrypoint
echo "🎮 Starting Multi-Container Game System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down --remove-orphans

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
echo "Player API Health:"
curl -s http://localhost:5000/health | python3 -m json.tool 2>/dev/null || echo "❌ Player API not ready"

echo -e "\nGame API Health:"
curl -s http://localhost:5001/health | python3 -m json.tool 2>/dev/null || echo "❌ Game API not ready"

# Display service information
echo -e "\n✅ Services started successfully!"
echo "📊 Access the application:"
echo "  🌐 Frontend UI: http://localhost:8080"
echo "  🎯 Player API: http://localhost:5000"
echo "  🎮 Game API: http://localhost:5001"
echo ""
echo "📝 Available endpoints:"
echo "  POST http://localhost:5000/add - Add a player"
echo "  GET  http://localhost:5000/players - Get all players"
echo "  GET  http://localhost:5001/players - Get all players (via game API)"
echo "  GET  http://localhost:5001/top3 - Get top 3 players"
echo ""
echo "🔍 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
```

---

## ✅ Step 5: GitHub Actions CI/CD

### 5.1 Create `.github/workflows/ci.yml`

> *Copilot Prompt:\
> Create a GitHub Actions workflow that:\
> - Triggers on push to main branch\
> - Uses ubuntu-latest runner\
> - Checks out code\
> - Builds all containers using docker-compose\
> - Tests that all services are healthy\
> - Validates API endpoints with curl\
> - Includes proper error handling and timeouts*

**✅ Expected Outcome:**

```yaml
name: Multi-Container Python APIs CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Build and start services
      run: |
        docker-compose up --build -d
        echo "✅ Services started"

    - name: Wait for services to be ready
      run: |
        echo "⏳ Waiting for services to start..."
        sleep 30
        
        # Check if containers are running
        docker-compose ps
        
        # Wait for health checks
        timeout=60
        while [ $timeout -gt 0 ]; do
          if curl -f http://localhost:5000/health && curl -f http://localhost:5001/health; then
            echo "✅ All services are healthy"
            break
          fi
          echo "⏳ Waiting for services... ($timeout seconds remaining)"
          sleep 5
          timeout=$((timeout-5))
        done
        
        if [ $timeout -le 0 ]; then
          echo "❌ Services failed to start within timeout"
          docker-compose logs
          exit 1
        fi

    - name: Test Player API
      run: |
        echo "🧪 Testing Player API..."
        
        # Test health endpoint
        curl -f http://localhost:5000/health
        
        # Test adding a player
        response=$(curl -s -X POST http://localhost:5000/add \
          -H "Content-Type: application/json" \
          -d '{"name":"TestPlayer"}')
        echo "Add player response: $response"
        
        # Test getting players
        players=$(curl -s http://localhost:5000/players)
        echo "Players: $players"
        
        # Verify player was added
        if echo "$players" | grep -q "TestPlayer"; then
          echo "✅ Player API tests passed"
        else
          echo "❌ Player API tests failed"
          exit 1
        fi

    - name: Test Game API
      run: |
        echo "🧪 Testing Game API..."
        
        # Test health endpoint
        curl -f http://localhost:5001/health
        
        # Test getting players through game API
        players=$(curl -s http://localhost:5001/players)
        echo "Game API players: $players"
        
        # Test top 3 endpoint
        top3=$(curl -s http://localhost:5001/top3)
        echo "Top 3 players: $top3"
        
        # Verify responses contain expected data
        if echo "$players" | grep -q "TestPlayer" && echo "$top3" | grep -q "score"; then
          echo "✅ Game API tests passed"
        else
          echo "❌ Game API tests failed"
          exit 1
        fi

    - name: Test Frontend
      run: |
        echo "🧪 Testing Frontend..."
        
        # Test that frontend is serving content
        response=$(curl -s http://localhost:8080)
        if echo "$response" | grep -q "Game Leaderboard"; then
          echo "✅ Frontend tests passed"
        else
          echo "❌ Frontend tests failed"
          exit 1
        fi

    - name: View service logs
      if: failure()
      run: |
        echo "📋 Service logs for debugging:"
        docker-compose logs --tail=50

    - name: Clean up
      if: always()
      run: |
        docker-compose down
        docker system prune -f
```

---

## ✅ Step 6: Testing and Validation

### 6.1 Local Testing Commands

```bash
# Start the entire system
chmod +x entrypoint.sh
./entrypoint.sh

# Test Player API
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice"}'

curl http://localhost:5000/players

# Test Game API
curl http://localhost:5001/players
curl http://localhost:5001/top3

# Check health
curl http://localhost:5000/health
curl http://localhost:5001/health

# Stop system
docker-compose down
```

### 6.2 Frontend Testing

1. Open http://localhost:8080 in your browser
2. Add several players using the form
3. Click "Show All Players" to see the list
4. Click "Top 3 Players" to see the leaderboard
5. Use "Health Check" to verify services are running

---

## ✅ Summary Table

| Task                    | Technology                | ✅ Expected Outcome                   |
|-------------------------|---------------------------|--------------------------------------|
| Player API              | Python Flask + Docker    | REST API for adding players          |
| Game API                | Python Flask + Requests  | API aggregation and top scores       |
| Frontend UI             | HTML + JavaScript + Nginx| Interactive web interface            |
| Container Orchestration | Docker Compose           | Multi-service coordination           |
| Service Communication   | HTTP + Docker Networks    | Inter-container API calls            |
| CI/CD Pipeline          | GitHub Actions           | Automated testing and validation     |
| Local Development       | entrypoint.sh             | One-command system startup           |

---

## 🎓 Learning Outcomes

By completing this lab, students will have mastered:

### **Technical Skills**
- **Python Flask**: RESTful API development, request handling, service integration
- **Docker**: Multi-container applications, networking, health checks
- **Service Architecture**: Microservices communication, API aggregation patterns
- **Frontend Integration**: JavaScript API consumption, error handling, user experience
- **DevOps**: Container orchestration, CI/CD pipelines, automated testing

### **Professional Concepts**
- **System Design**: Multi-service architecture, service discovery, dependency management
- **Testing Strategies**: API testing, integration testing, health check patterns
- **Deployment Automation**: Infrastructure as code, automated builds and deployments
- **Monitoring**: Service health, logging, debugging containerized applications

This lab provides hands-on experience with modern microservices architecture and containerized application development! 🚀
