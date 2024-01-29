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
    user_input = print(QandA(input_data))

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
    upserting(file.filename)
    return {"response": "POST REQUEST RECEIVED"}


#METHODS
def manipulate_data(input_data):
    return (input_data + " this is the response from the backend!")


















import pandas as pd
from transformers import GPT2Tokenizer
import numpy as np
import textract
import os
from pinecone import Pinecone, ServerlessSpec

openai_api_key = os.getenv("OPENAIKEY")
pc = Pinecone(api_key='d489c9e2-5765-423f-ab5a-5da2eabb2d14')
index = pc.Index("batest")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


def upserting(FileName):
    max_len = 550
    loader = textract.process(FileName)
    text_content = loader.decode("utf-8")
    words = text_content.split(" ")
    chunk_size = 350
    word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    embedded_chunks = [tokenizer.encode(" ".join(chunk)) for chunk in word_chunks]

    # Pad the chunks to have the same length
    padded_chunks = [(chunk + [0] * (max_len - len(chunk))) for chunk in embedded_chunks]

    # Now 'padded chunks' contains the embedded and padded chunks of 350 words each
    df = pd.DataFrame(
        data={
        "id": range(1, len(word_chunks) + 1),
        "vector": padded_chunks
    })
    df

    data_to_upsert = [(str(row["id"]), np.array(row["vector"], dtype=float)) for index, row in df.iterrows()]
    index.upsert(vectors=data_to_upsert) # insert new vectors or update the vector if the id was already created





def QandA(Question):
    max_len = 550
    # Get question from user
    question = Question

    input_q1 = tokenizer.encode(question)
    print(input_q1 , " ")


    # Ensure the same length of input_ids for both sentences
    input_q1 += [0] * (max_len - len(input_q1))



    #return the top 1 value that matches the vector
    return_vectors = index.query(
        vector=input_q1,
        top_k=3,
        include_values=True) # returns top_k matches


    print("Return sentence is: ")
    vector0 = ' '.join(str(tokenizer.decode(return_vectors['matches'][0]['values'])).split())
    print(vector0)

    import openai
    openai.api_key = ""


    completion = openai.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": "you only have this context for information: " + vector0 + "answer this question ONLY!!!! using the info from the following context if the question cannot be answered with the info return a 'cannot be found': " + question}
    ])

    Answer = (completion.choices[0].message.content)
    return Answer





# RUNS THE FLASK APP
if __name__ == '__main__':
    app.run(debug=True)