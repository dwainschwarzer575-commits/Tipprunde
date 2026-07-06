# app.py
import streamlit as st
import sqlite3
from contextlib import closing
from datetime import datetime

DB_PATH = "tipprunde.db"

# --- DB Setup ---
def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phase TEXT NOT NULL,
            home TEXT NOT NULL,
            away TEXT NOT NULL,
            res_h INTEGER,
            res_a INTEGER,
            created_at TEXT NOT NULL
        )""")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            game_id INTEGER NOT NULL,
            tip_h INTEGER,
            tip_a INTEGER,
            updated_at TEXT NOT NULL,
            UNIQUE(user, game_id),
            FOREIGN KEY(game_id) REFERENCES games(id) ON DELETE CASCADE
        )""")
        # Neue Tabelle für Weltmeistertipps
        conn.execute("""
        CREATE TABLE IF NOT EXISTS world_cup_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL UNIQUE,
            winner TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )""")
        conn.commit()


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# --- CRUD ---
def add_game(phase, home, away):
    conn = get_db()
    with conn:
        conn.execute(
            "INSERT INTO games (phase, home, away, created_at) VALUES (?, ?, ?, ?)",
            (phase, home, away, datetime.utcnow().isoformat())
        )


def delete_game(game_id):
    conn = get_db()
    with conn:
        conn.execute("DELETE FROM games WHERE id = ?", (game_id,))


def update_result(game_id, res_h, res_a):
    conn = get_db()
    with conn:
        conn.execute("UPDATE games SET res_h = ?, res_a = ? WHERE id = ?", (res_h, res_a, game_id))


def save_tip(user, game_id, tip_h, tip_a):
    conn = get_db()
    with conn:
        now = datetime.utcnow().isoformat()
        cur = conn.execute("SELECT id FROM tips WHERE user = ? AND game_id = ?", (user, game_id)).fetchone()
        if cur:
            conn.execute("UPDATE tips SET tip_h = ?, tip_a = ?, updated_at = ? WHERE id = ?", (tip_h, tip_a, now, cur["id"]))
        else:
            conn.execute("INSERT INTO tips (user, game_id, tip_h, tip_a, updated_at) VALUES (?, ?, ?, ?, ?)",
                         (user, game_id, tip_h, tip_a, now))


def save_world_cup_tip(user, winner):
    """Speichert den Weltmeistertipp"""
    conn = get_db()
    with conn:
        now = datetime.utcnow().isoformat()
        cur = conn.execute("SELECT id FROM world_cup_tips WHERE user = ?", (user,)).fetchone()
        if cur:
            conn.execute("UPDATE world_cup_tips SET winner = ?, updated_at = ? WHERE user = ?", (winner, now, user))
        else:
            conn.execute("INSERT INTO world_cup_tips (user, winner, updated_at) VALUES (?, ?, ?)",
                         (user, winner, now))


def get_world_cup_tip(user):
    """Holt den Weltmeistertipp eines Spielers"""
    conn = get_db()
    row = conn.execute("SELECT winner FROM world_cup_tips WHERE user = ?", (user,)).fetchone()
    return row["winner"] if row else None


def get_games():
    conn = get_db()
    return conn.execute("SELECT * FROM games ORDER BY created_at ASC").fetchall()


def get_games_by_phase(phase):
    conn = get_db()
    return conn.execute("SELECT * FROM games WHERE phase = ? ORDER BY created_at ASC", (phase,)).fetchall()


def get_user_tips(user):
    conn = get_db()
    rows = conn.execute("SELECT t.*, g.phase, g.home, g.away, g.res_h, g.res_a FROM tips t JOIN games g ON t.game_id = g.id WHERE t.user = ?", (user,)).fetchall()
    return rows


def get_all_tips_grouped():
    conn = get_db()
    rows = conn.execute("SELECT t.user, t.game_id, t.tip_h, t.tip_a, g.res_h, g.res_a FROM tips t JOIN games g ON t.game_id = g.id").fetchall()
    grouped = {}
    for r in rows:
        grouped.setdefault(r["user"], []).append(dict(r))
    return grouped


def get_all_users():
    """Alle Spieler auslesen"""
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT user FROM tips ORDER BY user ASC").fetchall()
    return [r["user"] for r in rows]


def delete_user_data(user):
    """Alle Daten eines Spielers löschen"""
    conn = get_db()
    with conn:
        conn.execute("DELETE FROM tips WHERE user = ?", (user,))
        conn.execute("DELETE FROM world_cup_tips WHERE user = ?", (user,))


def get_all_phases():
    """Alle eindeutigen Phasen auslesen"""
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT phase FROM games ORDER BY created_at ASC").fetchall()
    return [r["phase"] for r in rows]


