#SecondBrainVector@gmail.com
#SecondBrainVector1!
#https://www.pinecone.io/

import pandas as pd
from transformers import GPT2Tokenizer
import numpy as np
import textract
import os
#from dotenv import load_dotenv

# Load environment variables from the .env file
#load_dotenv()

# Access the API key using the environment variable
openai_api_key = os.getenv("OPENAIKEY")

from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key='d489c9e2-5765-423f-ab5a-5da2eabb2d14')

index = pc.Index("test2")


max_len = 450

loader = textract.process("exampleDoc.docx")

text_content = loader.decode("utf-8") # Decode bytes to string assuming utf-8 encoding




tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

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


#dattt = np.array(data_to_upsert[0][1], dtype=float)

data_to_upsert = [(str(row["id"]), np.array(row["vector"], dtype=float)) for index, row in df.iterrows()]


index.upsert(vectors=data_to_upsert) # insert new vectors or update the vector if the id was already created




# Get question from user
question = input("What's your question? ")

input_q1 = tokenizer.encode(question)

# Ensure the same length of input_ids for both sentences
input_q1 += [0] * (max_len - len(input_q1))

print(input_q1)

#return the top 1 value that matches the vector
return_vectors = index.query(
     vector=input_q1,
     top_k=3,
     include_values=True) # returns top_k matches


print(return_vectors)

print("Return sentence is: ")
vector0 = ' '.join(str(tokenizer.decode(return_vectors['matches'][0]['values'])).split())



import openai
openai.api_key = ""


completion = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": "given the context: " + vector0 + "answer this question ONLY!!!! using the info from the following context if the question cannot be answered with the info return a 'cannot be found': " + question}
])


print(completion.choices[0].message.content)
