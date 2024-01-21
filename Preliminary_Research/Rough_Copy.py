#SecondBrainVector@gmail.com
#SecondBrainVector1!
#https://www.pinecone.io/

import pinecone
import pandas as pd
from langchain.document_loaders import PyPDFLoader
from transformers import GPT2Tokenizer
import numpy as np
import textract

pinecone.init(api_key="d489c9e2-5765-423f-ab5a-5da2eabb2d14", environment="gcp-starter")
index = pinecone.Index("test")


max_len = 1536

loader = textract.process("exampleDoc.docx")

text_content = loader.decode("utf-8") # Decode bytes to string assuming utf-8 encoding

print("text content")
print(text_content)
print("")
print("")
print("")



tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

words = text_content.split(" ")

print("words")
print(words)
print("")
print("")
print("")



chunk_size = 350
word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]


embedded_chunks = [tokenizer.encode(" ".join(chunk)) for chunk in word_chunks]


# Pad the chunks to have the same length
padded_chunks = [(chunk + [0] * (max_len - len(chunk))) for chunk in embedded_chunks]

# Now 'padded chunks' contains the embedded and padded chunks of 350 words each
print("padded chunks")
print(padded_chunks)
print("")
print("")
print("")



df = pd.DataFrame(
    data={
      "id": range(1, len(word_chunks) + 1),
      "vector": padded_chunks
    })
df

data_to_upsert = [(str(row["id"]), row["vector"]) for index, row in df.iterrows()]

index.upsert(vectors=data_to_upsert) # insert new vectors or update the vector if the id was already created


# Get question from user
question = input("What's your question? ")

input_q1 = tokenizer.encode(question)

# Ensure the same length of input_ids for both sentences
input_q1 += [0] * (max_len - len(input_q1))



#return the top 1 value that matches the vector
return_vectors = index.query(
     vector=input_q1,
     top_k=3,
     include_values=True) # returns top_k matches


print("Return sentence is: ")
vector0 = ' '.join(str(tokenizer.decode(return_vectors['matches'][0]['values'])).split())
vector1 = ' '.join(str(tokenizer.decode(return_vectors['matches'][1]['values'])).split())
vector2 = ' '.join(str(tokenizer.decode(return_vectors['matches'][2]['values'])).split())

print("vector0 - ",vector0)
print("vector1 - ",vector1)
print("vector2 - ",vector2)


import openai
openai.api_key = "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"


completion = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": "given the context: " + vector0 + vector1 + vector2 + "answer this question ONLY using the info from the following context if the question cannot be answered with the info return a 'cannot be found': " + question}
])


print(completion.choices[0].message.content)

