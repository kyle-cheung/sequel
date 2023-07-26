import sqlite3
import pandas as pd
import database
from database import fetch_all_table_structure
from dotenv import load_dotenv
import os
import re
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

sequel_db = 'bi_tool.db'
load_dotenv()  # Load environment variables from .env file
openai_api_key = os.environ['OPENAI_API_KEY']

def construct_response(gpt_response):
        sql_response = extract_query(gpt_response)
        sql_results = query_database(sql_response)
        return {
            "status" : "success",
            "sql_query" : sql_response,
            "sql_results": sql_results
        }
    
def init_llm():
    template = """
        You are a data analyst employed at our DVD rental store called Pagila.
        You helps us write SQL in PostgreSQL dialect.
        When you write SQL you follow 5 rules
        1. Write your SQL in a single block wrapped in triple back ticks "```"
        2. Always use table aliases
        3. Always use CTEs when necessary
        4. Never use subqueries
        5. Only describe your query in SQL comments
        Using the table structure provided, answer the question correctly making sure to think step by step and following the rules above.
        Respond with, "I don't know", if both of these apply:
        1. The question is not related to the database or company
        2. The question cannot be answered using the database
        Table structure (database): {table_structure}
        Question: {user_prompt}
        Answer: 
    """
    prompt = PromptTemplate(template = template, input_variables=["user_prompt", "table_structure"])
    chat = ChatOpenAI(model_name="gpt-4", temperature=0.1, openai_api_key=openai_api_key)
    llm_chain = LLMChain(prompt=prompt, llm=chat)
    return prompt, llm_chain, chat

def init_system_template():
    table_structure = "{" + repr(database.fetch_all_table_structure()) + "}"
    system_message = f"""
        You are a data analyst employed at our company, which is a bike sales store.
        You helps us write SQL in SQLite dialect.
        When you write SQL you follow 5 rules
            1. Write your SQL in a single block wrapped in triple back ticks "```"
            2. Always use table aliases
            3. Always use CTEs when necessary
            4. Never use subqueries
            5. Only describe your query in SQL comments
        Using the database provided, answer the question correctly making sure to think step by step and following the rules above.
        Respond with, "I don't know", if these 2 conditions apply:
            1. The question is not related to the database or company
            2. The question cannot be answered using the database
        If any of these conditions apply, ask the user clarifying questions:
            1. The question is vague
        Database table structure: {table_structure}
    """
    return system_message

def init_conversation_chain():
    system_prompt = init_system_template()
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    
    llm = ChatOpenAI(temperature=0.1, openai_api_key=openai_api_key, model_name="gpt-4")
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    return conversation

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

    # Check if query list is not empty
    if query:
        # Get the first item in the list (which should be the matched string)
        query_string = query[0]
        query_string = re.sub(r'^.*?[\r\n]?\b(WITH|SELECT)\b', r'\1', query_string, flags=re.IGNORECASE)
        print (f"Here is your query {query_string}")
        return query_string
    else:
        print("No query found")
        return None
