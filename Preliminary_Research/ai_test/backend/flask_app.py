from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
#from langchain.document_loaders import PyPDFLoader


"""
HOW TO RUN!!!

to run the python backend, do the following in a terminal:
cd backend
.\venv\Scripts\activate     **this step might be different if on mac
python flask_app.py


to run the react frontend:
cd frontend
npm start

"""

app = Flask(__name__)
CORS(app)


from flask import Response

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route("/api/get", methods=['GET'])
def get_data():
    global user_input
    return {"response": [user_input]}
    

@app.route("/api/submit", methods=['POST', 'GET', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def submit_data():
    input_data = request.json.get('inputValue')
    print("bad")
    global user_input
    user_input = manipulate_data(input_data)
    get_data()
    return {"response": ["response:", input_data]}


def manipulate_data(input_data):
    return (input_data*2)

@app.route("/api/files", methods=['POST', 'GET'])
@cross_origin(headers=['Content-Type'])
def get_files():
    file = request.files['file']
    print(file)
    #file.save(file.filename)
    #file2 = open("sample txt file.txt", 'r')
    #print(file2.readlines())
    names.append(file.filename)
    return ""


@app.route("/api/getfiles", methods=['GET'])
def get_file_names():
    return {"response": names}

"""
usernames = ["kristian", "iain", "aiden"]
for username in usernames:
    @app.route("/api/"+username, methods=['GET'])
    def get_thesetings():

        return {"response": username}
"""




user_input = ""
names = []

if __name__ == '__main__':
    app.run(debug=True)