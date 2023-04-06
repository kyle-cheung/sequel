import sqlite3
import pandas as pd

DATABASE_FILE = "bi_tool.db"

def save_csv_to_db(file, table_name, overwrite=False):
    # Read the CSV file using Pandas
    df = pd.read_csv(file)

    conn = sqlite3.connect(DATABASE_FILE)

    if overwrite:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Save the DataFrame to the database
    print(f"Saving DataFrame to database with table name: {table_name}")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Saved DataFrame to database with table name: {table_name}")
    conn.close()

    # Get the first 5 rows of the DataFrame as JSON
    sample_data = df.head(5).to_json(orient="records")

    return sample_data

def table_exists(table_name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def get_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    return [table[0] for table in tables]

def get_table_fields(table_name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    fields = cursor.fetchall()
    conn.close()

    return [field[1] for field in fields]

def get_tables_and_columns():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [table[0] for table in cursor.fetchall()]

    tables = []
    for table_name in table_names:
        # Get the list of columns for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [column[1] for column in cursor.fetchall()]

        tables.append({"name": table_name, "columns": columns})

    conn.close()
    return tables

