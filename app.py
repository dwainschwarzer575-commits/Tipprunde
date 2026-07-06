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


def get_games():
    conn = get_db()
    return conn.execute("SELECT * FROM games ORDER BY created_at ASC").fetchall()


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


def calculate_points_for_user(user):
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
    return pts

# --- Streamlit UI ---
st.set_page_config(page_title="Tipprunde", layout="wide")
init_db()

# Session State initialisieren
if "user" not in st.session_state:
    st.session_state.user = ""

st.title("🏆 WM 2026 Tipp-Runde")

# Sidebar: Benutzer mit besserer Sichtbarkeit
st.sidebar.markdown("## 👤 Spieler")
user = st.sidebar.text_input("Dein Name", value=st.session_state.user, placeholder="Name eingeben...")
if user:
    st.session_state.user = user

# Aktuellen Namen prominent oben anzeigen (gut für Mobile)
if user:
    st.info(f"📍 **Angemeldet als:** {user}")
else:
    st.warning("⚠️ Bitte gib deinen Namen ein, um Tipps zu machen!")

st.sidebar.markdown("---")
st.sidebar.info("Gib deinen Namen ein, damit deine Tipps gespeichert werden.")

# Add game
st.subheader("➕ Neues Spiel hinzufügen")
col1, col2, col3, col4 = st.columns(4)
with col1:
    phase_in = st.text_input("Phase", placeholder="z.B. Gruppenphase", key="phase_in")
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

# Main area: games + tip inputs
st.subheader("🎮 Spiele & Tipps")
games = get_games()
if not games:
    st.info("📭 Keine Spiele vorhanden. Füge oben ein Spiel hinzu!")
else:
    for g in games:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1])
            
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
            
            # Ergebnisse
            with col3:
                st.write("**Ergebnis:**")
                col_h, col_a = st.columns(2)
                with col_h:
                    res_h = st.number_input(f"H", min_value=0, max_value=10, format="%d", 
                                          value=g['res_h'] if g['res_h'] is not None else 0, 
                                          key=f"res_h_{g['id']}")
                with col_a:
                    res_a = st.number_input(f"A", min_value=0, max_value=10, format="%d", 
                                          value=g['res_a'] if g['res_a'] is not None else 0, 
                                          key=f"res_a_{g['id']}")
                if st.button("📝 Speichern", key=f"save_res_{g['id']}", use_container_width=True):
                    update_result(g['id'], res_h, res_a)
                    st.success("Ergebnis gespeichert!")
                    st.rerun()
            
            # Bearbeitungs-Button
            with col4:
                if st.button("✏️ Bearbeiten", key=f"edit_game_{g['id']}", use_container_width=True):
                    st.session_state[f"edit_game_{g['id']}"] = True
            
            # Lösch-Button
            with col5:
                if st.button("🗑️", key=f"del_game_{g['id']}"):
                    delete_game(g['id'])
                    st.success("Spiel gelöscht!")
                    st.rerun()
        
        # Bearbeitungs-Sektion
        if st.session_state.get(f"edit_game_{g['id']}", False):
            with st.expander(f"🔧 Spiel {g['id']} bearbeiten", expanded=True):
                st.warning("⚠️ Hinweis: Bearbeitung wird hier später erweitert.")
                if st.button("❌ Bearbeitung schließen", key=f"close_edit_{g['id']}"):
                    st.session_state[f"edit_game_{g['id']}"] = False
                    st.rerun()

# Leaderboard
st.markdown("---")
st.subheader("🏅 Rangliste")
tips_grouped = get_all_tips_grouped()
scores = []
for name in tips_grouped.keys():
    pts = calculate_points_for_user(name)
    scores.append((name, pts))
scores.sort(key=lambda x: -x[1])

if not scores:
    st.info("Noch keine Tipps abgegeben.")
else:
    # Tabelle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Spieler**")
    with col2:
        st.write("**Punkte**")
    
    for idx, (name, pts) in enumerate(scores, start=1):
        col1, col2 = st.columns([3, 1])
        with col1:
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
            st.write(f"{medal} {name}")
        with col2:
            st.write(f"**{pts}**")

st.markdown("---")
st.info("💾 Hinweis: Die App speichert Daten in einer lokalen SQLite-Datei (tipprunde.db). Bei der Bereitstellung auf bestimmten Plattformen (z.B. Streamlit Cloud) können lokale Dateien zwischen Neustarts verloren gehen. Nutze dann einen externen Datenbankdienst.")