def calculate_points_for_user(user, world_cup_winner=None):
    conn = get_db()
    rows = conn.execute("SELECT t.tip_h, t.tip_a, g.res_h, g.res_a FROM tips t JOIN games g ON t.game_id = g.id WHERE t.user = ?", (user,)).fetchall()
    pts = 0
    for r in rows:
        if r["res_h"] is None or r["res_a"] is None:
            continue
        try:
            rh, ra, th, ta = int(r["res_h"]), int(r["res_a"]), int(r["tip_h"]), int(r["tip_a"])
        except (TypeError, ValueError):
            continue
        if rh == th and ra == ta:
            pts += 3
        elif (rh - ra) == 0 and (th - ta) == 0:
            pts += 1
        elif (rh - ra) * (th - ta) > 0:
            pts += 1
    
    # Weltmeistertipp-Bonus
    if world_cup_winner and get_world_cup_tip(user) == world_cup_winner:
        pts += 20
    
    return pts


def calculate_points_for_tip(tip_h, tip_a, res_h, res_a):
    """Berechnet Punkte für einen einzelnen Tipp"""
    if res_h is None or res_a is None:
        return 0
    try:
        rh, ra, th, ta = int(res_h), int(res_a), int(tip_h), int(tip_a)
    except (TypeError, ValueError):
        return 0
    
    if rh == th and ra == ta:
        return 3
    elif (rh - ra) == 0 and (th - ta) == 0:
        return 1
    elif (rh - ra) * (th - ta) > 0:
        return 1
    return 0


# --- Streamlit UI ---
st.set_page_config(page_title="Tipprunde", layout="wide")
init_db()

# Session State initialisieren
if "user" not in st.session_state:
    st.session_state.user = ""

st.title("🏆 WM 2026 Tipp-Runde")

# Reiter erstellen
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Tipps", "🏅 Rangliste", "📊 Detailansicht", "🌍 Weltmeistertipp"])

