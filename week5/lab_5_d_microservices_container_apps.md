# ☁️ Lab 5D: Microservices with Azure Container Apps

## 🎯 Objective
Deploy a distributed microservices application with 2 Python services and a frontend to Azure Container Apps.

**Cool Services Architecture:**
- 🎲 **Dice Service**: Random number generation with statistics
- 🎨 **Color Service**: Generate color palettes and hex codes
- 🌐 **Frontend**: Interactive dashboard making API calls to both services

## 🗂 Structure
```
lab5d/
├── services/
│   ├── dice-service/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── color-service/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── frontend/
│       ├── index.html
│       ├── app.js
│       ├── styles.css
│       └── Dockerfile
├── scripts/
│   ├── build-all.sh
│   ├── deploy-microservices.sh
│   └── cleanup-microservices.sh
└── .env (from Lab 5A)
```

## ✅ Step 1: Create Dice Service

### `services/dice-service/app.py`
```python
from flask import Flask, jsonify
import random
import time
from collections import defaultdict

app = Flask(__name__)

# In-memory stats storage
roll_stats = defaultdict(int)
total_rolls = 0

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "dice-service"})

@app.route('/roll')
def roll_dice():
    global total_rolls
    sides = 6
    result = random.randint(1, sides)
    
    # Update stats
    roll_stats[result] += 1
    total_rolls += 1
    
    return jsonify({
        "roll": result,
        "timestamp": int(time.time()),
        "total_rolls": total_rolls
    })

@app.route('/roll/<int:sides>')
def roll_custom_dice(sides):
    global total_rolls
    if sides < 2 or sides > 100:
        return jsonify({"error": "Sides must be between 2 and 100"}), 400
    
    result = random.randint(1, sides)
    total_rolls += 1
    
    return jsonify({
        "roll": result,
        "sides": sides,
        "timestamp": int(time.time()),
        "total_rolls": total_rolls
    })

@app.route('/stats')
def get_stats():
    return jsonify({
        "total_rolls": total_rolls,
        "distribution": dict(roll_stats),
        "service": "dice-service"
    })

@app.route('/')
def root():
    return jsonify({
        "service": "dice-service",
        "endpoints": ["/roll", "/roll/<sides>", "/stats", "/health"],
        "description": "Random dice rolling with statistics"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### `services/dice-service/requirements.txt`
```
Flask==2.3.3
```

### `services/dice-service/Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 5000

CMD ["python", "app.py"]
```

## ✅ Step 2: Create Color Service

### `services/color-service/app.py`
```python
from flask import Flask, jsonify
import random
import colorsys

app = Flask(__name__)

# Predefined color themes
COLOR_THEMES = {
    "ocean": ["#006994", "#0582CA", "#00A6FB", "#B3E5FC", "#E1F5FE"],
    "sunset": ["#FF6B35", "#F7931E", "#FFD23F", "#FFF1B8", "#FFB5A7"],
    "forest": ["#2D5016", "#4F772D", "#90A955", "#C7E9B4", "#E8F5E8"],
    "cosmic": ["#240046", "#3C096C", "#5A189A", "#7B2CBF", "#9D4EDD"],
    "vintage": ["#8B4513", "#D2691E", "#F4A460", "#DEB887", "#F5E6D3"]
}

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "color-service"})

@app.route('/random')
def random_color():
    """Generate a random hex color"""
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return jsonify({
        "hex": color,
        "rgb": hex_to_rgb(color),
        "name": get_color_name(color)
    })

@app.route('/palette/<int:count>')
def generate_palette(count):
    """Generate a palette of N colors"""
    if count < 1 or count > 10:
        return jsonify({"error": "Count must be between 1 and 10"}), 400
    
    palette = []
    for _ in range(count):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        palette.append({
            "hex": color,
            "rgb": hex_to_rgb(color)
        })
    
    return jsonify({
        "palette": palette,
        "count": count,
        "theme": "random"
    })

