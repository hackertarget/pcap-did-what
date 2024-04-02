#!/usr/bin/python3
import sqlite3
import os
import csv

def create_table_from_log(cursor, table_name, columns):
    if not columns:  # Check if the columns list is empty
        raise ValueError(f"No columns found for table {table_name}")
    column_definitions = ', '.join([f'"{col}" TEXT' for col in columns])
    create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({column_definitions});'
    cursor.execute(create_table_sql)

def insert_data_from_log(cursor, table_name, columns, data):
    placeholders = ', '.join(['?' for _ in columns])
    column_names = ', '.join([f'"{col}"' for col in columns])
    insert_sql = f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders});'
    cursor.executemany(insert_sql, data)

def convert_zeek_logs_to_sqlite(db_name, directory):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            table_name = os.path.splitext(filename)[0].replace('-', '_')  # Ensure table names are valid SQLite identifiers
            log_path = os.path.join(directory, filename)

            with open(log_path, 'r') as file:
                reader = csv.reader(file, delimiter='\t')
                columns = []
                for row in reader:
                    if row[0].startswith('#fields'):
                        columns = [col.replace('.', '_') for col in row[1:]]  # Adjusted to handle '#fields'
                        break  # Stop after finding the columns

                if not columns:
                    print(f"No columns extracted for {filename}.")
                    continue

                create_table_from_log(cursor, table_name, columns)

                data = [row for row in reader if not row[0].startswith('#')]  # Skip comment lines
                insert_data_from_log(cursor, table_name, columns, data)

    conn.commit()
    conn.close()

# Example usage
directory_path = '/data/'  # Update this to the path of your Zeek log files
db_name = 'zeek_logs.db'
convert_zeek_logs_to_sqlite(db_name, directory_path)

