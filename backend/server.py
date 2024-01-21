# FLASK BACKEND
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) # allows cross origin requests

#SET UP GLOBAL VARIABLES
user_input = ""
file_names = []

#ROUTES
@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route("/api/get", methods=['GET'])
def get_data():
    global user_input
    return {"response": [user_input]}

@app.route("/api/submit", methods=['POST', 'GET', 'OPTIONS'])
def submit_data():
    input_data = request.json.get('inputValue')

    global user_input
    user_input = manipulate_data(input_data)

    get_data()
    return {"response": "POST REQUEST RECEIVED"}

@app.route("/api/getfiles", methods=['GET'])
def get_file_names():
    return {"response": file_names}

@app.route("/api/files", methods=['POST', 'GET', 'OPTIONS'])
def submit_files():
    file = request.files['file']
    file.save(file.filename)
    file_names.append(file.filename)
    return {"response": "POST REQUEST RECEIVED"}


#METHODS
def manipulate_data(input_data):
    return (input_data + " this is the response from the backend!")


# RUNS THE FLASK APP
if __name__ == '__main__':
    app.run(debug=True)