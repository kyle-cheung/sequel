import sqlite3
import pandas as pd

DATABASE_FILE = "bi_tool.db"

def save_csv_to_db(file, table_name):
    df = pd.read_csv(file)

    with sqlite3.connect(DATABASE_FILE) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    sample_data = df.head(5).to_json(orient="records")
    return sample_data

def get_tables():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
    return tables

def delete_table(table_name):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    return "success"
