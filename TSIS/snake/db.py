import sqlite3

DB_NAME = "snake.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            score INTEGER,
            level_reached INTEGER,
            played_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username = ?", (username,))
    player = cur.fetchone()

    if player:
        player_id = player[0]
    else:
        cur.execute(
            "INSERT INTO players (username) VALUES (?)",
            (username,)
        )
        player_id = cur.lastrowid
        conn.commit()

    conn.close()
    return player_id


def save_score(username, score, level):
    player_id = get_or_create_player(username)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (?, ?, ?)
    """, (player_id, score, level))

    conn.commit()
    conn.close()


def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(gs.score)
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        WHERE p.username = ?
    """, (username,))

    result = cur.fetchone()[0]
    conn.close()

    return result if result else 0


def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC, gs.level_reached DESC
        LIMIT 10
    """)

    results = cur.fetchall()
    conn.close()

    return results