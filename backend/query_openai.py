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

    prompt = (
        f"\nPretend you are a SQL expert name Sequel. Sequel has 70 years of experience, the SQL Sequel writes is always the most optimized and most efficient."
        "\nThere are 4 things Sequel ALWAYS does. 1: Sequel only returns SQL code 2: Sequel always uses table aliases 3: Sequel always uses common table expressions when they can 4: Sequel never uses subqueries. "
        "\nSequel, please write a query using SQLite dialect for the question below based on the SQLite table structure described below. Please wrap the query in triple back ticks: `"
        f"\nQuestion: \"\"\"{question}\"\"\""
        f"SQLite Table Structure: {str(table_structure)} "
    )

    sql_results = None
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content" : prompt}],
            max_tokens=500,
            n=1,
            temperature=0.8,
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
    pattern = r"```(.*?)```"
    query = re.findall(pattern, sql_query, re.DOTALL)
    query = query[0]
    query = re.sub(r'^.*?[\r\n]?\b(WITH|SELECT)\b', r'\1', query, flags=re.IGNORECASE)
    print (f"Here is your query {query}")
    return query