import sqlite3
import pandas as pd
import openai
import database
from database import fetch_all_table_structure
from dotenv import load_dotenv
import os
import re

sequel_db = 'bi_tool.db'
load_dotenv()  # Load environment variables from .env file
openai.api_key = os.environ['OPENAI_API_KEY']

def store_user_query(query):
    response, sql_response, sql_results, status = generate_sql_query(query)
    print(sql_results)
    return {
        "status" : status,
        "sql_query" : sql_response,
        "sql_results": sql_results
    }

def generate_sql_query(question):
    """
    This function generates the SQL query by making a POST request to OpenAI GPT-3 API with
     the user question and the table structure
    :param question: user question
    :return: SQL query
    """
    table_structure = database.fetch_all_table_structure()

    prompt = f"""
        You are a data analyst employed at our company, which is a DVD rental store called Pagila.
        You helps us write SQL in SQLite dialect.
        When you write SQL you follow these 5 rules:
            1. Write your SQL in a single block wrapped in triple back ticks "```"
            2. Always use table aliases
            3. Always use CTEs when necessary
            4. Never use subqueries
            5. Only describe your query in SQL comments
        Using the database provided, answer future questions correctly making sure to think step by step and following the rules above.
        Respond with, "I don't know", if these 2 conditions apply:
            1. The question is not related to the database or company
            2. The question cannot be answered using the database
        If the question is at all vague, ask the user to clarify.
        Question: \"\"\"{question}\"\"\"
        SQLite Table Structure: {str(table_structure)}
    """
    

    sql_results = None
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content" : prompt}],
            max_tokens=1000,
            n=1,
            temperature=0.1,
        )
        sql_query = extract_query(response.choices[0].message.content.strip())
        print(prompt)
        print(response)

        if sql_query:
            print(f"Generated SQL query: {sql_query}")
            sql_results = query_database(sql_query)
            status = "success"
        else:
            print("Oops, that didn't work. Can you rephrase your question?")
            status = "error"
            sql_results = None

        
        return response, sql_query, sql_results, status

    except Exception as e:
        print("Error while calling GPT-3 API: ", e)
        status = "error"
        sql_query = ""
        sql_results = None

        return None, sql_query, sql_results, status

def query_database(sql_query):
    try:
        with sqlite3.connect(sequel_db) as conn:
            # Fetch the results using pandas
            df = pd.read_sql_query(sql_query, conn)

            return df.to_dict('records')

    except sqlite3.Error as e:  # Catch a more specific exception
        print("Error while executing SQL query: ", e)
        return {
            "status": "error",
            "message" :str(e)
        }

def extract_query(sql_query):
    pattern = r"```sql(.*?)```"
    query = re.findall(pattern, sql_query, re.DOTALL)
    query = query[0]
    query = re.sub(r'^.*?[\r\n]?\b(WITH|SELECT)\b', r'\1', query, flags=re.IGNORECASE)
    print (f"Here is your query {query}")
    return query