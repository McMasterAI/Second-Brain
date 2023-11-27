#This file will be used to extract the relevant plain text from the vector database after the similairity search has been performed

"""
This code first tokenizes the text using gpt2 .encode() function into a vector that can be stored in pinecone.
The vectors need to be converted to numpy arrays and resized for the similarity search.
The vectors are also padded with zeros so that they are the same size as each other **May affect the similarity search**.
The similar document can then be converted back to text using the .decode() function.
"""

import pinecone
import pandas as pd

pinecone.init(api_key="d489c9e2-5765-423f-ab5a-5da2eabb2d14", environment="gcp-starter")
index = pinecone.Index("test")

from sklearn.metrics.pairwise import cosine_similarity
from transformers import GPT2Tokenizer
import numpy as np

# Get question from user
question = input("What's your question? ")


# Sample sentences
sentence1 = "In the heart of the bustling city, towering skyscrapers reach towards the sky, their reflective surfaces glistening in the sunlight. Neon lights illuminate the vibrant streets below, where diverse cultures converge. Commuters rush to catch the morning train, creating a symphony of urban energy that defines the city's pulse."
sentence2 = "The heart of a bustling city"
sentence3 = "Luigi, Mario, Bowser, Peach, Wario"
sentence4 = "Classical music is the best genre of music"
sentence5 = "12345678910"


# Load pre-trained GPT2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Encode the tokens
input_ids1 = tokenizer.encode(sentence1)
input_ids2 = tokenizer.encode(sentence2)
input_ids3 = tokenizer.encode(sentence3)
input_ids4 = tokenizer.encode(sentence4)
input_ids5 = tokenizer.encode(sentence5)
input_q1 = tokenizer.encode(question)


# Ensure the same length of input_ids for both sentences
max_len = max(len(input_ids1), len(input_ids2),len(input_ids3),len(input_ids4),len(input_ids5),len(input_q1))
input_ids1 += [0] * (max_len - len(input_ids1))
input_ids2 += [0] * (max_len - len(input_ids2))
input_ids3 += [0] * (max_len - len(input_ids3))
input_ids4 += [0] * (max_len - len(input_ids4))
input_ids5 += [0] * (max_len - len(input_ids5))
input_q1 += [0] * (max_len - len(input_q1))

# Create lists of vectors and their names
df = pd.DataFrame(
    data={
        "id": ["array1","array2","array3","array4","array5"],
        "vector": [input_ids1,input_ids2,input_ids3,input_ids4,input_ids5]
    })
df

# Uploads vectors to Pinecone database
index.upsert(vectors=(zip(df.id, df.vector)))  # insert new vectors or update the vector if the id was already created

#return the top 1 value that matches the vector
return_vectors = index.query(
    vector=[input_q1],
    top_k=1,
    include_values=True) # returns top_k matches

print("Return sentence is: ")
vector = return_vectors['matches'][0]['values']

print(tokenizer.decode(vector))