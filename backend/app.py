from flask import Flask, request, jsonify, render_template, json
import os
import database
import re
import query_textcortex
import query_openai
import query_langchain

static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

app = Flask(__name__, template_folder='../frontend/templates', static_url_path='/static', static_folder=static_path)
gpt = query_langchain.init_conversation_chain()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    table_name = request.form["table_name"]
    
    if not table_name or not re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", table_name):
        return jsonify({"status": "error", "message": "Invalid table name"})
        
    sample_data = database.save_csv_to_db(file, table_name)
    return jsonify({"status": "success", "message": f"CSV file uploaded successfully as {table_name}", "sample_data": sample_data})

@app.route("/tables", methods=["GET"])
def get_tables():
    table_names = database.get_tables()
    return jsonify({"tables": table_names})

@app.route("/delete_table", methods=["DELETE"])
def delete_table():
    table_name = request.args.get("table_name")
    if table_name:
        try:
            database.delete_table(table_name)
            return jsonify({"status": "success", "message": f"Table {table_name} deleted successfully"})
        except Exception as e:
            print(e)
            return jsonify({"status": "error", "message": "An error occurred while deleting the table"})
    else:
        return jsonify({"status": "error", "message": "No table name provided"})

@app.route("/store_user_query", methods=["POST"])
def store_user_query():
    user_query = request.form["user_query"]
    # selected_model = request.form["selected_model"]
    selected_model = "gpt4"
    query_reponse = None

    if selected_model == "gpt3.5":
        query_response = query_openai.store_user_query(user_query)
    elif selected_model == "textcortex":
        query_response = query_textcortex.store_user_query(user_query)
    elif selected_model == "gpt4":
        gpt_response = gpt.predict(input=user_query)
        query_response = query_langchain.construct_response(gpt_response)

        
    print (query_response)
    query_response["sql_results"] = json.dumps(query_response["sql_results"])
    return jsonify({"status": query_response["status"], "message": query_response})

if __name__ == "__main__":
    app.run(debug=True)