@app.route('/theme/<theme_name>')
def get_theme(theme_name):
    """Get a predefined color theme"""
    if theme_name not in COLOR_THEMES:
        return jsonify({
            "error": f"Theme '{theme_name}' not found",
            "available_themes": list(COLOR_THEMES.keys())
        }), 404
    
    colors = COLOR_THEMES[theme_name]
    palette = []
    
    for color in colors:
        palette.append({
            "hex": color,
            "rgb": hex_to_rgb(color)
        })
    
    return jsonify({
        "theme": theme_name,
        "palette": palette,
        "count": len(palette)
    })

@app.route('/themes')
def list_themes():
    """List all available themes"""
    return jsonify({
        "themes": list(COLOR_THEMES.keys()),
        "count": len(COLOR_THEMES)
    })

@app.route('/')
def root():
    return jsonify({
        "service": "color-service",
        "endpoints": ["/random", "/palette/<count>", "/theme/<name>", "/themes", "/health"],
        "description": "Color palette generation service"
    })

def hex_to_rgb(hex_color):
    """Convert hex to RGB"""
    hex_color = hex_color.lstrip('#')
    return {
        "r": int(hex_color[0:2], 16),
        "g": int(hex_color[2:4], 16),
        "b": int(hex_color[4:6], 16)
    }

def get_color_name(hex_color):
    """Simple color name approximation"""
    rgb = hex_to_rgb(hex_color)
    r, g, b = rgb["r"], rgb["g"], rgb["b"]
    
    if r > 200 and g > 200 and b > 200:
        return "light"
    elif r < 50 and g < 50 and b < 50:
        return "dark"
    elif r > g and r > b:
        return "red-ish"
    elif g > r and g > b:
        return "green-ish"
    elif b > r and b > g:
        return "blue-ish"
    else:
        return "neutral"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### `services/color-service/requirements.txt`
```
Flask==2.3.3
```

### `services/color-service/Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 5000

CMD ["python", "app.py"]
```

## ✅ Step 3: Create Frontend

### `services/frontend/index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microservices Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🎲🎨 Microservices Dashboard</h1>
            <p>Independent API calls to Dice and Color services</p>
        </header>

        <div class="services-grid">
            <!-- Dice Service Section -->
            <div class="service-card">
                <h2>🎲 Dice Service</h2>
                <div class="controls">
                    <button onclick="rollDice()">Roll Dice (6-sided)</button>
                    <input type="number" id="diceInput" placeholder="Sides (2-100)" min="2" max="100">
                    <button onclick="rollCustomDice()">Roll Custom</button>
                    <button onclick="getDiceStats()">Get Stats</button>
                </div>
                <div id="diceResult" class="result"></div>
            </div>

            <!-- Color Service Section -->
            <div class="service-card">
                <h2>🎨 Color Service</h2>
                <div class="controls">
                    <button onclick="getRandomColor()">Random Color</button>
                    <input type="number" id="paletteInput" placeholder="Palette size (1-10)" min="1" max="10">
                    <button onclick="generatePalette()">Generate Palette</button>
                    <select id="themeSelect">
                        <option value="">Select Theme...</option>
                        <option value="ocean">Ocean</option>
                        <option value="sunset">Sunset</option>
                        <option value="forest">Forest</option>
                        <option value="cosmic">Cosmic</option>
                        <option value="vintage">Vintage</option>
                    </select>
                    <button onclick="getTheme()">Get Theme</button>
                </div>
                <div id="colorResult" class="result"></div>
            </div>
        </div>

        <div class="status-bar">
            <div id="statusDice" class="status">Dice Service: <span class="status-indicator">🔴</span></div>
            <div id="statusColor" class="status">Color Service: <span class="status-indicator">🔴</span></div>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>
