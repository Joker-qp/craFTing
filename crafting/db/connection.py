import sqlite3
from crafting.config import DB_PATH, ensure_app_dir_exists

def get_connection() -> sqlite3.Connection:
    ensure_app_dir_exists()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_encrypted INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("PRAGMA table_info(notes)")
    collums = [column[1] for column in cursor.fetchall()]
    if "tags" not in collums:
        cursor.execute("ALTER TABLE notes ADD COLUMN tags TEXT")


    conn.commit()