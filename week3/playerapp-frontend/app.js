async function fetchPlayersFromAPI() {
    try {
        const response = await fetch('http://localhost:5000/players');
        const data = await response.json();
        return data.players;
    } catch (error) {
        console.log('API not available, using local data');
        return generateLocalPlayers();
    }
}

function generateLocalPlayers() {
    const players = [];
    
    for (let i = 0; i < 5; i++) {
        players.push({
            id: Math.floor(Math.random() * 900) + 100,
            name: `Player-${Math.floor(Math.random() * 900) + 100}`,
            score: Math.floor(Math.random() * 101)
        });
    }
    return players;
}

// Update generatePlayers function
async function generatePlayers() {
    const players = await fetchPlayersFromAPI();
    document.getElementById('players').innerHTML = players
        .map(p => `<div class="player">ID: ${p.id} | ${p.name} | Score: ${p.score}</div>`)
        .join('');
}

generatePlayers();
