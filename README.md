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
        /* Schöne Scrollbalken für das helle Design */
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
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen pb-12 selection:bg-indigo-100 selection:text-indigo-900">

    <!-- Toast-Container für helle Benachrichtigungen -->
    <div id="toastContainer" class="fixed top-4 right-4 z-50 space-y-2 pointer-events-none"></div>

    <!-- Verbindungshinweis (Dezente Statusleiste) -->
    <div id="connectionStatus" class="bg-slate-200 text-slate-600 text-xs font-semibold py-1.5 px-4 text-center transition-all duration-300">
        ⚡ Initialisiere Tipp-Zentrale...
    </div>

    <!-- Header-Banner (Helles Layout) -->
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
                Tippe gemeinsam mit der Familie! Alle Daten synchronisieren sich blitzschnell im Hintergrund.
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
                            <input id="newPhase" type="text" placeholder="Phase (z.B. Achtelfinale)" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                        </div>
                        <div>
                            <input id="newHome" type="text" placeholder="Heim-Team" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                        </div>
                        <div>
                            <input id="newAway" type="text" placeholder="Gast-Team" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                        </div>
                        <button onclick="addGame()" class="w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white rounded-xl font-bold text-sm py-3 px-4 shadow-sm hover:shadow transition-all flex items-center justify-center gap-1.5">
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
                            Wer tippt gerade?
                        </label>
                        <input type="text" id="userName" oninput="handleUserChange()" placeholder="Deinen Namen eingeben (lädt sofort deine Tipps)" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3.5 text-slate-900 placeholder-slate-400 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                    </div>

                    <!-- Spieletitel -->
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Spielpaarungen &amp; Ergebnisse</span>
                        <span class="text-xs text-indigo-600 font-semibold cursor-default bg-indigo-50 px-2.5 py-1 rounded-full">Tippe links | Trage rechts reale Ergebnisse ein</span>
                    </div>

                    <!-- Spielliste -->
                    <div id="gameList" class="space-y-4">
                        <!-- Wird sofort lokal befüllt -->
                    </div>

                    <!-- Speicher-Button -->
                    <button onclick="saveMyTips()" class="w-full bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white p-4 rounded-xl mt-6 font-bold tracking-wide shadow-sm hover:shadow transition-all flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                        </svg>
                        Tipps &amp; Ergebnisse speichern
                    </button>
                </div>
            </div>

            <!-- Rechte Spalte: Rangliste -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="flex items-center gap-2.5 mb-5">
                        <div class="p-2 bg-amber-50 rounded-lg text-amber-600">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                        </div>
                        <h2 class="text-xl font-bold text-slate-950 tracking-tight">🏆 Live-Rangliste</h2>
                    </div>

                    <div id="leaderboard" class="space-y-2.5 max-h-[400px] overflow-y-auto pr-1">
                        <!-- Wird sofort lokal befüllt -->
                    </div>
                    
                    <!-- Punktewertung Legende -->
                    <div class="mt-6 pt-5 border-t border-slate-100 text-xs text-slate-500 space-y-2 bg-slate-50 -mx-6 -mb-6 p-6 rounded-b-2xl">
                        <h4 class="font-bold text-slate-700 flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Punktewertung:
                        </h4>
                        <ul class="space-y-1.5 list-none pl-0">
                            <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> <b>3 Punkte:</b> Exaktes Ergebnis getippt</li>
                            <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span> <b>1 Punkt:</b> Richtige Tendenz (Sieg/Remis)</li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Detailansicht Modal -->
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

    <!-- Helles Custom Confirmation Modal -->
    <div id="confirmModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-all">
         <div class="bg-white border border-slate-200 rounded-2xl p-6 max-w-sm w-full shadow-2xl transform transition-all">
              <div class="p-3 bg-rose-50 rounded-full text-rose-600 w-fit mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
              </div>
              <h3 id="confirmTitle" class="text-lg font-bold text-slate-950">Aktion bestätigen</h3>
              <p id="confirmMessage" class="text-sm text-slate-500 mt-2">Möchtest du diese Aktion wirklich durchführen? Das kann nicht rückgängig gemacht werden.</p>
              <div class="flex justify-end gap-3 mt-6">
                  <button id="confirmCancelBtn" class="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-800 bg-slate-100 hover:bg-slate-200 rounded-xl transition">Abbrechen</button>
                  <button id="confirmActionBtn" class="px-4 py-2 text-sm font-semibold text-white bg-rose-600 hover:bg-rose-700 rounded-xl transition">Bestätigen</button>
              </div>
         </div>
    </div>

    <script type="module">
        // Firebase Importe
        import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js';
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js';
        import { getFirestore, doc, setDoc, getDoc, collection, onSnapshot, updateDoc, deleteDoc } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js';

        // 1. INITIALE LOCAL-FIRST DATEN (Wird in unter 1ms geladen!)
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

        // Lokalen Speicher auslesen, bevor Firebase initialisiert wird
        window.games = JSON.parse(localStorage.getItem('games') || JSON.stringify(initialGames));
        window.usersData = JSON.parse(localStorage.getItem('wm_data') || '{}');

        // UI sofort rendern (Keine Wartezeit!)
        render();
        renderLeaderboard();

        // 2. CHECK OB FIREBASE CONFIG EXISTIERT (Umgebungsprüfung)
        let hasCloudConfig = false;
        let firebaseApp, auth, db, appId;

        const connectionStatus = document.getElementById('connectionStatus');
        const badgeStorage = document.getElementById('badgeStorage');

        try {
            if (typeof __firebase_config !== 'undefined' && __firebase_config) {
                const firebaseConfig = JSON.parse(__firebase_config);
                firebaseApp = initializeApp(firebaseConfig);
                auth = getAuth(firebaseApp);
                db = getFirestore(firebaseApp);
                appId = typeof __app_id !== 'undefined' ? __app_id : 'wm-tippspiel-2026';
                hasCloudConfig = true;
            }
        } catch (e) {
            console.warn("Cloud-Dienste konnten nicht initialisiert werden (lokaler Modus aktiv).", e);
        }

        if (!hasCloudConfig) {
            // Reiner lokaler Betrieb (ideal für Google Drive/Netlify etc. ohne Konfiguration)
            connectionStatus.className = "bg-indigo-500 text-white text-xs font-semibold py-1.5 px-4 text-center";
            connectionStatus.innerText = "💾 Lokaler Modus aktiv (Tipps werden auf diesem Gerät gespeichert)";
            badgeStorage.className = "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700 border border-indigo-100 mb-3";
            badgeStorage.innerText = "💾 Lokaler Speicher";
        } else {
            // Im Hintergrund mit Cloud verbinden
            connectionStatus.innerText = "🔄 Verbinde im Hintergrund mit der Cloud...";
            initAuth();
        }

        // 3. ANONYME CLOUD-AUTHENTIFIZIERUNG IM HINTERGRUND
        async function initAuth() {
            try {
                if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
                    await signInWithCustomToken(auth, __initial_auth_token);
                } else {
                    await signInAnonymously(auth);
                }
                
                onAuthStateChanged(auth, (user) => {
                    if (user) {
                        connectionStatus.className = "bg-emerald-600 text-white text-xs font-semibold py-1.5 px-4 text-center transition-all duration-300";
                        connectionStatus.innerText = "☁️ Synchronisiert mit Live-Cloud!";
                        badgeStorage.className = "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100 mb-3";
                        badgeStorage.innerText = "☁️ Live-Cloud synchronisiert";
                        
                        // Blende die Statusleiste nach erfolgreichem Sync dezent aus
                        setTimeout(() => {
                            connectionStatus.style.height = "0";
                            connectionStatus.style.padding = "0";
                            connectionStatus.style.overflow = "hidden";
                        }, 2500);

                        // Startet die Echtzeit-Synchronisation
                        setupRealtimeListeners();
                    }
                });
            } catch (error) {
                console.error("Cloud connection failed:", error);
                connectionStatus.className = "bg-rose-500 text-white text-xs font-semibold py-1.5 px-4 text-center";
                connectionStatus.innerText = "⚠️ Cloud offline. Verwende lokalen Zwischenspeicher.";
            }
        }

        // 4. CLOUD LIVE LISTENERS
        function setupRealtimeListeners() {
            // Spiele synchronisieren
            const gamesCollection = collection(db, 'artifacts', appId, 'public', 'data', 'games');
            onSnapshot(gamesCollection, (snapshot) => {
                const cloudGames = [];
                snapshot.forEach(doc => {
                    cloudGames.push({ id: doc.id, ...doc.data() });
                });
                
                if (cloudGames.length > 0) {
                    cloudGames.sort((a, b) => (a.createdAt || 0) - (b.createdAt || 0));
                    window.games = cloudGames;
                    localStorage.setItem('games', JSON.stringify(window.games));
                    render();
                } else {
                    // Falls die Cloud komplett leer ist, initialen Datensatz hochladen
                    syncInitialGamesToCloud();
                }
            }, (err) => console.warn("Games sync error:", err));

            // Tipps synchronisieren
            const tipsCollection = collection(db, 'artifacts', appId, 'public', 'data', 'tips');
            onSnapshot(tipsCollection, (snapshot) => {
                const cloudTips = {};
                snapshot.forEach(doc => {
                    cloudTips[doc.id] = doc.data().tips || [];
                   background: #94a3b8;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen pb-12 selection:bg-indigo-100 selection:text-indigo-900">

    <!-- Toast-Container für helle Benachrichtigungen -->
    <div id="toastContainer" class="fixed top-4 right-4 z-50 space-y-2 pointer-events-none"></div>

    <!-- Verbindungshinweis (Dezente Statusleiste) -->
    <div id="connectionStatus" class="bg-slate-200 text-slate-600 text-xs font-semibold py-1.5 px-4 text-center transition-all duration-300">
        ⚡ Initialisiere Tipp-Zentrale...
    </div>

    <!-- Header-Banner (Helles Layout) -->
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
                Tippe gemeinsam mit der Familie! Alle Daten synchronisieren sich blitzschnell im Hintergrund.
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
                            <input id="newPhase" type="text" placeholder="Phase (z.B. Achtelfinale)" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                        </div>
                        <div>
                            <input id="newHome" type="text" placeholder="Heim-Team" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                        </div>
                        <div>
                            <input id="newAway" type="text" placeholder="Gast-Team" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                        </div>
                        <button onclick="addGame()" class="w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white rounded-xl font-bold text-sm py-3 px-4 shadow-sm hover:shadow transition-all flex items-center justify-center gap-1.5">
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
                            Wer tippt gerade?
                        </label>
                        <input type="text" id="userName" oninput="handleUserChange()" placeholder="Deinen Namen eingeben (lädt sofort deine Tipps)" class="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-indigo-500 focus:bg-white rounded-xl p-3.5 text-slate-900 placeholder-slate-400 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all">
                    </div>

                    <!-- Spieletitel -->
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Spielpaarungen &amp; Ergebnisse</span>
                        <span class="text-xs text-indigo-600 font-semibold cursor-default bg-indigo-50 px-2.5 py-1 rounded-full">Tippe links | Trage rechts reale Ergebnisse ein</span>
                    </div>

                    <!-- Spielliste -->
                    <div id="gameList" class="space-y-4">
                        <!-- Wird sofort lokal befüllt -->
                    </div>

                    <!-- Speicher-Button -->
                    <button onclick="saveMyTips()" class="w-full bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white p-4 rounded-xl mt-6 font-bold tracking-wide shadow-sm hover:shadow transition-all flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                        </svg>
                        Tipps &amp; Ergebnisse speichern
                    </button>
                </div>
            </div>

            <!-- Rechte Spalte: Rangliste -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="flex items-center gap-2.5 mb-5">
                        <div class="p-2 bg-amber-50 rounded-lg text-amber-600">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                        </div>
                        <h2 class="text-xl font-bold text-slate-950 tracking-tight">🏆 Live-Rangliste</h2>
                    </div>

                    <div id="leaderboard" class="space-y-2.5 max-h-[400px] overflow-y-auto pr-1">
                        <!-- Wird sofort lokal befüllt -->
                    </div>
                    
                    <!-- Punktewertung Legende -->
                    <div class="mt-6 pt-5 border-t border-slate-100 text-xs text-slate-500 space-y-2 bg-slate-50 -mx-6 -mb-6 p-6 rounded-b-2xl">
                        <h4 class="font-bold text-slate-700 flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Punktewertung:
                        </h4>
                        <ul class="space-y-1.5 list-none pl-0">
                            <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> <b>3 Punkte:</b> Exaktes Ergebnis getippt</li>
                            <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span> <b>1 Punkt:</b> Richtige Tendenz (Sieg/Remis)</li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Detailansicht Modal -->
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

    <!-- Helles Custom Confirmation Modal -->
    <div id="confirmModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-all">
         <div class="bg-white border border-slate-200 rounded-2xl p-6 max-w-sm w-full shadow-2xl transform transition-all">
              <div class="p-3 bg-rose-50 rounded-full text-rose-600 w-fit mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
              </div>
              <h3 id="confirmTitle" class="text-lg font-bold text-slate-950">Aktion bestätigen</h3>
              <p id="confirmMessage" class="text-sm text-slate-500 mt-2">Möchtest du diese Aktion wirklich durchführen? Das kann nicht rückgängig gemacht werden.</p>
              <div class="flex justify-end gap-3 mt-6">
                  <button id="confirmCancelBtn" class="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-800 bg-slate-100 hover:bg-slate-200 rounded-xl transition">Abbrechen</button>
                  <button id="confirmActionBtn" class="px-4 py-2 text-sm font-semibold text-white bg-rose-600 hover:bg-rose-700 rounded-xl transition">Bestätigen</button>
              </div>
         </div>
    </div>

    <script type="module">
        // Firebase Importe
        import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js';
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js';
        import { getFirestore, doc, setDoc, getDoc, collection, onSnapshot, updateDoc, deleteDoc } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js';

        // 1. INITIALE LOCAL-FIRST DATEN (Wird in unter 1ms geladen!)
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

        // Lokalen Speicher auslesen, bevor Firebase initialisiert wird
        window.games = JSON.parse(localStorage.getItem('games') || JSON.stringify(initialGames));
        window.usersData = JSON.parse(localStorage.getItem('wm_data') || '{}');

        // UI sofort rendern (Keine Wartezeit!)
        render();
        renderLeaderboard();

        // 2. CHECK OB FIREBASE CONFIG EXISTIERT (Umgebungsprüfung)
        let hasCloudConfig = false;
        let firebaseApp, auth, db, appId;

        const connectionStatus = document.getElementById('connectionStatus');
        const badgeStorage = document.getElementById('badgeStorage');

        try {
            if (typeof __firebase_config !== 'undefined' && __firebase_config) {
                const firebaseConfig = JSON.parse(__firebase_config);
                firebaseApp = initializeApp(firebaseConfig);
                auth = getAuth(firebaseApp);
                db = getFirestore(firebaseApp);
                appId = typeof __app_id !== 'undefined' ? __app_id : 'wm-tippspiel-2026';
                hasCloudConfig = true;
            }
        } catch (e) {
            console.warn("Cloud-Dienste konnten nicht initialisiert werden (lokaler Modus aktiv).", e);
        }

        if (!hasCloudConfig) {
            // Reiner lokaler Betrieb (ideal für Google Drive/Netlify etc. ohne Konfiguration)
            connectionStatus.className = "bg-indigo-500 text-white text-xs font-semibold py-1.5 px-4 text-center";
            connectionStatus.innerText = "💾 Lokaler Modus aktiv (Tipps werden auf diesem Gerät gespeichert)";
            badgeStorage.className = "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700 border border-indigo-100 mb-3";
            badgeStorage.innerText = "💾 Lokaler Speicher";
        } else {
            // Im Hintergrund mit Cloud verbinden
            connectionStatus.innerText = "🔄 Verbinde im Hintergrund mit der Cloud...";
            initAuth();
        }

        // 3. ANONYME CLOUD-AUTHENTIFIZIERUNG IM HINTERGRUND
        async function initAuth() {
            try {
                if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
                    await signInWithCustomToken(auth, __initial_auth_token);
                } else {
                    await signInAnonymously(auth);
                }
                
                onAuthStateChanged(auth, (user) => {
                    if (user) {
                        connectionStatus.className = "bg-emerald-600 text-white text-xs font-semibold py-1.5 px-4 text-center transition-all duration-300";
                        connectionStatus.innerText = "☁️ Synchronisiert mit Live-Cloud!";
                        badgeStorage.className = "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100 mb-3";
                        badgeStorage.innerText = "☁️ Live-Cloud synchronisiert";
                        
                        // Blende die Statusleiste nach erfolgreichem Sync dezent aus
                        setTimeout(() => {
                            connectionStatus.style.height = "0";
                            connectionStatus.style.padding = "0";
                            connectionStatus.style.overflow = "hidden";
                        }, 2500);

                        // Startet die Echtzeit-Synchronisation
                        setupRealtimeListeners();
                    }
                });
            } catch (error) {
                console.error("Cloud connection failed:", error);
                connectionStatus.className = "bg-rose-500 text-white text-xs font-semibold py-1.5 px-4 text-center";
                connectionStatus.innerText = "⚠️ Cloud offline. Verwende lokalen Zwischenspeicher.";
            }
        }

        // 4. CLOUD LIVE LISTENERS
        function setupRealtimeListeners() {
            // Spiele synchronisieren
            const gamesCollection = collection(db, 'artifacts', appId, 'public', 'data', 'games');
            onSnapshot(gamesCollection, (snapshot) => {
                const cloudGames = [];
                snapshot.forEach(doc => {
                    cloudGames.push({ id: doc.id, ...doc.data() });
                });
                
                if (cloudGames.length > 0) {
                    cloudGames.sort((a, b) => (a.createdAt || 0) - (b.createdAt || 0));
                    window.games = cloudGames;
                    localStorage.setItem('games', JSON.stringify(window.games));
                    render();
                } else {
                    // Falls die Cloud komplett leer ist, initialen Datensatz hochladen
                    syncInitialGamesToCloud();
                }
            }, (err) => console.warn("Games sync error:", err));

            // Tipps synchronisieren
            const tipsCollection = collection(db, 'artifacts', appId, 'public', 'data', 'tips');
            onSnapshot(tipsCollection, (snapshot) => {
                const cloudTips = {};
                snapshot.forEach(doc => {
                    cloudTips[doc.id] = doc.data().tips || [];
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
