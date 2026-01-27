import sqlite3

class DBHandler:
    def __init__(self, db_file: str):
        """
        Initialise DBHandler with provided database filename.
        
        db_file: string for database filename.
        """

        self.db_file = db_file
    
    def insert_data(self, table: str, data: dict[str, float]):
        """ 
        Insert provided data into table. 

        table: string containing the table name.
        data: dict[str, float] containing the column names with appropriate sensor readings.
        """

        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()

            if table == "air_data":
                cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, datetime('now'))", (data['temperature'], data['humidity']))
                conn.commit()

            if table == "soil_data":
                cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, datetime('now'))", (data['temperature'], data['moisture']))
                conn.commit()
            
            if table == "growth_snapshots":
                cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, datetime('now'))", (data['path'],))
                conn.commit()

    def get_data(self, statement: str) -> list:
        """
        Return a list of rows.
        
        statement: string for SQL statement.
        """

        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            data = cur.execute(statement).fetchall()
            list(data)
            
        return data

    def print_table(self, table: str):
        """
        Print each row in a table.
        
        table: string for table to print.
        """

        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            for row in cur.execute(f"SELECT * FROM {table}"):
                print(row)
