# Import required libraries
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
import database
import os


# Get the absolute path to the frontend static folder
static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

# Initialize a Flask application with the absolute path to the frontend static folder
app = Flask(__name__, template_folder='../frontend/templates', static_url_path='/static', static_folder=static_path)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask app
CORS(app)

# Route for handling CSV file uploads
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    table_name = request.form["table_name"]
    overwrite = request.form.get("overwrite", False)

    if database.table_exists(table_name) and not overwrite:
        return jsonify({"status": "exists", "message": "A table with this name already exists."})

    sample_data = database.save_csv_to_db(file, table_name, overwrite=bool(overwrite))
    return jsonify({"status": "success", "message": "CSV file uploaded successfully", "sample_data": sample_data})



# Route for processing user queries
@app.route("/query", methods=["POST"])
def query():
    # Retrieve the user query from the request
    user_query = request.json["query"]
    
    # Process the query and generate a response
    response = database.process_query(user_query)
    
    # Return the response as a JSON object
    return jsonify(response)

@app.route("/")
def index():
    print("Inside index()")
    return render_template("index.html")

@app.route("/get_tables")
def get_tables():
    tables = database.get_tables_and_columns()
    return jsonify(tables)

@app.route("/get_table_fields", methods=["GET"])
def get_table_fields():
    table_name = request.args.get("table_name")
    fields = database.get_table_fields(table_name)
    return jsonify({"fields": fields})


# Main entry point of the application
if __name__ == "__main__":
    
    # Run the Flask application with debug mode enabled
    app.run(debug=True)
