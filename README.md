```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WM 2026 Tipp-Zentrale</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-4">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-center mb-6">⚽ WM 2026 Tipp-Zentrale</h1>
        
        <!-- Bereich zum Hinzufügen von Spielen -->
        <div class="bg-blue-50 p-4 rounded-lg mb-6 shadow-sm border border-blue-200">
            <h3 class="font-bold mb-2 text-sm text-blue-800">Neues Spiel hinzufügen:</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <input id="newPhase" placeholder="Phase" class="p-2 border rounded text-sm">
                <input id="newHome" placeholder="Heim" class="p-2 border rounded text-sm">
                <input id="newAway" placeholder="Gast" class="p-2 border rounded text-sm">
                <button onclick="addGame()" class="bg-blue-600 text-white rounded font-bold text-sm hover:bg-blue-700">Hinzufügen</button>
            </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-md mb-6">
            <input type="text" id="userName" placeholder="Dein Name" class="w-full p-3 border rounded mb-4">
            <div id="gameList" class="space-y-4"></div>
            <button onclick="saveMyTips()" class="w-full bg-green-600 text-white p-3 rounded-lg mt-4 font-bold">Tipps speichern</button>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-md">
            <h2 class="text-xl font-bold mb-4">🏆 Rangliste</h2>
            <div id="leaderboard" class="space-y-2"></div>
            
            <!-- Punktewertung Legende -->
            <div class="mt-6 pt-4 border-t text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                <h4 class="font-bold mb-1">Punktewertung:</h4>
                <ul class="list-disc pl-5">
                    <li><b>3 Punkte:</b> Exaktes Ergebnis getippt.</li>
                    <li><b>1 Punkt:</b> Richtige Tendenz (Sieg/Niederlage/Unentschieden) bei falschem Ergebnis.</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Detailansicht Modal -->
    <div id="modal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
        <div class="bg-white p-6 rounded-xl max-w-lg w-full">
            <h2 id="modalTitle" class="text-xl font-bold mb-4">Details</h2>
            <div id="modalContent" class="space-y-2 text-sm"></div>
            <button onclick="document.getElementById('modal').classList.add('hidden')" class="mt-4 w-full bg-gray-500 text-white p-2 rounded">Schließen</button>
        </div>
    </div>

    <script>
        const initialGames = [
            {id:1, phase:"Achtelfinale", home:"Brasilien", away:"Norwegen", resH:null, resA:null},
            {id:2, phase:"Achtelfinale", home:"Mexiko", away:"England", resH:null, resA:null},
            {id:3, phase:"Achtelfinale", home:"Portugal", away:"Spanien", resH:null, resA:null},
            {id:4, phase:"Achtelfinale", home:"USA", away:"Belgien", resH:null, resA:null},
            {id:5, phase:"Achtelfinale", home:"Argentinien", away:"Ägypten", resH:null, resA:null},
            {id:6, phase:"Achtelfinale", home:"Schweiz", away:"Kolumbien", resH:null, resA:null},
            {id:7, phase:"Achtelfinale", home:"Frankreich", away:"Japan", resH:null, resA:null},
            {id:8, phase:"Achtelfinale", home:"Niederlande", away:"Italien", resH:null, resA:null}
        ];

        let games = JSON.parse(localStorage.getItem('games') || JSON.stringify(initialGames));

        function render() {
            const list = document.getElementById('gameList');
            list.innerHTML = games.map(g => `
                <div class="border-b pb-2">
                    <span class="text-[10px] uppercase text-gray-500 font-bold">${g.phase} | ${g.home} vs ${g.away}</span>
                    <div class="flex items-center gap-2 mt-1">
                        <input type="number" class="tipH w-12 border p-1 rounded" data-id="${g.id}" placeholder="H"> : 
                        <input type="number" class="tipA w-12 border p-1 rounded" data-id="${g.id}" placeholder="A">
                        <span class="ml-4 text-[10px] text-gray-400">Erg:</span>
                        <input type="number" value="${g.resH ?? ''}" onchange="updateResult(${g.id}, 'h', this.value)" class="w-10 border p-1 rounded" placeholder="H"> : 
                        <input type="number" value="${g.resA ?? ''}" onchange="updateResult(${g.id}, 'a', this.value)" class="w-10 border p-1 rounded" placeholder="A">
                    </div>
                </div>
            `).join('');
            renderLeaderboard();
        }

        function addGame() {
            const phase = document.getElementById('newPhase').value;
            const home = document.getElementById('newHome').value;
            const away = document.getElementById('newAway').value;
            if(!phase || !home || !away) return alert("Alle Felder ausfüllen!");
            games.push({ id: Date.now(), phase, home, away, resH: null, resA: null });
            localStorage.setItem('games', JSON.stringify(games));
            render();
        }

        function deletePlayer(name) {
            if(!confirm("Wirklich löschen?")) return;
            let data = JSON.parse(localStorage.getItem('wm_data') || '{}');
            delete data[name];
            localStorage.setItem('wm_data', JSON.stringify(data));
            render();
        }

        function updateResult(id, type, val) {
            const game = games.find(g => g.id == id);
            if(type === 'h') game.resH = val === "" ? null : val; else game.resA = val === "" ? null : val;
            localStorage.setItem('games', JSON.stringify(games));
            render();
        }

        function saveMyTips() {
            const name = document.getElementById('userName').value.trim();
            if (!name) return alert("Bitte Namen eingeben!");
            const tips = Array.from(document.querySelectorAll('.tipH')).map(el => ({
                id: el.dataset.id, h: el.value, a: document.querySelector(`.tipA[data-id="${el.dataset.id}"]`).value
            }));
            let data = JSON.parse(localStorage.getItem('wm_data') || '{}');
            data[name] = tips;
            localStorage.setItem('wm_data', JSON.stringify(data));
            render();
        }

        function showDetails(name) {
            const data = JSON.parse(localStorage.getItem('wm_data') || '{}');
            const userTips = data[name];
            document.getElementById('modalTitle').innerText = `Details für ${name}`;
            document.getElementById('modalContent').innerHTML = userTips.map(t => {
                const g = games.find(ga => ga.id == t.id);
                if(!g) return '';
                let pts = 0;
                if (g.resH !== null && g.resA !== null && t.h !== "" && t.a !== "") {
                    if (g.resH == t.h && g.resA == t.a) pts = 3;
                    else if ((g.resH > g.resA && t.h > t.a) || (g.resH < g.resA && t.h < t.a)) pts = 1;
                }
                return `<div class="border-b py-1 flex justify-between">
                    <span>${g.home}-${g.away}</span>
                    <span>Tipp: ${t.h}:${t.a} | Erg: ${g.resH ?? '-'}:${g.resA ?? '-'}</span>
                    <b class="text-blue-600">${pts} Pkt</b>
                </div>`;
            }).join('');
            document.getElementById('modal').classList.remove('hidden');
        }

        function renderLeaderboard() {
            const data = JSON.parse(localStorage.getItem('wm_data') || '{}');
            const board = document.getElementById('leaderboard');
            board.innerHTML = Object.keys(data).map(name => {
                let pts = 0;
                data[name].forEach(t => {
                    const g = games.find(ga => ga.id == t.id);
                    if (g && g.resH !== null && g.resA !== null && t.h !== "" && t.a !== "") {
                        if (g.resH == t.h && g.resA == t.a) pts += 3;
                        else if ((g.resH > g.resA && t.h > t.a) || (g.resH < g.resA && t.h < t.a)) pts = 1;
                    }
                });
                return `<div class="flex justify-between items-center border-b p-2">
                            <span onclick="showDetails('${name}')" class="cursor-pointer text-blue-600 underline">${name}</span>
                            <div class="flex items-center gap-4"><b>${pts} Pkt</b><button onclick="deletePlayer('${name}')" class="text-red-400 text-xs hover:text-red-600">Löschen</button></div>
                        </div>`;
            }).join('');
        }

        window.onload = render;
    </script>
</body>
</html>

```
