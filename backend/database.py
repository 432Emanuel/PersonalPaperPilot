"""
SQLite database handler for storing document metadata.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


class Database:
    """Handles all database operations for the PPP app."""

    def __init__(self, db_path: str = "data/ppp.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self._ensure_db_dir()
        self._create_tables()

    def _ensure_db_dir(self):
        """Create database directory if it doesn't exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get a fresh database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        """Create the documents table if it doesn't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                category TEXT NOT NULL,
                text TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def save_document(self, filename: str, category: str, text: str) -> int:
        """
        Save a new document record to the database.

        Args:
            filename: Name of the stored file
            category: Classified category
            text: Extracted OCR text

        Returns:
            The ID of the inserted record
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO documents (filename, category, text, created_at)
            VALUES (?, ?, ?, ?)
        """, (filename, category, text, created_at))

        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return doc_id

    def get_document(self, doc_id: int) -> Optional[dict]:
        """Retrieve a document by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_all_documents(self) -> list[dict]:
        """Retrieve all documents."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_documents_by_category(self, category: str) -> list[dict]:
        """Retrieve all documents of a specific category."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM documents WHERE category = ? ORDER BY created_at DESC",
            (category,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
