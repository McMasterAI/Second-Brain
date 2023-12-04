#SecondBrainVector@gmail.com
#SecondBrainVector1!
#https://www.pinecone.io/





#uploading pdf 
import pinecone
import pandas as pd

pinecone.init(api_key="d489c9e2-5765-423f-ab5a-5da2eabb2d14", environment="gcp-starter")
index = pinecone.Index("test")

#https://docs.google.com/document/d/1cS1TBS-nr5zXRfmm3Li3qMA4v6VUxegEmHpRXg7Ru00/edit?usp=sharing
from langchain.document_loaders import PyPDFLoader
from sklearn.metrics.pairwise import cosine_similarity
from transformers import GPT2Tokenizer
import numpy as np

# Load pre-trained GPT2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load PDF and extract text
loader = PyPDFLoader("example4.pdf")
pages = loader.load_and_split()

# Extracted text from the PDF joined into single string
document_text = ''.join([page.page_content for page in pages])

document_embedding = tokenizer.encode(document_text)
# 'document_embedding' now contains the vector representation of the entire document

df = pd.DataFrame(
    data={
        "id": ["FirstDoc"],
        "vector": [document_embedding]
    })
df

index.upsert(vectors=(zip(df.id, df.vector)))  # insert new vectors or update the vector if the id was already created





#asking question,



# Get question from user
question = input("What's your question? ")



input_q1 = tokenizer.encode(question)


# Ensure the same length of input_ids for both sentences
max_len = 3624
input_q1 += [0] * (max_len - len(input_q1))

#return the top 1 value that matches the vector
return_vectors = index.query(
    vector=[input_q1],
    top_k=1,
    include_values=True) # returns top_k matches


print("Return sentence is: ")
vector = return_vectors['matches'][0]['values']

#returns decoded vector
return_document = tokenizer.decode(vector)

from huggingface_hub import InferenceClient
import requests


# Made using hugging face 
API_URL1 = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct" #falcon-7b model is used for text generation
API_URL2 = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2" #roberta-base-squad2 model is used for answering questions
headers = {"Authorization": "Bearer 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"}


def getAnswer(payload):
	response = requests.post(API_URL2, headers=headers, json=payload) # use the answering questions API to get an answer
	return response.json()

def createResponse(payload):
	response = requests.post(API_URL1, headers=headers, json=payload)
	return response.json()
	
answer_dict = getAnswer({
	"inputs": {
		"question": question,
		"context": return_document
	},
})

answer = answer_dict["answer"]
#print(answer)

import openai

# ChatGPT APi Basic Call
openai.api_key = "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"

completion = openai.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "user", "content": "given the context: " + return_document + "answer this question ONLY using the info from the context: " + question}
                                            ])

print(completion.choices[0].message.content)
