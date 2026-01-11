import sqlite3
import sys

class DBHandler:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def insert_data(self, table: str, data: dict):
        """ Insert data into a table using a dict. """
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()

            if table == "DHT_data":
                cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, datetime('now'))", (data['temperature'], data['humidity']))
                conn.commit()

            if table == "soil_data":
                cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, datetime('now'))", (data['temperature'], data['moisture']))
                conn.commit()

    def get_data(self, statement: str):
        """ Execute an SQL statement and return data. Used outside this class for database access. """
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            data = cur.execute(statement).fetchall()
            list(data)
            
        return data

    def print_table(self, table: str):
        """ Print table contents. """
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            for row in cur.execute(f"SELECT * FROM {table}"):
                print(row)
