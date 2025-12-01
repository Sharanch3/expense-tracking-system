import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection():
    """
    Context manager for MySQL database connections.
    Using this class with the 'with' statement ensures automatic
    connection setup, commit/rollback handling, and cleanup.
    
    """

    def __init__(
            self,
            host: str = os.getenv("DB_HOST"),
            user: str = os.getenv("DB_USER"),
            password: str = os.getenv("DB_PASSWORD"),
            database: str = os.getenv("DB_NAME")
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None


    def __enter__(self):
        """Establishes a MySQL connection and returns cursor."""

        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database

        )

        self.cursor = self.connection.cursor(dictionary=True)

        return self.cursor


    def __exit__(self, exc_type, exc_val, exc_tb):
        """automatic resource cleanup"""
        
        if self.cursor:
            self.cursor.close()

        if self.connection:
            if not (exc_type or exc_val or exc_tb):
                self.connection.commit()
            else:  
                self.connection.rollback()

            self.connection.close()