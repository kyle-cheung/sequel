Activate virtual environment with:
```
source venv/bin/activate
```

At a high level my goal is: create a tool that accepts text input to query a database.
This can be achieved by a few milestones
1. Establish a connection to a database: let's work on this part first, and this is achieved by accepting, uploading, processing, and displaying the CSV uploads that represent tables in a database
2. Have a text input
3. Send the text input and relevant schema information via API to OpenAI GPT3 to then create the SQL query which we will pass to the database

Let's try and tackle 1 from the beginning. I will provide you the template in which we want to work. In my project directory called sequel, we want to split the backend and frontend files into separate directories.
-backend: hold all backend python files
-frontend: hold all frontend files
The first build you should attempt should be able to do these things:
1. Have a button that allows the user to choose a CSV file from their computer. This button should be at the center of the webpage
2. Once the file is chosen the user can enter a name for the file. This name is used as the table name once it is uploaded to the database. This text input should appear to the right of the choose file button
3.  Have a button that says upload, where we then upload the chosen file to the SQLite database with the specified name from step2
4. Once the upload is successful, below the upload button it will display a message "You have successfully uploaded your CSV as <table_name>" 
5. Display the first 5 rows of the new table along with its headers below the message in step 4

sequel/
|-- backend/
|   |-- app.py
|   |-- database.py
|-- frontend/
|   |-- templates/
|   |   |-- index.html
|   |-- static/
|   |   |-- styles.css
|   |   |-- upload.js
|   |   |-- tables.js