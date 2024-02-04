import sqlite3
from contextlib import closing
from pathlib import Path
from typing import List, Tuple

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
        
    def select_primary_key(self, table: str, primary_key_value: int, columns: list|None = None) -> dict:
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
        result_rows = self.execute(query, (str(primary_key_value),))
        
        if result_rows:
            record = result_rows[0]
        else:
            raise ValueError("No matching record found.")
        
        return {column: value for column, value in zip(columns, record)}
    
    def unique_to_id(self, table: str, column: str, key: str) -> int:
        """
        Retrieve the unique identifier (id) of a record from a specified table
        where a specified column matches a given key.

        Args:
            table (str): The name of the table to query.
            column (str): The column to check for a match.
            key (str): The value to match in the specified column.

        Returns:
            int: The id of the matching record.

        Raises:
            ValueError: If no matching record is found.
        """
        query = f"SELECT id FROM {table} WHERE {column}=?"
        result_rows = self.execute(query, (key,))
        
        if result_rows:
            record = result_rows[0]
            return record[0]
        
        raise ValueError("No matching record found.")


    
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
    
    def search_into(self, table_name: str, columns: tuple, query: str, sort_by: str = None, desc: bool = False) -> tuple:
        """
        Search for data in a table based on the specified query and columns.

        Args:
            table_name (str): Name of the table to perform the search in.
            columns (tuple): Tuple of column names to search in.
            query (str): Search query.
            sort_by (str, optional): Name of the column to sort the results by. Default is None.
            desc (bool, optional): Indicates whether sorting should be done in descending order. Default is False.

        Returns:
            tuple: A tuple containing the search results.
        """
        base_query = f"SELECT id FROM {table_name} WHERE "
        conditions = [f"{column} LIKE '%' || ? || '%'" for column in columns]
        sort = f"ORDER BY {sort_by}" if sort_by else ""
        variation = " DESC" if desc else ""
        final_query = base_query + " OR ".join(conditions) + sort + variation
        print(final_query)
        return self.execute(final_query, (query, ))

    def set(self, table_name: str, column: str, id: int, value):
        """
        Update the value of a column for a specified entry in a table.

        Args:
            table_name (str): Name of the table to perform the update in.
            column (str): Name of the column to update.
            id (int): ID of the entry to update.
            value: New value to set for the column.
        """
        query = f"UPDATE {table_name} SET {column} = ? WHERE id = ?"
        return self.execute(query, (value, id))

    def delete(self, table_name: str, id: int) -> None:
        """
        Delete a record from the specified table based on the provided id.

        Args:
            table_name (str): The name of the table from which to delete the record.
            id (int): The unique identifier of the record to be deleted.
        """
        query = f"DELETE FROM {table_name} WHERE id=?"
        self.execute(query, (id,))