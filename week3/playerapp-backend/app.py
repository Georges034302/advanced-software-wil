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
