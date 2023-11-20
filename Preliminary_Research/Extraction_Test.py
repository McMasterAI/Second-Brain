#This file will be used to extract the relevant plain text from the vector database after the similairity search has been performed

"""
This code first tokenizes the text using gpt2 .encode() function into a vector that can be stored in pinecone.
The vectors need to be converted to numpy arrays and resized for the similarity search.
The vectors are also padded with zeros so that they are the same size as each other **May affect the similarity search**.
The similar document can then be converted back to text using the .decode() function.
"""

from sklearn.metrics.pairwise import cosine_similarity
from transformers import GPT2Tokenizer
import numpy as np

# Sample sentences
sentence1 = "In the heart of the bustling city, towering skyscrapers reach towards the sky, their reflective surfaces glistening in the sunlight. Neon lights illuminate the vibrant streets below, where diverse cultures converge. Commuters rush to catch the morning train, creating a symphony of urban energy that defines the city's pulse."
sentence2 = "The heart of a bustling city"

# Load pre-trained GPT2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Encode the tokens
input_ids1 = tokenizer.encode(sentence1)
input_ids2 = tokenizer.encode(sentence2)

# Ensure the same length of input_ids for both sentences
max_len = max(len(input_ids1), len(input_ids2))
input_ids1 += [0] * (max_len - len(input_ids1))
input_ids2 += [0] * (max_len - len(input_ids2))

# Convert the token IDs to NumPy arrays
array1 = np.array(input_ids1).reshape(1, -1)  # Add batch dimension
array2 = np.array(input_ids2).reshape(1, -1)  # Add batch dimension

# Calculate cosine similarity using NumPy arrays
similarity = cosine_similarity(array1, array2)

print(f"Similarity between the sentences: {similarity[0, 0]}")

print(tokenizer.decode(input_ids1, skip_special_tokens=True))
