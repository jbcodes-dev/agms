import sqlite3
import sys

class DBHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    
    def create_connection(self):
        """ Create connection to database. """
        self.conn = sqlite3.connect(self.db_file)
        self.create_cursor()

    def create_cursor(self):
        """ Create cursor for database navigation. """
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """ Close connection to database and purge cursor. """
        self.conn.close()
        self.conn = None
        self.cursor = None

    def insert_data(self, table: str, data: dict):
        """ Insert data into a table using a dict. """
        if table == "DHT_data":
            self.cursor.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, datetime('now'))", (data['temperature'], data['humidity']))
            self.conn.commit()

    def print_table(self, table: str):
        """ Print table contents. """
        for row in self.cursor.execute(f"SELECT * FROM {table}"):
            print(row)


