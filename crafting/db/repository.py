from typing import List, Optional
from crafting.core.models import Note
from crafting.db.connection import get_connection

class NoteRepository:
    @staticmethod
    def add(note: Note) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO notes (title, content, tags, is_encrypted, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (note.title, note.content,note.tags, int(note.is_encrypted), note.created_at, note.updated_at)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all() -> List[Note]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content, tags, is_encrypted, created_at, updated_at FROM notes")
            rows = cursor.fetchall()
            return[
                Note(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    tags=row["tags"],
                    is_encrypted=row["is_encrypted"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
                for row in rows
            ]

    @staticmethod
    def get_by_id(note_id: int) -> Optional[Note]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content, tags, is_encrypted, created_at, updated_at FROM notes WHERE id = ?", (note_id,))
            row = cursor.fetchone()
            if row:
                return Note(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    tags=row["tags"],
                    is_encrypted=bool(row["is_encrypted"]),
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            return None

    @staticmethod
    def search(query: str) -> List[Note]:
        with get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute(
                """
                SELECT id, title, content, tags, is_encrypted, created_at, updated_at 
                FROM notes 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                """,
                (search_pattern, search_pattern, search_pattern)
            )
            rows = cursor.fetchall()
            return [
                Note(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    tags=row["tags"],
                    is_encrypted=bool(row["is_encrypted"]),
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
                for row in rows
            ]

    @staticmethod
    def delete(note_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            if cursor.rowcount == 0:
                return False

            cursor.execute("SELECT title,content, tags, is_encrypted, created_at, updated_at FROM notes ORDER BY id ASC")
            remaining_notes = cursor.fetchall()

            cursor.execute("DELETE FROM notes")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='notes'")

            for note in remaining_notes:
                cursor.execute(
                    """
                    INSERT INTO notes (title, content, tags, is_encrypted, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (note["title"], note["content"], note["tags"], note["is_encrypted"], note["created_at"], note["updated_at"])    
                )

            conn.commit()
            return True
        