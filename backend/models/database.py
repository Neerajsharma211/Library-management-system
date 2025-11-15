import sqlite3
import os
from contextlib import contextmanager
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self._initialize_db()

    def _initialize_db(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Check if tables already exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone():
                # Database already initialized
                return

            # Read and execute schema
            schema_path = os.path.join(os.path.dirname(__file__), '../../database/schema.sql')
            with open(schema_path, 'r') as f:
                schema = f.read()
                cursor.executescript(schema)

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch_one:
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch_all:
                return [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                return cursor.lastrowid

# Global database instance
db = Database()
