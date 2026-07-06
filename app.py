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

st.title("WM 2026 Tipp-Runde (Streamlit)")

# Sidebar: Benutzer
user = st.sidebar.text_input("Name", value=st.session_state.get("user", ""))
if user:
    st.session_state["user"] = user

st.sidebar.markdown("---")
st.sidebar.write("Dein Name wird benötigt, damit deine Tipps gespeichert werden.")

# Add game
with st.expander("Neues Spiel hinzufügen"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        phase_in = st.text_input("Phase", key="phase_in")
    with col2:
        home_in = st.text_input("Heim-Team", key="home_in")
    with col3:
        away_in = st.text_input("Gast-Team", key="away_in")
    with col4:
        if st.button("Spiel hinzufügen"):
            if phase_in and home_in and away_in:
                add_game(phase_in, home_in, away_in)
                st.experimental_rerun()
            else:
                st.warning("Alle Felder ausfüllen.")

# Main area: games + tip inputs
games = get_games()
if not games:
    st.info("Keine Spiele vorhanden. Füge oben ein Spiel hinzu.")
else:
    st.write("## Spiele / Tipps")
    for g in games:
        cols = st.columns([3, 2, 1])
        with cols[0]:
            st.markdown(f"**{g['phase']}** — **{g['home']}** vs **{g['away']}**")
        with cols[1]:
            # Tip inputs for current user
            if user:
                tip_h = st.number_input(f"Tipp {g['id']}-H ({g['home']})", min_value=0, format="%d", key=f"tip_h_{g['id']}")
                tip_a = st.number_input(f"Tipp {g['id']}-A ({g['away']})", min_value=0, format="%d", key=f"tip_a_{g['id']}")
                if st.button(f"Speichern Tipp {g['id']}", key=f"save_tip_{g['id']}"):
                    save_tip(user, g['id'], tip_h, tip_a)
                    st.success("Tipp gespeichert.")
                    st.experimental_rerun()
            else:
                st.info("Bitte Name in der Sidebar eingeben, um zu tippen.")
        with cols[2]:
            # Ergebnisse (Admin / lokal)
            res_h = st.number_input(f"Erg H {g['id']}", min_value=0, format="%d", value=g['res_h'] if g['res_h'] is not None else 0, key=f"res_h_{g['id']}")
            res_a = st.number_input(f"Erg A {g['id']}", min_value=0, format="%d", value=g['res_a'] if g['res_a'] is not None else 0, key=f"res_a_{g['id']}")
            if st.button(f"Ergebnis speichern {g['id']}", key=f"save_res_{g['id']}"):
                update_result(g['id'], res_h, res_a)
                st.success("Ergebnis gespeichert.")
                st.experimental_rerun()
            if st.button(f"Spiel löschen {g['id']}", key=f"del_game_{g['id']}"):
                delete_game(g['id'])
                st.success("Spiel gelöscht.")
                st.experimental_rerun()

# Leaderboard
st.write("## Rangliste")
# gather users
tips_grouped = get_all_tips_grouped()
scores = []
for name in tips_grouped.keys():
    pts = calculate_points_for_user(name)
    scores.append((name, pts))
scores.sort(key=lambda x: -x[1])
if not scores:
    st.info("Noch keine Tipper.")
else:
    for idx, (name, pts) in enumerate(scores, start=1):
        st.write(f"{idx}. **{name}** — {pts} Pkt")

st.markdown("---")
st.write("Hinweis: Diese Demo speichert Daten in einer lokalen SQLite-Datei (tipprunde.db). Beim Hosten auf bestimmten Plattformen kann die lokale Datei zwischen Deployments nicht persistent sein — für dauerhafte Speicherung empfehle ich eine echte Datenbank (Supabase/Postgres) oder Firebase mit Service Account.")
