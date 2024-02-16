from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from  storeAndSearch import get_relevant_section
from LLMCall import get_answer


filepath = "uploads/exampleDoc2.0.pdf" #this is hardcoded please change this
api_key= "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" #insert your own key
 
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for the specific route
 
# Ensure 'uploads' directory exists
uploads_dir = os.path.join('uploads')  #making the 'uploads' directory to store documents
os.makedirs(uploads_dir, exist_ok=True)
 
@app.route("/api/submit", methods=['POST'])
def submit_data():
    query = request.form.get('inputValue')
    file = request.files.get('file')
    print(os.path.join(uploads_dir, file.filename))
    # Process the file as needed (e.g., save it to a folder)
    if file: #if the file exists, save it in 'uploads'
        file.save(os.path.join(uploads_dir, file.filename))
   
    #manipulated_string = manipulate_string(query)
    relevant_section= get_relevant_section(filepath, query, api_key)# see storeAndSearch.py for more details
    answer= get_answer(relevant_section, query, api_key)# see LLMCall.py for more details
    return jsonify({"relevantSection": relevant_section,"answer": answer}) #send this info to the frontend
 
   
   
 
def manipulate_string(input_string):
    return f"This is a manipulated string: {input_string}"
 
 
 
 
if __name__ == '__main__':
    app.run(debug=True)