import sqlite3
from contextlib import closing
from pathlib import Path
from typing import List

class DataBase:
    def __init__(self, db_path: str):
        """Initialize the DataBase object.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        
    
    def execute(self, query: str, values: tuple):
        """Execute the given SQL query with sqlite3.

        Args:
            query (str): SQL query to execute.
            values (tuple): Values to insert into the query to prevent SQL injection.
        
        Returns:
            list: List of result rows.
        """
        with closing(sqlite3.connect(self.db_path)) as db_connection:
            with db_connection:
                cursor = db_connection.cursor()
                cursor.execute(query, values)
                result_rows = cursor.fetchall()
        return result_rows
                
    def executescript(self, script: str):
        """Execute the given SQL script with sqlite3.

        Args:
            script (str): SQL script containing multiple queries.
        
        Returns:
            list: List of result rows.
        """
        with closing(sqlite3.connect(self.db_path)) as db_connection:
            with db_connection:
                cursor = db_connection.cursor()
                cursor.executescript(script)
                result_rows = cursor.fetchall()
        return result_rows
        
    def executefile(self, sql_file_path: Path):
        """Execute the SQL script in the given file.

        Args:
            sql_file_path (Path): Path of the SQL file.
        
        Returns:
            list: List of result rows.
        
        Raises:
            FileNotFoundError: If the file is not found.
            PermissionError: If there is an issue opening the file.
        """
        try:
            with sql_file_path.open() as file:
                queries = file.read()
                result_rows = self.executescript(queries)
            return result_rows
        except FileNotFoundError:
            raise FileNotFoundError(f"SQL file not found: {sql_file_path}")
        except PermissionError:
            raise PermissionError(f"Permission error while opening SQL file: {sql_file_path}")
        
    def get_columns_names(self, table: str) -> List[str]:
        """Retrieve column names for the specified table.

        Args:
            table (str): Name of the table.

        Returns:
            List[str]: List of column names.
        """
        query = f"PRAGMA table_info({table});"
        result_rows = self.execute(query, ())
        return [description[1] for description in result_rows]
        
    def select_primary_key(self, table: str, primary_key_value: int, columns: list = None) -> dict:
        """Retrieve a record from the specified table based on the primary key.

        Args:
            table (str): Name of the table.
            primary_key_value (int): Primary key value to search for.
            columns (list): Optional list of columns to retrieve from the record. Defaults to None.
        
        Returns:
            dict: A dictionary with column names as keys and corresponding values.
        
        Raises:
            ValueError: If there is no matching record.
        """
        if columns is None:
            columns_clause = '*'
            columns = self.get_columns_names(table)
        else:
            columns_clause = ', '.join(columns)
        
        query = f"SELECT {columns_clause} FROM {table} WHERE id=?"
        result_rows = self.execute(query, (primary_key_value,))
        
        if result_rows:
            record = result_rows[0]
        else:
            raise ValueError("No matching record found.")
        
        return {column: value for column, value in zip(columns, record)}
    
    def insert_into_table(self, table_name: str, **values) -> int:
        """Insert a new row into the specified table with specified values.

        Args:
            table_name (str): Name of the table.
            values (dict): Dictionary of column names and their corresponding values.

        Returns:
            int: The ID of the newly inserted row.
        """
        columns = ', '.join(values.keys())
        placeholders = ', '.join('?' for _ in values)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with closing(sqlite3.connect(self.db_path)) as db_connection:
            with db_connection:
                cursor = db_connection.cursor()
                cursor.execute(query, tuple(values.values()))
                # Retrieve the ID of the newly inserted row
                row_id = cursor.lastrowid

        return row_id
    
    def search_into(self, table_name: str, columns: tuple, query: str) -> tuple:
        base_query = f"SELECT id FROM {table_name} WHERE "
        conditions = [f'{column} LIKE "%?%"' for column in columns]
        final_query = base_query + " OR ".join(conditions)
        
