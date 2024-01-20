#SecondBrainVector@gmail.com
#SecondBrainVector1!
#https://www.pinecone.io/





#uploading pdf 
import pinecone
import pandas as pd

pinecone.init(api_key="", environment="gcp-starter")
index = pinecone.Index("test")

#https://docs.google.com/document/d/1cS1TBS-nr5zXRfmm3Li3qMA4v6VUxegEmHpRXg7Ru00/edit?usp=sharing
from langchain.document_loaders import PyPDFLoader
from transformers import GPT2Tokenizer
import numpy as np

max_len = 1536

# Load pre-trained GPT2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load PDF and extract text
loader = PyPDFLoader("example4.pdf")
pages = loader.load_and_split()

# Embeds each page and adds them to an array
embedded_pages = [tokenizer.encode(page.page_content) for page in pages]

padded_pages = [(page + [0] * (max_len - len(page))) for page in embedded_pages]

df = pd.DataFrame(
    data={
        "id": range(1, len(pages) + 1),
        "vector": padded_pages
    })
df

data_to_upsert = [(str(row["id"]), row["vector"]) for index, row in df.iterrows()]

index.upsert(vectors=data_to_upsert)  # insert new vectors or update the vector if the id was already created

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
vector0 = return_vectors['matches'][0]['values']
vector1 = return_vectors['matches'][1]['values']
vector2 = return_vectors['matches'][2]['values']

print("vector1 = " + vector0)
print("vector2 = " + vector1)
print("vector3 = " + vector2)


### UPDATE LLM TO TAKE TOP 3 DOCUMENT PAGES

import openai

# ChatGPT APi Basic Call
openai.api_key = ""

completion = openai.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "user", "content": "given the context: " + return_document + "answer this question ONLY using the info from the context: " + question}
                                            ])

print(completion.choices[0].message.content)
