#SecondBrainVector@gmail.com
#SecondBrainVector1!
#https://www.pinecone.io/


#spaces before end of sentence with !
#change the question from ! to ? 

import random
import pandas as pd
from transformers import GPT2Tokenizer
import numpy as np
import textract
import os
#from dotenv import load_dotenv

# Load environment variables from the .env file
#load_dotenv()

# Access the API key using the environment variable
openai_api_key = os.getenv("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")

from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key='d489c9e2-5765-423f-ab5a-5da2eabb2d14') # create a pinecone instance

index = pc.Index("test4") #creates an index, a data structure for vector embeddings


max_len = 550

loader = textract.process("BreakingBad.docx")#extracts text from provided document

text_content = loader.decode("utf-8") # Decode bytes to string assuming utf-8 encoding




tokenizer = GPT2Tokenizer.from_pretrained("gpt2")#using Hugging face's tokenizer

words = text_content.split(" ")#creates list of individual words from document, split by spaces



chunk_size = 290
word_chunks = []
for i in range(0, len(words), chunk_size):
    chunk = words[i:i + chunk_size]
    word_chunks.append(chunk)

#word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]#put this in for loop form


embedded_chunks = [tokenizer.encode(" ".join(chunk)) for chunk in word_chunks]


# Pad the chunks to have the same length
padded_chunks = [(chunk + [100] * (max_len - len(chunk))) for chunk in embedded_chunks]
print("Length padded ", len(padded_chunks[0]))
print("Length padded ", len(padded_chunks[1]))



# Now 'padded chunks' contains the embedded and padded chunks of 350 words each




df = pd.DataFrame(
    data={
    "id": range(1, len(word_chunks) + 1),
    "vector": padded_chunks
  })
df


#dattt = np.array(data_to_upsert[0][1], dtype=float)

data_to_upsert = [(str(row["id"]), np.array(row["vector"], dtype=float)) for index, row in df.iterrows()]


index.upsert(vectors=data_to_upsert) # insert new vectors or update the vector if the id was already created




# Get question from user
question = input("What's your question? ")

input_q1 = tokenizer.encode(question)
print(input_q1 , " ")





for i in range(max_len - len(input_q1)):
    input_q1 = input_q1 + [random.randint(1, 200)]



# Ensure the same length of input_ids for both sentences
print("QUESTION ",tokenizer.decode(input_q1))



#return the top 1 value that matches the vector
return_vectors = index.query(
     vector=input_q1,
     top_k=3,
     include_values=True) # returns top_k matches


print("Return sentence is: ")
vector0 = ' '.join(str(tokenizer.decode(return_vectors['matches'][0]['values'])).split())
print(vector0)

import openai
openai.api_key = "KEYHERE"


completion = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": "you only have this context for information: " + vector0 + "answer this question ONLY!!!! using the info from the following context if the question cannot be answered with the info return a 'cannot be found': " + question}
])


print(completion.choices[0].message.content)

