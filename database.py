import os
import mysql.connector


def get_connection():
    """Create a fresh connection to the configured airport_system database."""
    return mysql.connector.connect(
        host=os.getenv("AIRPORT_DB_HOST", "localhost"),
        port=int(os.getenv("AIRPORT_DB_PORT", "3306")),
        user=os.getenv("AIRPORT_DB_USER", "root"),
        password=os.getenv("AIRPORT_DB_PASSWORD", ""),
        database=os.getenv("AIRPORT_DB_NAME", "airport_system"),
    )


class DatabaseService:
    """Small shared helper for safely executing parameterized SQL."""

    @staticmethod
    def execute_insert(query, values):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            return cursor.lastrowid
        except Exception:
            if connection and connection.is_connected():
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def fetch_one(query, values):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, values)
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def fetch_all(query, values=()):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, values)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