```

### `services/frontend/styles.css`
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 40px;
    color: white;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.services-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 30px;
}

.service-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.service-card:hover {
    transform: translateY(-5px);
}

.service-card h2 {
    margin-bottom: 20px;
    color: #5a67d8;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 10px;
}

.controls {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
}

button {
    background: #5a67d8;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s ease;
}

button:hover {
    background: #4c51bf;
}

input, select {
    padding: 10px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 14px;
}

input:focus, select:focus {
    outline: none;
    border-color: #5a67d8;
}

.result {
    background: #f7fafc;
    border-radius: 8px;
    padding: 15px;
    min-height: 100px;
    border-left: 4px solid #5a67d8;
}

.color-preview {
    display: inline-block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 5px;
    border: 2px solid #ddd;
    vertical-align: middle;
}

.status-bar {
    display: flex;
    justify-content: center;
    gap: 40px;
    background: rgba(255,255,255,0.9);
    padding: 15px;
    border-radius: 10px;
}

.status {
    font-weight: 600;
}

.status-indicator {
    font-size: 12px;
}

@media (max-width: 768px) {
    .services-grid {
        grid-template-columns: 1fr;
    }
    
    .controls {
        flex-direction: column;
    }
    
    header h1 {
        font-size: 2rem;
    }
}
```

