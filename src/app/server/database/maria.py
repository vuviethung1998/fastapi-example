import numpy as np 
import pandas as pd 
import pymysql
from decouple import config  
from urllib.parse import urlparse

class MariaDB:
    def __init__(self) -> None:
        mysql_uri = urlparse(f"{config('DB_CONN')}")
        self.conn = self.__create_connection(mysql_uri)
        # self.cursor = self.conn.cursor()
        self.database = None
        self.table = None

    def set_database(self, db_name):
        self.database = db_name 
    
    def set_table(self, table_name):
        self.table = table_name 

    def __create_connection(self, parsed_uri):
        try:
            conn = pymysql.connect(
                host=parsed_uri.hostname,
                port=parsed_uri.port,
                user=parsed_uri.username,
                password=parsed_uri.password,
                db=parsed_uri.path[1:],  # Remove the leading '/'
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn 
        except pymysql.Error as e:
            print(f"Error: {e}")

    def create_database(self, db_name, query):
        try:
            # create cursor 
            with self.conn.cursor() as c:
                c.execute(query)
                print(f"Table '{db_name}' created successfully")
        except pymysql.Error as e:
            print(f"Error: {e}")

    def insert_many(self, table_name, data, columns):
        try:
            with self.conn.cursor() as c:
                # Create the INSERT query
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in range(len(columns))])})"
                # Execute the query for each row of data
                c.executemany(query, data)
                print(f"Insert data successfully")
            
            self.conn.commit()
            return data
        except pymysql.Error as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    def last_k_records(self, table_name, col='tradingdate', k=1):
        query = f'''SELECT * FROM {table_name}
            ORDER BY {col} DESC
            LIMIT {k};'''
        try:
            with self.conn.cursor() as c:
                c.execute(query)
                result = c.fetchone()
                print("Received data successfully!")
                df = pd.DataFrame.from_records([result])
                return df
        except pymysql.Error as e:
            print(f"Error: {e}")

    def upsert_many(self, table_name, data, cols, key_cols):
        try:
            with self.conn.cursor() as c:
                set_query = ', '.join([f"{col} = VALUES({col})" for col in cols if col not in key_cols])
                columns = ', '.join(cols)
                placeholders = ', '.join(['%s'] * len(cols))       
                # Combine the update and insert queries for the upsert operation
                upsert_query = f"""
                    INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE {set_query};
                """
                # Execute the upsert query for all rows in the DataFrame
                c.executemany(upsert_query, [row for row in data])
            self.conn.commit()
            print("Upserted data successfully!")

        except pymysql.Error as e:
            print(f"Error: {e}")

    def delete_many(self, table_name, column, value_delete):
        try:
            with self.conn.cursor() as c:
                # Create the DELETE query
                query = f"DELETE FROM {table_name} WHERE {column} = %s;"
                # Execute the query
                c.execute(query, (value_delete,))
                print("Delete data sucessfully!")
            # Commit the changes to the database
            self.conn.commit()
        except pymysql.Error as e:
            print(f"Error: {e}")
    
    def get_all_data(self, table_name):
        query = f"SELECT * FROM {table_name};"
        try:
            # Create the SELECT query
            # df = pd.read_sql(query, self.conn)
            # print(query)
            # return df
            with self.conn.cursor() as c:
                c.execute(query)
                df = c.fetchall()
                return df
        except pymysql.Error as e:
            print(f"Error: {e}")
    
    def get_all_data_match_condition(self, query):
        try:
            # Execute the query
            with self.conn.cursor() as c:
                c.execute(query)
                df = c.fetchall()
                return df
        except pymysql.Error as e:
            print(f"Error: {e}")
    
    def get_data_from_date_to_date(self, table_name, start_date, end_date, date_col='tradingdate'):
        try:
            # Create a cursor object
            with self.conn.cursor() as cursor:
                # Create the SELECT query with the date range condition
                query = f"SELECT * FROM {table_name} WHERE {date_col} BETWEEN %s AND %s;"
                
                # Execute the query
                cursor.execute(query, (start_date, end_date))

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Get column names from the cursor description
                column_names = [desc[0] for desc in cursor.description]
        except pymysql.Error as e:
            print(f"Error: {e}")

        # Convert the result to a DataFrame
        df = pd.DataFrame(rows, columns=column_names)
        return df
    
    def get_data_by_date(self, table_name, date, date_col='tradingdate'):
        try:
            # Create a cursor object
            with self.conn.cursor() as cursor:
                # Create the SELECT query with the date range condition
                query = f"SELECT * FROM {table_name} WHERE {date_col} LIKE %s;"
                
                # Execute the query
                cursor.execute(query, (date))

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Get column names from the cursor description
                column_names = [desc[0] for desc in cursor.description]
        except pymysql.Error as e:
            print(f"Error: {e}")

        # Convert the result to a DataFrame
        df = pd.DataFrame(rows, columns=column_names)
        return df
    
    def delete_table(self, table_name):
        try:
            # Create a cursor object
            with self.conn.cursor() as cursor:
                # Create the DROP TABLE query
                query = f"DROP TABLE IF EXISTS {table_name};"
                
                # Execute the query
                cursor.execute(query)
                print(f"Table '{table_name}' dropped successfully")

            # Commit the changes
            self.conn.commit() 
        except pymysql.Error as e:
            print(f"Error: {e}")

    def disconnect(self):
        try:
            self.conn.close()
        except pymysql.Error as e:
            print(f"Error: {e}")

if __name__=="__main__":
    db = MariaDB()
    db.set_database('vnstock')
    db.set_table('company')
    db.delete_many('alo', 'info', 'No Inf')