# --- TAB 1: TIPPS ---
with tab1:
    # --- HAUPTBEREICH: Name-Eingabe (mobil-freundlich) ---
    col_name_input, col_name_spacer = st.columns([3, 1])
    with col_name_input:
        user = st.text_input("👤 Dein Name", value=st.session_state.user, placeholder="Name eingeben...", label_visibility="collapsed")
        if user:
            st.session_state.user = user

    if user:
        col_status, col_delete = st.columns([3, 1])
        with col_status:
            st.success(f"✅ Angemeldet als: **{user}**")
        with col_delete:
            if st.button("🗑️ Profil löschen", use_container_width=True):
                if st.session_state.get(f"confirm_delete_{user}", False):
                    delete_user_data(user)
                    st.session_state.user = ""
                    st.session_state[f"confirm_delete_{user}"] = False
                    st.success("Profil gelöscht!")
                    st.rerun()
                else:
                    st.session_state[f"confirm_delete_{user}"] = True
                    st.warning("⚠️ Klick nochmal zum Bestätigen!")
    else:
        st.warning("⚠️ Bitte gib deinen Namen ein, um Tipps zu machen!")

    st.markdown("---")

    # Add game
    st.subheader("➕ Neues Spiel hinzufügen")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        phase_in = st.selectbox("Phase", 
            ["Gruppenphase", "Sechzehntelfinale", "Achtelfinale", "Viertelfinale", "Halbfinale", "Finale"],
            key="phase_in", index=None)
    with col2:
        home_in = st.text_input("Heim-Team", placeholder="z.B. Deutschland", key="home_in")
    with col3:
        away_in = st.text_input("Gast-Team", placeholder="z.B. Frankreich", key="away_in")
    with col4:
        st.write("")  # Spacing
        st.write("")
        if st.button("✅ Hinzufügen", use_container_width=True):
            if phase_in and home_in and away_in:
                add_game(phase_in, home_in, away_in)
                st.success("Spiel hinzugefügt!")
                st.rerun()
            else:
                st.error("⚠️ Bitte alle Felder ausfüllen!")

    st.markdown("---")

    # Phasenfilter
    st.subheader("🎮 Spiele & Tipps nach Phase")
    phases = get_all_phases()
    if phases:
        selected_phase = st.selectbox("Filtern nach Phase:", ["Alle"] + phases, key="filter_phase")
        
        if selected_phase == "Alle":
            games_to_show = get_games()
        else:
            games_to_show = get_games_by_phase(selected_phase)
    else:
        games_to_show = []

    if not games_to_show:
        st.info("📭 Keine Spiele vorhanden. Füge oben ein Spiel hinzu!")
    else:
        for g in games_to_show:
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.2, 1.2, 1])
                
                # Spielinfo
                with col1:
                    st.markdown(f"### {g['phase']}")
                    st.write(f"**{g['home']}** vs **{g['away']}**")
                
                # Tipps
                with col2:
                    st.write("**Dein Tipp:**")
                    if user:
                        col_h, col_a = st.columns(2)
                        with col_h:
                            tip_h = st.number_input(f"H", min_value=0, max_value=10, format="%d", key=f"tip_h_{g['id']}")
                        with col_a:
                            tip_a = st.number_input(f"A", min_value=0, max_value=10, format="%d", key=f"tip_a_{g['id']}")
                        if st.button("💾 Speichern", key=f"save_tip_{g['id']}", use_container_width=True):
                            save_tip(user, g['id'], tip_h, tip_a)
                            st.success("Tipp gespeichert!")
                            st.rerun()
                    else:
                        st.warning("Bitte Namen eingeben!")
                
                # Ergebnisse (kompakt)
                with col3:
                    st.write("**Ergebnis:**")
                    col_h, col_a = st.columns(2, gap="small")
                    with col_h:
                        res_h = st.number_input(f"H", min_value=0, max_value=10, format="%d", 
                                              value=g['res_h'] if g['res_h'] is not None else 0, 
                                              key=f"res_h_{g['id']}", label_visibility="collapsed")
                    with col_a:
                        res_a = st.number_input(f"A", min_value=0, max_value=10, format="%d", 
                                              value=g['res_a'] if g['res_a'] is not None else 0, 
                                              key=f"res_a_{g['id']}", label_visibility="collapsed")
                
                # Speichern Button für Ergebnis
                with col4:
                    if st.button("📝 Speichern", key=f"save_res_{g['id']}", use_container_width=True):
                        update_result(g['id'], res_h, res_a)
                        st.success("Ergebnis gespeichert!")
                        st.rerun()
                
                # Lösch-Button
                with col5:
                    if st.button("🗑️", key=f"del_game_{g['id']}"):
                        delete_game(g['id'])
                        st.success("Spiel gelöscht!")
                        st.rerun()

    # Legende für Punktewertung
    st.markdown("---")
    st.subheader("📋 Punktewertung")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **✅ 3 Punkte**
        - Exaktes Ergebnis
        - Beispiel: Du tippst 2:1 und das Ergebnis ist 2:1
        """)
    with col2:
        st.markdown("""
        **🟡 1 Punkt**
        - Unentschieden
        - Beispiel: Du tippst 1:1 und das Ergebnis ist 2:2
        """)
    with col3:
        st.markdown("""
        **🟡 1 Punkt**
        - Richtige Gewinnermannschaft
        - Beispiel: Du tippst 2:1 und das Ergebnis ist 3:1 (beide Heimsieg)
        """)

# --- TAB 2: RANGLISTE ---
with tab2:
    st.subheader("🏅 Rangliste")
    tips_grouped = get_all_tips_grouped()
    
    # Weltmeistertipp auslesen
    world_cup_winner = None
    conn = get_db()
    winner_row = conn.execute("SELECT winner FROM world_cup_tips LIMIT 1").fetchone()
    if winner_row:
        world_cup_winner = winner_row["winner"]
    
    scores = []
    for name in tips_grouped.keys():
        pts = calculate_points_for_user(name, world_cup_winner)
        scores.append((name, pts))
    scores.sort(key=lambda x: -x[1])

    if not scores:
        st.info("Noch keine Tipps abgegeben.")
    else:
        # Tabelle
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write("**Spieler**")
        with col2:
            st.write("**Punkte**")
        with col3:
            st.write("**WM-Tipp**")
        
        for idx, (name, pts) in enumerate(scores, start=1):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                st.write(f"{medal} {name}")
            with col2:
                st.write(f"**{pts}**")
            with col3:
                wc_tip = get_world_cup_tip(name)
                st.write(f"**{wc_tip if wc_tip else '-'}**")

# --- TAB 3: DETAILANSICHT ---
with tab3:
    st.subheader("📊 Detailansicht - Tipps nach Phase")
    
    phases = get_all_phases()
    if not phases:
        st.info("📭 Keine Spiele vorhanden.")
    else:
        selected_phase = st.selectbox("Wähle eine Phase:", phases, key="phase_select")
        
        games_in_phase = get_games_by_phase(selected_phase)
        
        if not games_in_phase:
            st.info(f"Keine Spiele in der Phase '{selected_phase}' vorhanden.")
        else:
            st.write(f"### Spiele in: **{selected_phase}**")
            
            for g in games_in_phase:
                with st.container(border=True):
                    st.markdown(f"**{g['home']}** vs **{g['away']}**")
                    
                    # Ergebnis anzeigen + nachträglich bearbeiten
                    col1, col2 = st.columns([2, 2])
                    with col1:
                        if g['res_h'] is not None and g['res_a'] is not None:
                            st.write(f"📊 **Endergebnis: {g['res_h']}:{g['res_a']}**")
                        else:
                            st.write("📊 **Endergebnis: Noch nicht eingetragen**")
                    with col2:
                        st.write("**Ergebnis nachtragen:**")
                        col_h, col_a = st.columns(2, gap="small")
                        with col_h:
                            res_h_detail = st.number_input(f"H", min_value=0, max_value=10, 
                                                  value=g['res_h'] if g['res_h'] is not None else 0,
                                                  key=f"detail_res_h_{g['id']}", label_visibility="collapsed")
                        with col_a:
                            res_a_detail = st.number_input(f"A", min_value=0, max_value=10,
                                                  value=g['res_a'] if g['res_a'] is not None else 0,
                                                  key=f"detail_res_a_{g['id']}", label_visibility="collapsed")
                        if st.button("💾 Speichern", key=f"detail_save_{g['id']}", use_container_width=True):
                            update_result(g['id'], res_h_detail, res_a_detail)
                            st.success("Ergebnis gespeichert!")
                            st.rerun()
                    
                    # Alle Tipps für dieses Spiel anzeigen
                    conn = get_db()
                    tips = conn.execute(
                        "SELECT user, tip_h, tip_a FROM tips WHERE game_id = ? ORDER BY user ASC",
                        (g['id'],)
                    ).fetchall()
                    
                    if tips:
                        st.write("**Tipps der Spieler:**")
                        
                        # Tabelle für Tipps
                        cols = st.columns([2, 1, 1])
                        with cols[0]:
                            st.write("**Spieler**")
                        with cols[1]:
                            st.write("**Tipp**")
                        with cols[2]:
                            st.write("**Punkte**")
                        
                        for tip in tips:
                            pts = calculate_points_for_tip(tip["tip_h"], tip["tip_a"], g['res_h'], g['res_a'])
                            cols = st.columns([2, 1, 1])
                            with cols[0]:
                                st.write(tip["user"])
                            with cols[1]:
                                st.write(f"{tip['tip_h']}:{tip['tip_a']}")
                            with cols[2]:
                                if pts == 3:
                                    st.write("✅ 3")
                                elif pts == 1:
                                    st.write("🟡 1")
                                else:
                                    st.write("❌ 0")
                    else:
                        st.info("Noch keine Tipps für dieses Spiel.")

# --- TAB 4: WELTMEISTERTIPP ---
with tab4:
    st.subheader("🌍 Weltmeistertipp")
    st.write("Tippe hier, welche Mannschaft die WM 2026 gewinnt! Bei richtigem Tipp bekommst du **20 Zusatzpunkte**.")
    
    if user:
        current_tip = get_world_cup_tip(user)
        world_cup_teams = [
            "🇦🇷 Argentinien", "🇦🇺 Australien", "🇦🇹 Österreich", "🇧🇪 Belgien", 
            "🇧🇷 Brasilien", "🇧🇬 Bulgarien", "🇨🇦 Kanada", "🇭🇷 Kroatien",
            "🇨🇿 Tschechien", "🇩🇰 Dänemark", "🇪🇬 Ägypten", "🇫🇮 Finnland",
            "🇫🇷 Frankreich", "🇩🇪 Deutschland", "🇬🇷 Griechenland", "🇭🇺 Ungarn",
            "🇮🇸 Island", "🇮🇹 Italien", "🇮🇷 Iran", "🇯🇵 Japan", "🇲🇽 Mexiko",
            "🇳🇱 Niederlande", "🇳🇿 Neuseeland", "🇳🇬 Nigeria", "🇳🇴 Norwegen",
            "🇵🇱 Polen", "🇵🇹 Portugal", "🇷🇴 Rumänien", "🇷🇺 Russland", "🇪🇸 Spanien",
            "🇸🇪 Schweden", "🇨🇭 Schweiz", "🇹🇷 Türkei", "🇺🇦 Ukraine", "🇬🇧 England",
            "🇺🇸 USA", "🇺🇾 Uruguay"
        ]
        
        selected_team = st.selectbox(
            "Wähle deinen Weltmeister:",
            world_cup_teams,
            index=world_cup_teams.index(current_tip) if current_tip in world_cup_teams else 0,
            key="wm_select"
        )
        
        if st.button("🏆 Weltmeistertipp speichern", use_container_width=True):
            save_world_cup_tip(user, selected_team)
            st.success(f"✅ Weltmeistertipp gespeichert: **{selected_team}**")
            st.balloons()
    else:
        st.warning("⚠️ Bitte gib deinen Namen in Tab 1 ein, um einen Weltmeistertipp abzugeben!")

st.markdown("---")
st.info("💾 Hinweis: Die App speichert Daten in einer lokalen SQLite-Datei (tipprunde.db).")
st.info("💾 Hinweis: Die App speichert Daten in einer lokalen SQLite-Datei (tipprunde.db). Bei der Bereitstellung auf bestimmten Plattformen (z.B. Streamlit Cloud) können lokale Dateien zwischenzeitlich zurückgesetzt werden.")
