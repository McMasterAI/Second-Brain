#For testing LLM API

import openai
import cohere
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
		"question": "What should I study?",
		"context": "I am good at math, and I am really bad at physics."
	},
})

answer = answer_dict["answer"]
print(answer)

response_dict = createResponse({
	"inputs": "Make a plan for me to do well on my " + answer + " test.",
})

response = response_dict[0]["generated_text"]

print("\n" + response + "\n")





"""
# Hugging Face Basic Call

repository_id = "deepset/roberta-base-squad2"
API_token = " insert your own api token"

client = InferenceClient(model=repository_id, token=API_token)
inputs = {
            "question": "Tell me a story about monkeys"
            "context": "Monkeys eat apples, bananas, and carrots, but they prefer bananas. They love to go to the beach.",
        }
response = client.post(json=inputs)
print(response)

"""

"""
# Cohere Basic Call
API_key= "insert your own api token"
co = cohere.Client(API_key)
response = co.generate(
    prompt="Generate a summary about mcmaster engineering",
    max_tokens=20
)
print(response.generations[0].text)
"""



# ChatGPT APi Basic Call
openai.api_key = "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"

completion = openai.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "user", "content": "Tell me about McMaster University"}
                                            ])

print(completion.choices[0].message.content)

