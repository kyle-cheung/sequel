import sqlite3
import pandas as pd
import requests
import database
from database import fetch_all_table_structure

sequel_db = 'bi_tool.db'
textcortex_api_key = 'Bearer gAAAAABkMFEMlesLUwl9Uy6K4zZYUxtxsazlYOpSKP1_HASvA5EuoI0e2Xsd6o5EtWLXayMR_Rrqa1nT612wCsesvWb-gMf_U865T9HXIMuPf5RGmsfJBnRaEQTq5jaktjDO50tBVvRy'
textcortex_sql_generator_endpoint = "https://api.textcortex.com/v1/codes"

def store_user_query(query):
    response, sql_response, sql_results, status = generate_sql_query(query)
    print(sql_results)
    return {
        "status" : status,
        "sql_query" : sql_response,
        "sql_results": sql_results
    }


def construct_textcortex_api_data(question):
    table_structure = database.fetch_all_table_structure()
    payload = {
        "max_tokens": 1024,
        "mode": "python",
        "model": "icortex-1",
        "n": 1,
        "temperature": 0,
        "text": "SQLite Table Structure: " + str(table_structure) + " Question: " + question + " SQL Query: "
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": textcortex_api_key
    }

    return payload, headers

def generate_sql_query(question):
    """
    This function generates the SQL query by making a POST request to TextCortex API with
     the user question and the table structure
    :param question: user question
    :param table_structure: table structure of the database
    :return: SQL query
    """
    
    payload, headers = construct_textcortex_api_data(question)
    sql_query = ""

    response = requests.request("POST", textcortex_sql_generator_endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        # Execute SQL query and display results
        sql_query = response.json()['data']['outputs'][0]['text']
        print(f"Generated SQL query: {sql_query}")
        sql_results = query_database(sql_query)
    else:
        print("Oops, that didn't work. Can you rephrase your question?", response.text)
    # Close connection
    return response, sql_query, sql_results, "error" if response.status_code != 200 else "success"

def query_database(sql_query):
    try:
        with sqlite3.connect(sequel_db) as conn:
            # Fetch the results using pandas
            df = pd.read_sql_query(sql_query, conn)

            return df.to_dict('records')

    except Exception as e:
        print("Error while executing SQL query: ", e)
        return {
            "status": "error",
            "message" :str(e)
        }