### `services/frontend/app.js`
```javascript
// Configuration - these will be replaced by actual service URLs
let DICE_SERVICE_URL = 'DICE_SERVICE_URL_PLACEHOLDER';
let COLOR_SERVICE_URL = 'COLOR_SERVICE_URL_PLACEHOLDER';

// Check if we're running locally or need to use environment
if (DICE_SERVICE_URL === 'DICE_SERVICE_URL_PLACEHOLDER') {
    // For local development
    DICE_SERVICE_URL = 'http://localhost:5001';
    COLOR_SERVICE_URL = 'http://localhost:5002';
}

// Service health checking
async function checkServiceHealth() {
    try {
        const diceResponse = await fetch(`${DICE_SERVICE_URL}/health`);
        const diceStatus = document.querySelector('#statusDice .status-indicator');
        diceStatus.textContent = diceResponse.ok ? '🟢' : '🔴';
    } catch (error) {
        document.querySelector('#statusDice .status-indicator').textContent = '🔴';
    }

    try {
        const colorResponse = await fetch(`${COLOR_SERVICE_URL}/health`);
        const colorStatus = document.querySelector('#statusColor .status-indicator');
        colorStatus.textContent = colorResponse.ok ? '🟢' : '🔴';
    } catch (error) {
        document.querySelector('#statusColor .status-indicator').textContent = '🔴';
    }
}

// Dice Service Functions
async function rollDice() {
    try {
        const response = await fetch(`${DICE_SERVICE_URL}/roll`);
        const data = await response.json();
        
        document.getElementById('diceResult').innerHTML = `
            <h3>🎲 Dice Roll Result</h3>
            <p><strong>Result:</strong> ${data.roll}</p>
            <p><strong>Total Rolls:</strong> ${data.total_rolls}</p>
            <p><strong>Timestamp:</strong> ${new Date(data.timestamp * 1000).toLocaleTimeString()}</p>
        `;
    } catch (error) {
        document.getElementById('diceResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

async function rollCustomDice() {
    const sides = document.getElementById('diceInput').value;
    if (!sides) {
        alert('Please enter number of sides (2-100)');
        return;
    }

    try {
        const response = await fetch(`${DICE_SERVICE_URL}/roll/${sides}`);
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('diceResult').innerHTML = `
                <h3>🎲 Custom Dice Roll</h3>
                <p><strong>Result:</strong> ${data.roll} (${data.sides}-sided)</p>
                <p><strong>Total Rolls:</strong> ${data.total_rolls}</p>
                <p><strong>Timestamp:</strong> ${new Date(data.timestamp * 1000).toLocaleTimeString()}</p>
            `;
        } else {
            document.getElementById('diceResult').innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('diceResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

async function getDiceStats() {
    try {
        const response = await fetch(`${DICE_SERVICE_URL}/stats`);
        const data = await response.json();
        
        let distributionHtml = '';
        for (const [number, count] of Object.entries(data.distribution)) {
            distributionHtml += `<p>${number}: ${count} times</p>`;
        }
        
        document.getElementById('diceResult').innerHTML = `
            <h3>📊 Dice Statistics</h3>
            <p><strong>Total Rolls:</strong> ${data.total_rolls}</p>
            <div><strong>Distribution:</strong><br>${distributionHtml || 'No rolls yet'}</div>
        `;
    } catch (error) {
        document.getElementById('diceResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

// Color Service Functions
async function getRandomColor() {
    try {
        const response = await fetch(`${COLOR_SERVICE_URL}/random`);
        const data = await response.json();
        
        document.getElementById('colorResult').innerHTML = `
            <h3>🎨 Random Color</h3>
            <div class="color-preview" style="background-color: ${data.hex}"></div>
            <p><strong>Hex:</strong> ${data.hex}</p>
            <p><strong>RGB:</strong> rgb(${data.rgb.r}, ${data.rgb.g}, ${data.rgb.b})</p>
            <p><strong>Name:</strong> ${data.name}</p>
        `;
    } catch (error) {
        document.getElementById('colorResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

async function generatePalette() {
    const count = document.getElementById('paletteInput').value;
    if (!count) {
        alert('Please enter palette size (1-10)');
        return;
    }

    try {
        const response = await fetch(`${COLOR_SERVICE_URL}/palette/${count}`);
        const data = await response.json();
        
        if (response.ok) {
            let paletteHtml = '<h3>🎨 Generated Palette</h3><div>';
            data.palette.forEach(color => {
                paletteHtml += `
                    <div style="display: inline-block; margin: 5px; text-align: center;">
                        <div class="color-preview" style="background-color: ${color.hex}"></div>
                        <small>${color.hex}</small>
                    </div>
                `;
            });
            paletteHtml += '</div>';
            
            document.getElementById('colorResult').innerHTML = paletteHtml;
        } else {
            document.getElementById('colorResult').innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('colorResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

async function getTheme() {
    const theme = document.getElementById('themeSelect').value;
    if (!theme) {
        alert('Please select a theme');
        return;
    }

    try {
        const response = await fetch(`${COLOR_SERVICE_URL}/theme/${theme}`);
        const data = await response.json();
        
        if (response.ok) {
            let themeHtml = `<h3>🎨 ${data.theme.toUpperCase()} Theme</h3><div>`;
            data.palette.forEach(color => {
                themeHtml += `
                    <div style="display: inline-block; margin: 5px; text-align: center;">
                        <div class="color-preview" style="background-color: ${color.hex}"></div>
                        <small>${color.hex}</small>
                    </div>
                `;
            });
            themeHtml += '</div>';
            
            document.getElementById('colorResult').innerHTML = themeHtml;
        } else {
            document.getElementById('colorResult').innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('colorResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    checkServiceHealth();
    setInterval(checkServiceHealth, 30000); // Check health every 30 seconds
});
```

### `services/frontend/Dockerfile`
```dockerfile
FROM nginx:alpine

# Copy static files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Create nginx config for SPA
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
```

## ✅ Step 4: Build Scripts

### `scripts/build-all.sh`
```bash
#!/bin/bash
set -e

echo "🏗️ Building all microservices"
source .env

# Build dice service
echo "📦 Building dice service..."
cd services/dice-service
docker build -t $ACR_NAME.azurecr.io/dice-service:latest .
docker push $ACR_NAME.azurecr.io/dice-service:latest
cd ../..

# Build color service
echo "🎨 Building color service..."
cd services/color-service
docker build -t $ACR_NAME.azurecr.io/color-service:latest .
docker push $ACR_NAME.azurecr.io/color-service:latest
cd ../..

# Build frontend
echo "🌐 Building frontend..."
cd services/frontend
docker build -t $ACR_NAME.azurecr.io/frontend:latest .
docker push $ACR_NAME.azurecr.io/frontend:latest
cd ../..

echo "✅ All services built and pushed to ACR"
```

