#For testing LLM API

import openai
import cohere
from huggingface_hub import InferenceClient


"""
# Hugging Face Basic Call

repository_id = "deepset/roberta-base-squad2"
API_token = "insert api key"

client = InferenceClient(model=repository_id, token=API_token)
inputs = {
            "question": "What is a monkeys favorite fruit", 
            "context": "Monkeys eat apples, bananas, and carrots, but they prefer bananas"
        }
response = client.post(json=inputs)
print(response)
"""


"""
# Cohere Basic Call
API_key= "insert api key"
co = cohere.Client(API_key)
response = co.generate(
    prompt="Generate a summary about mcmaster engineering",
    max_tokens=20
)
print(response.generations[0].text)
"""


"""
# ChatGPT APi Basic Call
openai.api_key = "insert api key"

completion = openai.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "user", "content": "Tell me about McMaster University"}
                                            ])

print(completion.choices[0].message.content)
"""
