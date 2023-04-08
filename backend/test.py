import query_openai
import sqlite3
import os

sequel_db = 'bi_tool.db'

DATABASE = 'bi_tool.db'
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

if __name__ == '__main__':
    print(os.environ.get('openai_api_key'))
    # Ask user for question
    while question := input(f"What would you like to ask to {DATABASE} database? "):
        query_openai.generate_sql_query(question)
