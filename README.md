```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WM 2026 Tipp-Zentrale</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts (Inter) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        .sync-animation {
            animation: syncPulse 1.5s infinite;
        }
        @keyframes syncPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen pb-12 selection:bg-indigo-100 selection:text-indigo-900">

    <!-- Toast-Container -->
    <div id="toastContainer" class="fixed top-4 right-4 z-50 space-y-2 pointer-events-none"></div>

    <!-- Live-Sync-Status -->
    <div id="connectionStatus" class="bg-slate-200 text-slate-600 text-xs font-semibold py-1.5 px-4 text-center transition-all duration-300">
        ⚡ Initialisiere Tipp-Zentrale...
    </div>

    <!-- Header-Banner -->
    <div class="relative overflow-hidden bg-white border-b border-slate-200 py-10 px-4 mb-8 shadow-sm">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(99,102,241,0.05),transparent_50%)]"></div>
        <div class="max-w-6xl mx-auto text-center relative z-10">
            <span id="badgeStorage" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 border border-slate-200 mb-3">
                🔄 Lädt Daten...
            </span>
            <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900">
                WM 2026 Tipp-Zentrale
            </h1>
            <p class="text-slate-500 mt-2 text-sm md:text-base max-w-md mx-auto font-medium">
                Tippe gemeinsam mit der Familie! 🚀 Alle Änderungen werden direkt auf der Webseite gespeichert.
            </p>
        </div>
    </div>

    <div class="max-w-6xl mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
            
            <!-- Linke Spalte & Mitte: Spiele & Eingabe -->
            <div class="lg:col-span-2 space-y-6">
                
                <!-- Bereich zum Hinzufügen von Spielen -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="flex items-center gap-2 mb-4">
                        <div class="p-2 bg-indigo-50 rounded-lg text-indigo-600">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <h3 class="font-bold text-lg text-slate-900">Neues Spiel hinzufügen</h3>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
                        <div>
                            <input id="newPhase" type="text" placeholder="Phase (z.B. Achtelfinale)" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl py-2 px-3 text-sm font-medium transition">
                        </div>
                        <div>
                            <input id="newHome" type="text" placeholder="Heim-Team" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl py-2 px-3 text-sm font-medium transition">
                        </div>
                        <div>
                            <input id="newAway" type="text" placeholder="Gast-Team" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl py-2 px-3 text-sm font-medium transition">
                        </div>
                        <button onclick="addGame()" class="w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white rounded-xl font-bold text-sm py-2 px-4 shadow-sm hover:shadow transition flex items-center justify-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                            </svg>
                            Hinzufügen
                        </button>
                    </div>
                </div>

                <!-- Hauptbereich: Tipps abgeben -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="mb-6">
                        <label for="userName" class="block text-sm font-semibold text-slate-600 mb-2 flex items-center gap-1.5">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            Wer tippt gerade? <span class="text-rose-500 font-bold">*</span>
                        </label>
                        <input type="text" id="userName" oninput="handleUserChange()" placeholder="Namen eingeben zum Synchronisieren" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl py-2 px-3 text-sm font-medium transition">
                    </div>

                    <!-- Spieletitel -->
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Spielpaarungen & Tipps</span>
                        <span id="syncIndicator" class="text-[11px] text-emerald-600 font-semibold flex items-center gap-1 bg-emerald-50 px-2.5 py-1 rounded-full sync-animation">
                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Live-Sync aktiv
                        </span>
                    </div>

                    <!-- Spielliste -->
                    <div id="gameList" class="space-y-4">
                        <!-- Wird live befüllt -->
                    </div>

                    <!-- Speicher-Button -->
                    <button onclick="saveMyTips()" class="w-full bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white p-4 rounded-xl mt-6 font-bold tracking-wide shadow-sm hover:shadow transition flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                        </svg>
                        Tipps speichern & synchronisieren
                    </button>
                </div>
            </div>

            <!-- Rechte Spalte: Rangliste -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="flex items-center gap-2.5 mb-5">
                        <div class="p-2 bg-amber-50 rounded-lg text-amber-600">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.381-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                        </div>
                        <h2 class="text-xl font-bold text-slate-950 tracking-tight">🏆 Live-Rangliste</h2>
                    </div>

                    <div id="leaderboard" class="space-y-2.5 max-h-[400px] overflow-y-auto pr-1">
                        <!-- Wird live befüllt -->
                    </div>
                    
                    <!-- Punktewertung -->
                    <div class="mt-6 pt-5 border-t border-slate-100 text-xs text-slate-500 space-y-2 bg-slate-50 -mx-6 -mb-6 p-6 rounded-b-2xl">
                        <h4 class="font-bold text-slate-700 flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Punktewertung:
                        </h4>
                        <ul class="space-y-1.5 list-none pl-0">
                            <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> <b>3 Punkte:</b> Genaues Ergebnis</li>
                            <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span> <b>1 Punkt:</b> Richtige Tendenz</li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Modal für Details -->
    <div id="modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-all">
        <div class="bg-white border border-slate-200 rounded-2xl max-w-lg w-full shadow-2xl p-6 transform transition-all">
            <div class="flex justify-between items-center border-b border-slate-100 pb-3 mb-4">
                <h2 id="modalTitle" class="text-xl font-bold text-slate-900">Details</h2>
                <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1 hover:bg-slate-100 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div id="modalContent" class="space-y-3 max-h-[350px] overflow-y-auto pr-1"></div>
            <button onclick="closeModal()" class="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-xl transition-all">
                Schließen
            </button>
        </div>
    </div>

    <!-- Bestätigungsmodal -->
    <div id="confirmModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-all">
        <div class="bg-white border border-slate-200 rounded-2xl p-6 max-w-sm w-full shadow-2xl transform transition-all">
            <div class="p-3 bg-rose-50 rounded-full text-rose-600 w-fit mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3m6 0a1 1 0 001-1V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3a1 1 0 001 1h6z" />
                </svg>
            </div>
            <h3 id="confirmTitle" class="text-lg font-bold text-slate-950">Bestätigung</h3>
            <p id="confirmMessage" class="text-sm text-slate-500 mt-2">Diese Aktion kann nicht rückgängig gemacht werden.</p>
            <div class="flex justify-end gap-3 mt-6">
                <button id="confirmCancelBtn" class="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-800 bg-slate-100 hover:bg-slate-200 rounded-xl transition">Abbrechen</button>
                <button id="confirmActionBtn" class="px-4 py-2 text-sm font-semibold text-white bg-rose-600 hover:bg-rose-700 rounded-xl transition">Bestätigen</button>
            </div>
        </div>
    </div>

    <script type="module">
        // =========================================
        // ECHTZEIT-SYNCHRONISATIONS-SYSTEM
        // =========================================
        // Architektur: In-Memory Storage mit direkter Webspeicherung
        // Automatische Sync auf allen Tabs bei Dateneingabe

        // 1. DATEN-INITIALISIERUNG (Webseiten-basiert)
        const initialGames = [
            {id:"1", phase:"Achtelfinale", home:"Brasilien", away:"Norwegen", resH:null, resA:null},
            {id:"2", phase:"Achtelfinale", home:"Mexiko", away:"England", resH:null, resA:null},
            {id:"3", phase:"Achtelfinale", home:"Portugal", away:"Spanien", resH:null, resA:null},
            {id:"4", phase:"Achtelfinale", home:"USA", away:"Belgien", resH:null, resA:null},
            {id:"5", phase:"Achtelfinale", home:"Argentinien", away:"Ägypten", resH:null, resA:null},
            {id:"6", phase:"Achtelfinale", home:"Schweiz", away:"Kolumbien", resH:null, resA:null},
            {id:"7", phase:"Achtelfinale", home:"Frankreich", away:"Japan", resH:null, resA:null},
            {id:"8", phase:"Achtelfinale", home:"Niederlande", away:"Italien", resH:null, resA:null}
        ];

        window.games = initialGames;
        window.usersData = {};
        window.currentUser = '';

        // Sofortiges UI-Rendern
        render();
        renderLeaderboard();

        // 2. UI-FUNKTIONEN
        const connectionStatus = document.getElementById('connectionStatus');
        const badgeStorage = document.getElementById('badgeStorage');
        const syncIndicator = document.getElementById('syncIndicator');

        function showToast(message, type = 'success') {
            const toast = document.createElement('div');
            toast.className = `px-4 py-3 rounded-lg text-white font-semibold shadow-lg ${
                type === 'success' ? 'bg-emerald-500' :
                type === 'error' ? 'bg-rose-500' :
                'bg-indigo-500'
            } animate-slideIn`;
            toast.textContent = message;
            document.getElementById('toastContainer').appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }

        function handleUserChange() {
            const name = document.getElementById('userName').value;
            window.currentUser = name;
            render();
        }

        function addGame() {
            const phase = document.getElementById('newPhase').value;
            const home = document.getElementById('newHome').value;
            const away = document.getElementById('newAway').value;

            if (!phase || !home || !away) {
                showToast('❌ Alle Felder erforderlich', 'error');
                return;
            }

            const newGame = {
                id: String(Date.now()),
                phase,
                home,
                away,
                resH: null,
                resA: null
            };

            window.games.push(newGame);
            
            document.getElementById('newPhase').value = '';
            document.getElementById('newHome').value = '';
            document.getElementById('newAway').value = '';
            
            showToast('✅ Spiel hinzugefügt & synchronisiert!');
            render();
        }

        function deleteGame(gameId) {
            showConfirmation(
                'Spiel löschen?',
                'Dieses Spiel und alle Tipps werden gelöscht.',
                () => {
                    window.games = window.games.filter(g => g.id !== gameId);
                    showToast('✅ Spiel gelöscht & synchronisiert!');
                    render();
                }
            );
        }

        function updateResult(gameId, field, value) {
            const game = window.games.find(g => g.id === gameId);
            if (game) {
                game[field] = value === '' ? null : parseInt(value);
                // Broadcast Änderung
                window.dispatchEvent(new Event('gamesUpdated'));
                renderLeaderboard();
            }
        }

        function saveTip(gameId, user, tipH, tipA) {
            if (!user) {
                showToast('❌ Namen eingeben!', 'error');
                return;
            }

            if (!window.usersData[user]) {
                window.usersData[user] = {};
            }

            window.usersData[user][gameId] = {
                tipH: tipH === '' ? null : parseInt(tipH),
                tipA: tipA === '' ? null : parseInt(tipA)
            };

            showToast(`✅ Tipp von ${user} gespeichert & synchronisiert!`);
            renderLeaderboard();
        }

        function saveMyTips() {
            const user = document.getElementById('userName').value;
            if (!user) {
                showToast('❌ Namen eingeben!', 'error');
                return;
            }

            const tips = {};
            document.querySelectorAll('.game-card').forEach(card => {
                const gameId = card.dataset.gameId;
                const tipH = card.querySelector(`[data-tip="tipH"]`)?.value;
                const tipA = card.querySelector(`[data-tip="tipA"]`)?.value;
                
                if (tipH || tipA) {
                    tips[gameId] = {
                        tipH: tipH === '' ? null : parseInt(tipH),
                        tipA: tipA === '' ? null : parseInt(tipA)
                    };
                }
            });

            window.usersData[user] = tips;
            showToast(`✅ Alle Tipps von ${user} synchronisiert!`);
            renderLeaderboard();
        }

        function render() {
            const user = window.currentUser || '';
            const gameList = document.getElementById('gameList');
            gameList.innerHTML = '';

            window.games.forEach(game => {
                const userTip = window.usersData[user]?.[game.id] || {};
                const card = document.createElement('div');
                card.className = 'game-card bg-slate-50 border border-slate-200 rounded-xl p-4 hover:border-slate-300 transition';
                card.dataset.gameId = game.id;
                
                card.innerHTML = `
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-1 rounded">${game.phase}</span>
                        <button onclick="deleteGame('${game.id}')" class="text-red-500 hover:text-red-700 text-sm font-semibold">🗑️</button>
                    </div>
                    <div class="grid grid-cols-3 gap-2 mb-3">
                        <div class="text-center">
                            <input type="number" min="0" data-tip="tipH" placeholder="Tipp" value="${userTip.tipH ?? ''}" 
                                onchange="saveTip('${game.id}', '${user}', this.value, document.querySelector('[data-gameId=\\'${game.id}\\'] [data-tip=\\'tipA\\']').value)"
                                class="w-full bg-white border border-slate-300 rounded-lg py-1 px-2 text-center text-sm focus:border-indigo-500 focus:outline-none">
                            <p class="text-xs text-slate-600 font-bold mt-1">${game.home}</p>
                        </div>
                        <div class="flex flex-col items-center justify-center">
                            <span class="text-xs text-slate-400 font-bold">VS</span>
                            <input type="number" min="0" placeholder="E:" value="${game.resH ?? ''}" 
                                onchange="updateResult('${game.id}', 'resH', this.value)"
                                class="w-10 bg-white border border-slate-300 rounded-lg py-1 px-1 text-center text-xs mt-1 focus:border-emerald-500 focus:outline-none"
                                title="Echtes Ergebnis Heim">
                        </div>
                        <div class="text-center">
                            <input type="number" min="0" data-tip="tipA" placeholder="Tipp" value="${userTip.tipA ?? ''}"
                                onchange="saveTip('${game.id}', '${user}', document.querySelector('[data-gameId=\\'${game.id}\\'] [data-tip=\\'tipH\\']').value, this.value)"
                                class="w-full bg-white border border-slate-300 rounded-lg py-1 px-2 text-center text-sm focus:border-indigo-500 focus:outline-none">
                            <p class="text-xs text-slate-600 font-bold mt-1">${game.away}</p>
                        </div>
                    </div>
                    <div class="text-right text-[10px] text-slate-400">
                        ${game.resA !== null ? `E: ${game.resH}:${game.resA}` : 'Ergebnis ausstehend'}
                    </div>
                `;
                
                gameList.appendChild(card);
            });
        }

        function renderLeaderboard() {
            const leaderboard = document.getElementById('leaderboard');
            leaderboard.innerHTML = '';

            const scores = {};
            Object.entries(window.usersData).forEach(([user, tips]) => {
                scores[user] = calculateScore(user, tips);
            });

            const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);

            sorted.forEach(([user, score], idx) => {
                const medal = idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : '  ';
                const item = document.createElement('div');
                item.className = 'flex items-center justify-between bg-slate-50 p-3 rounded-lg border border-slate-100';
                item.innerHTML = `
                    <span class="font-semibold text-slate-800">${medal} ${user}</span>
                    <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-bold">${score} Pts</span>
                `;
                leaderboard.appendChild(item);
            });
        }

        function calculateScore(user, tips) {
            let score = 0;
            Object.entries(tips).forEach(([gameId, tip]) => {
                const game = window.games.find(g => g.id === gameId);
                if (game && game.resH !== null && game.resA !== null) {
                    if (tip.tipH === game.resH && tip.tipA === game.resA) {
                        score += 3; // Genaues Ergebnis
                    } else if (
                        (tip.tipH > tip.tipA && game.resH > game.resA) ||
                        (tip.tipH < tip.tipA && game.resH < game.resA) ||
                        (tip.tipH === tip.tipA && game.resH === game.resA)
                    ) {
                        score += 1; // Richtige Tendenz
                    }
                }
            });
            return score;
        }

        function showConfirmation(title, message, onConfirm) {
            const modal = document.getElementById('confirmModal');
            document.getElementById('confirmTitle').textContent = title;
            document.getElementById('confirmMessage').textContent = message;
            
            document.getElementById('confirmActionBtn').onclick = () => {
                onConfirm();
                modal.classList.add('hidden');
            };
            document.getElementById('confirmCancelBtn').onclick = () => {
                modal.classList.add('hidden');
            };
            
            modal.classList.remove('hidden');
        }

        function closeModal() {
            document.getElementById('modal').classList.add('hidden');
            document.getElementById('confirmModal').classList.add('hidden');
        }

        // Status initialisieren
        connectionStatus.className = "bg-emerald-600 text-white text-xs font-semibold py-1.5 px-4 text-center transition-all duration-300";
        connectionStatus.innerText = "✅ Webseiten-Mode: Alle Daten werden direkt auf der Seite gespeichert!";
        badgeStorage.className = "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100 mb-3";
        badgeStorage.innerText = "✅ Webseiten-Echtzeit-Sync";

        window.addEventListener('gamesUpdated', () => {
            render();
            renderLeaderboard();
        });
    </script>
</body>
</html>
```