### `scripts/deploy-microservices.sh`
```bash
#!/bin/bash
set -e

echo "🚀 Deploying microservices to Azure Container Apps"
source .env

# Container Apps environment
CONTAINERAPP_ENV="microservices-env-lab5d"

echo "📦 Creating Container Apps environment..."
az containerapp env create \
  --name $CONTAINERAPP_ENV \
  --resource-group $RG_NAME \
  --location $LOCATION

# Deploy Dice Service
echo "🎲 Deploying Dice Service..."
az containerapp create \
  --name dice-service \
  --resource-group $RG_NAME \
  --environment $CONTAINERAPP_ENV \
  --image $ACR_NAME.azurecr.io/dice-service:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 5000 \
  --ingress external \
  --cpu 0.25 \
  --memory 0.5Gi \
  --min-replicas 1 \
  --max-replicas 5

# Deploy Color Service
echo "🎨 Deploying Color Service..."
az containerapp create \
  --name color-service \
  --resource-group $RG_NAME \
  --environment $CONTAINERAPP_ENV \
  --image $ACR_NAME.azurecr.io/color-service:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 5000 \
  --ingress external \
  --cpu 0.25 \
  --memory 0.5Gi \
  --min-replicas 1 \
  --max-replicas 5

# Get service URLs
DICE_URL=$(az containerapp show \
  --name dice-service \
  --resource-group $RG_NAME \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

COLOR_URL=$(az containerapp show \
  --name color-service \
  --resource-group $RG_NAME \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

# Update frontend with service URLs
echo "🌐 Updating frontend configuration..."
cd services/frontend
sed -i "s|DICE_SERVICE_URL_PLACEHOLDER|https://$DICE_URL|g" app.js
sed -i "s|COLOR_SERVICE_URL_PLACEHOLDER|https://$COLOR_URL|g" app.js

# Rebuild and push updated frontend
docker build -t $ACR_NAME.azurecr.io/frontend:latest .
docker push $ACR_NAME.azurecr.io/frontend:latest
cd ../..

# Deploy Frontend
echo "🌐 Deploying Frontend..."
az containerapp create \
  --name frontend \
  --resource-group $RG_NAME \
  --environment $CONTAINERAPP_ENV \
  --image $ACR_NAME.azurecr.io/frontend:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 80 \
  --ingress external \
  --cpu 0.25 \
  --memory 0.5Gi \
  --min-replicas 1 \
  --max-replicas 3

# Get frontend URL
FRONTEND_URL=$(az containerapp show \
  --name frontend \
  --resource-group $RG_NAME \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

# Save URLs to environment
echo "export CONTAINERAPP_ENV=$CONTAINERAPP_ENV" >> .env
echo "export DICE_URL=$DICE_URL" >> .env
echo "export COLOR_URL=$COLOR_URL" >> .env
echo "export FRONTEND_URL=$FRONTEND_URL" >> .env

# Store in GitHub secrets
if command -v gh &> /dev/null; then
    gh auth logout --hostname github.com || true
    
    if [[ -n "$GITHUB_TOKEN" ]]; then
        echo "$GITHUB_TOKEN" | gh auth login --with-token --hostname github.com
        echo "$DICE_URL" | gh secret set DICE_SERVICE_URL
        echo "$COLOR_URL" | gh secret set COLOR_SERVICE_URL
        echo "$FRONTEND_URL" | gh secret set FRONTEND_URL
        echo "✅ Service URLs stored in GitHub secrets"
    else
        echo "⚠️ GITHUB_TOKEN not found - skipping secret storage"
    fi
fi

echo ""
echo "✅ Microservices deployment complete!"
echo "🎲 Dice Service: https://$DICE_URL"
echo "🎨 Color Service: https://$COLOR_URL"
echo "🌐 Frontend Dashboard: https://$FRONTEND_URL"
```

