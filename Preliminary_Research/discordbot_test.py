import discord
import os
from sentence_transformers import SentenceTransformer

client = discord.Client(intents=discord.Intents.default())

model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2') #for vectorizing

TOKEN = "MTE4MDY4MDM3ODg5ODQ1NjY5Ng.G5YOeN.Ye86TjjOYsEqezO7Rjs02zVl5SSDwgyTE_JPtc" #discord bot token

global i
i = 0

@client.event
async def on_message(message):

    global i
    if message.author == client.user: # so that the bot does not respond to its own messages
        return


    if message.content == "1" and i == 0:
        await message.channel.send("What is the question you would like me to vectorize?")
        i=1

    elif message.content == "2" and i == 0:
        await message.channel.send("What is the question you would like me to answer?")
        i=2

    elif i == 1: #vectorize the question
        question = message.content
        question_embedding = model.encode([question])
        print(question_embedding)
        await message.channel.send("Question has been vectorized!")
        i=0
    
    elif i == 2:
        question = message.content
        await message.channel.send("Good question, let me think about it...")
        i=0

    else:
        await message.channel.send("Hello I am the chatbot! Please make a selection:")
        await message.channel.send("(1) Vectorize a question")
        await message.channel.send("(2) Answer a question")
        #await messasge.channel.send("(3) Upload Information")
        i=0
    

@client.event
async def on_connect():
    print("The bot is now online!")


client.run(TOKEN)