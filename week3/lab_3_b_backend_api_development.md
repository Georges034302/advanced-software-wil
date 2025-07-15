# Lab 3B: Backend API Development - Simple Player API

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
- Use GitHub Copilot to create a simple Flask REST API
- Containerize a Python backend application
- Connect frontend to backend API
- Test API endpoints

## 📋 Prerequisites
- Completion of Lab 3A (Frontend Containerization)
- Basic Python knowledge

---

## Part 1: Use Copilot to Create a Simple Player API

### 1.1 Project Setup

**📝 Create project folder:**
```bash
mkdir playerapp-backend
cd playerapp-backend
```

### 1.2 Generate Flask API with Copilot

**💡 Ask Copilot Chat:**
```
Create a simple Flask API with endpoints to get all players and get player by ID. Use sample player data with ID (3 digits), name (Player-XXXXXX), and score (0-100). Include CORS for frontend connection.
```

**📝 Exercise 1:** Create `app.py`:
```python
from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Sample players data
players = []

def generate_players():
    global players
    players = []
    for i in range(10):
        players.append({
            'id': random.randint(100, 999),
            'name': f"Player-{random.randint(100, 999)}",
            'score': random.randint(0, 100)
        })

@app.route('/')
def home():
    return jsonify({"message": "Player API is running!", "endpoints": ["/players", "/players/<id>"]})

@app.route('/players', methods=['GET'])
def get_players():
    sorted_players = sorted(players, key=lambda x: x['score'], reverse=True)
    return jsonify({"players": sorted_players})

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = next((p for p in players if p['id'] == player_id), None)
    if player:
        return jsonify({"player": player})
    else:
        return jsonify({"error": "Player not found"}), 404

if __name__ == '__main__':
    generate_players()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 1.3 Generate Requirements with Copilot

**💡 Ask Copilot Chat:**
```
Create a requirements.txt file for a simple Flask API with CORS support.
```

**📝 Exercise 2:** Create `requirements.txt`:
```txt
Flask==2.3.3
Flask-CORS==4.0.0
```

**📝 Test:** 
1. Run `python app.py` 
2. Check the **Ports tab** in VS Code
3. **Click "Open in Browser"** for port 5000
4. Add `/players` to the URL to test the endpoint

---

## Part 2: Containerize with Docker (using Copilot)

### 2.1 Create Dockerfile with Copilot

**💡 Ask Copilot Chat:**
```
Create a simple Dockerfile for a Flask Python application. Keep it minimal.
```

**📝 Exercise 3:** Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

**📝 Exercise 4:** Build and run with Docker commands from Copilot
```bash
# Build the image
docker build -t player-api .

# Run the container
docker run -d --name player-backend -p 5000:5000 player-api

# Check if it's running
docker ps
```

---

## Part 3: Test in Codespaces

### 3.1 Access Your API

**💡 In Codespaces:**
1. **Ports tab** shows port 5000
2. **Click "Open in Browser"**
3. **Test endpoints**: `/` and `/players`

**📝 Exercise 5:** Test your containerized API

### 3.2 Test with Commands

**💡 Ask Copilot for API testing commands:**
```
Show me curl commands to test a player API with endpoints for all players and single player.
```

**📝 Exercise 6:** Test API endpoints in terminal:
```bash
# Test API endpoints (works in Codespaces terminal)
curl http://localhost:5000/
curl http://localhost:5000/players
curl http://localhost:5000/players/123
```

**💡 Alternative:** Use browser with port forwarding URLs from Ports tab

---

## Part 4: Connect to Frontend (Optional)

### 4.1 Update Frontend to Use API

**💡 Ask Copilot Chat:**
```
Update JavaScript to fetch data from API instead of generating local data. Add error handling for when API is not available.
```

**📝 Exercise 6:** Add to your frontend `app.js`:
```javascript
async function fetchPlayersFromAPI() {
    try {
        const response = await fetch('http://localhost:5000/players');
        const data = await response.json();
        return data.players;
    } catch (error) {
        console.log('API not available, using local data');
        return generatePlayers();
    }
}

// Update generatePlayers function
async function generatePlayers() {
    const players = await fetchPlayersFromAPI();
    document.getElementById('players').innerHTML = players
        .map(p => `<div class="player">ID: ${p.id} | ${p.name} | Score: ${p.score}</div>`)
        .join('');
}
```

---

## Part 5: Conclusion

✅ **Used Copilot effectively** - Generated Flask API, Dockerfile, and commands  
✅ **Created simple REST API** - Two endpoints for player data  
✅ **Containerized the API** - Built and ran with Docker  
✅ **Connected frontend to backend** - API integration with error handling  


**🔮 Next:** Lab 3C - Full-Stack Integration with Docker Compose!

---

*Lab 3B: Backend API Development (with Copilot) - Complete* 🎉