from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from FinalBackend import UploadFile
from FinalBackend import GetResponse
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from authentication import register
from authentication import checkExisting
from authentication import checkLoginInfo

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for the specific route

# Ensure 'uploads' directory exists
uploads_dir = os.path.join('uploads')  # making the 'uploads' directory to store documents
os.makedirs(uploads_dir, exist_ok=True)

# username = ""

@app.route("/api/submit", methods=['POST'])
def submit_data():
    query = request.form.get('inputValue')
    username = request.form.get('username').lower()

    print(query)

    # Process the file as needed (e.g., save it to a folder)

    print("THIS IS USER",username)

    relevant_section,answer = GetResponse(query,username)  # see storeAndSearch.py for more details
    print(relevant_section)
    return jsonify({"relevantSection": relevant_section, "answer": answer})  # send this info to the frontend
   

@app.route("/api/upload", methods=['POST'])
def upload_data():
    username = request.form.get('username').lower()
    go = True
    i = 0
    latest_file = ""
    while go:
        file = request.files.get("file"+str(i))
        if file != None:
            i += 1
            print(file)
            file.save(os.path.join(uploads_dir, file.filename))
            filepath = os.path.join(uploads_dir, file.filename)
            #get username
            
            print("THIS IS USER for upload",username)
            UploadFile(filepath,username)
            latest_file = file.filename
        else:
            go = False
 

    return jsonify({"response": latest_file})

@app.route("/api/login", methods=['POST'])
def check_login():
    # global username
    username = request.form.get('username').lower()
    password = request.form.get('password')
    print(username, password)
    existing, account = checkLoginInfo(username, password)
    if (existing == "success"):
        # do something with the account variable (save it for later)
        pass
    print(existing)
    return jsonify({"message": existing})

@app.route("/api/register", methods=['POST'])
def register_user():
    # global username
    username = request.form.get('username').lower()
    password = request.form.get('password')
    print(username, password)
    existing = checkExisting(username)
    if existing != "username_error": # if the username is not already in the db
        register(username, password) # adds the users info to the pinecone db
    return jsonify({"message": existing})


if __name__ == '__main__':
    app.run(debug=True)
    
