# Crud Class for Sqlite

import sqlite3
import os

class SQLiteCRUD:
    def __init__(self, db_name):
        if not os.path.isfile(db_name):
            print("Error: DB does not exist.")    
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        try:
            # Create a table with the given columns
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
            self.cursor.execute(create_table_query)
            self.conn.commit()
#            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name, data):
        try:
            # Insert data into the table
            placeholders = ', '.join(['?'] * len(data))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            self.cursor.execute(insert_query, data)
            self.conn.commit()
#            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def read_data(self, table_name):
        try:
            # Retrieve all data from the table
            select_query = f"SELECT * FROM {table_name};"
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
            if result:
                for row in result:
                    print(row)
            else:
                print("No data found in the table.")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
    def describe(self):
      sql = """
      SELECT name FROM sqlite_schema 
      WHERE type IN ('table','view') 
      AND name NOT LIKE 'sqlite_%'
      ORDER BY 1;
      """
      self.cursor.execute(sql)
      result = self.cursor.fetchall()
      if result:
          for row in result:
              print(row)
    def get_data(self, table_name, column, condition_column, condition_value):
        try:
            # Retrieve data from the table based on a condition
            select_query = f"SELECT {column} FROM {table_name} WHERE {condition_column} = ?;"
            self.cursor.execute(select_query, (condition_value,))
            result = self.cursor.fetchall()
            if result:
                return result[0][0]
            else:
                print("No data found in the table.")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")              
    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        try:
            # Update data in the table based on a condition
            update_query = f"UPDATE {table_name} SET {column} = ? WHERE {condition_column} = ?;"
            self.cursor.execute(update_query, (new_value, condition_value))
            self.conn.commit()
 #           print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def delete_data(self, table_name, condition_column, condition_value):
        try:
            # Delete data from the table based on a condition
            delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
            self.cursor.execute(delete_query, (condition_value,))
            self.conn.commit()
  #          print("Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def close_connection(self):
        self.conn.close()
      #  print("Database connection closed.")

    def describe_table(self, table):
        # connect to the SQLite database.
        print("before")
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"PRAGMA table_info({table})")
        for row in self.cursor:
                print(row)
        print("after")
    def show_table(self):
        string_query = f"""
        SELECT
            name
        FROM
            sqlite_schema
        WHERE
            type ='table' AND
            name NOT LIKE 'squlite_%';
        """
        self.cursor.execute(string_query)
        rows = self.cursor.fetchall()
        print(rows)
        for row in rows:
            print("Hello")
            print(row)
    def print_table(self, table_name):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()

            if len(rows) == 0:
                print(f"The table '{table_name}' is empty.")
            else:
                # Print column headers
                col_names = [desc[0] for desc in self.cursor.description]
                print(", ".join(col_names))

                # Print data
                for row in rows:
                    print(", ".join(map(str, row)))

        except sqlite3.Error as e:
            print(f"Error reading data from the table: {e}")

class FileSystem:
    def __init__(self):
        db_name = "filesystem.db"
        crud = SQLiteCRUD(db_name)
        current_location = "0"

    def __buildDB(self):
        # Define table schema
        table_name = "files"
        columns = ["id INTEGER PRIMARY KEY", "pid INTEGER NOT NULL", "created TEXT", "modified TEXT", "size REAL","type TEXT","owner TEXT","group TEXT","permissions TEXT"]
        # Create table
        crud.create_table(table_name, columns)

    def __getFileId(self,**kwargs):
        """ Find a file id using current location + name
        """
        pass

    def list(self,**kwargs):
        """ List the files and folders in current directory
        """
        pass



    def chmod(self,**kwargs):
        """ Change the permissions of a file
        """
        pass
    

# Example usage:
if __name__ == "__main__":
    db_name = "my_database.sqlite"
    crud = SQLiteCRUD(db_name)
    
    # Define table schema
    table_name = "students"
    columns = ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]

    # Create table
    crud.create_table(table_name, columns)

    # Insert data
    data = (1, "Alice", 25)
    crud.insert_data(table_name, data)

    # Read data
    crud.read_data(table_name)

    # Update data
    crud.update_data(table_name, "age", 26, "name", "Alice")

    # Delete data
    #crud.delete_data(table_name, "name", "Alice")

    # Close the database connection
    crud.close_connection()