### `scripts/cleanup-microservices.sh`
```bash
#!/bin/bash
set -e

echo "🧹 Cleaning up microservices"
source .env

# Delete container apps
echo "🗑️ Deleting container apps..."
az containerapp delete --name dice-service --resource-group $RG_NAME --yes || true
az containerapp delete --name color-service --resource-group $RG_NAME --yes || true
az containerapp delete --name frontend --resource-group $RG_NAME --yes || true

# Delete environment
if [[ -n "$CONTAINERAPP_ENV" ]]; then
    az containerapp env delete \
      --name $CONTAINERAPP_ENV \
      --resource-group $RG_NAME \
      --yes || true
    echo "✅ Container Apps environment deleted"
fi

echo "✅ Cleanup complete"
```

## ✅ Step 5: Deploy & Test

### Build and Deploy
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Build all services
./scripts/build-all.sh

# Deploy to Container Apps
./scripts/deploy-microservices.sh
```

### Test Services Individually
```bash
source .env

# Test Dice Service
curl https://$DICE_URL/
curl https://$DICE_URL/roll
curl https://$DICE_URL/roll/20
curl https://$DICE_URL/stats

# Test Color Service
curl https://$COLOR_URL/
curl https://$COLOR_URL/random
curl https://$COLOR_URL/palette/5
curl https://$COLOR_URL/theme/ocean
```

### Test Frontend Integration
```bash
# Open frontend dashboard
echo "🌐 Frontend Dashboard: https://$FRONTEND_URL"

# Test API integrations through the UI:
# 1. Click "Roll Dice" - should call dice service
# 2. Click "Random Color" - should call color service
# 3. Generate palettes and themes
# 4. Check service health indicators
```

## ✅ Step 6: Monitor & Scale

### Check Service Health
```bash
# View all container apps
az containerapp list --resource-group $RG_NAME --output table

# Check individual service status
az containerapp show --name dice-service --resource-group $RG_NAME --query properties.provisioningState
az containerapp show --name color-service --resource-group $RG_NAME --query properties.provisioningState
az containerapp show --name frontend --resource-group $RG_NAME --query properties.provisioningState

# Monitor replicas
az containerapp replica list --name dice-service --resource-group $RG_NAME --output table
```

### Load Testing
```bash
# Test dice service load
for i in {1..20}; do
  curl https://$DICE_URL/roll &
done
wait

# Test color service load
for i in {1..20}; do
  curl https://$COLOR_URL/random &
done
wait

# Monitor scaling
az containerapp replica list --name dice-service --resource-group $RG_NAME --output table
az containerapp replica list --name color-service --resource-group $RG_NAME --output table
```

### Cleanup
```bash
./scripts/cleanup-microservices.sh
```

## 🎓 Complete

### What You Built
✅ **Microservices Architecture** - 3 independent containerized services
✅ **Dice Service** - Random number generation with statistics tracking
✅ **Color Service** - Color palette generation with predefined themes
✅ **Frontend Dashboard** - Interactive UI making independent API calls
✅ **Auto-scaling** - Services scale independently based on load
✅ **Service Discovery** - Frontend dynamically configured with service URLs

### Key Skills Learned
- Microservices deployment to Azure Container Apps
- Independent service scaling and load balancing
- Cross-service communication via HTTP APIs
- Frontend integration with multiple backend services
- Container orchestration and service discovery
- Multi-service CI/CD pipeline management

### Next Steps (Challenge)
- Add authentication and rate limiting
- Implement service mesh for advanced networking
- Add monitoring and distributed tracing
- Create API gateway for unified access
