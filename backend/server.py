from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from FinalBackend import UploadFile
from FinalBackend import GetResponse

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for the specific route

# Ensure 'uploads' directory exists
uploads_dir = os.path.join('uploads')  # making the 'uploads' directory to store documents
os.makedirs(uploads_dir, exist_ok=True)

@app.route("/api/submit", methods=['POST'])
def submit_data():
    query = request.form.get('inputValue')
    print(query)

    # Process the file as needed (e.g., save it to a folder)

    api_key = "sk-"  # insert your own key
    relevant_section = GetResponse(query, api_key)  # see storeAndSearch.py for more details
    answer = " Answer from the backend "  # see LLMCall.py for more details
    print(relevant_section[0])
    return jsonify({"relevantSection": relevant_section[0], "answer": answer})  # send this info to the frontend
   

@app.route("/api/upload", methods=['POST'])
def upload_data():
    api_key = "sk-"
    go = True
    i = 0
    while go:
        file = request.files.get("file"+str(i))
        if file != None:
            i += 1
            print(file)
            file.save(os.path.join(uploads_dir, file.filename))
            filepath = os.path.join(uploads_dir, file.filename)
            UploadFile(filepath, api_key)
        else:
            go = False
           
   
    return jsonify({"reponse": "Files Uploaded"})

if __name__ == '__main__':
    app.run(debug=True)
