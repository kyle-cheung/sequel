import query_openai
import sqlite3
import openai

sequel_db = 'bi_tool.db'
openai_api_key = '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'
openai.api_key = openai_api_key

DATABASE = 'bi_tool.db'
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

if __name__ == '__main__':
    # Ask user for question
    while question := input(f"What would you like to ask to {DATABASE} database? "):
        query_openai.generate_sql_query(question)
