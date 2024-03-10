from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_DOCDATA_API_KEY = os.getenv("PINECONE_DOCDATA_API_KEY")
PINECONE_LOGIN_API_KEY = os.getenv("PINECONE_LOGIN_API_KEY")

def register(username, password):
    pc = Pinecone(api_key=PINECONE_LOGIN_API_KEY)  # create a Pinecone instance
    pinecone_index = pc.Index("login-info")

    # api_key = "KEYHERE"
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    embedded_username = embeddings.embed_query(username)

    # creates a new index named the users username 
    # this is their unique server to upload to
    index_name = username
    if index_name not in pc.list_indexes().names():
    # Do something, such as create the index
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
                cloud="aws",
                region="us-west-2"
            )
        )

    pinecone_index.upsert(vectors=[{"id": username, "values": embedded_username, "metadata": {"password": password, "pinecone_account": "unique id"}}])
    print(username + " is registered in the pincone db")


def getClosestUserInfo(username):
    pc = Pinecone(api_key=PINECONE_LOGIN_API_KEY)  # create a Pinecone instance
    pinecone_index = pc.Index("login-info")   

    #uploading a first user
    # embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # embedded_username = embeddings.embed_query("Admin")
    # pinecone_index.upsert(vectors=[{"id": "Admin", "values": embedded_username, "metadata": {"password": "Admin", "pinecone_account": "unique id"}}])
    #end 

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    embedded_username = embeddings.embed_query(username)

    return_vectors = pinecone_index.query(
        vector=embedded_username,
        top_k=1,
        include_values=True
    )  # returns top_k matches

    metadata_list = []
    closest_username = ""
    # from all vectors returned from pinecone db, we will get the value of the closest to the username
    for i, match in enumerate(return_vectors['matches']): 
        vector_id_to_fetch = match['id']
        closest_username = vector_id_to_fetch
        metadata_result = pinecone_index.fetch([vector_id_to_fetch])
        metadata = metadata_result['vectors'][vector_id_to_fetch]['metadata']
        metadata_list.append(metadata)

    closest_password = metadata_list[0]['password']
    account = metadata_list[0]['pinecone_account']

    return closest_username, closest_password, account

def checkExisting(username):
    
    closest_username, closest_password, account = getClosestUserInfo(username)

    if (username == closest_username):
        return "username_error" # username already exists in the db
    else:
        return "success" # username does not exist, and new account can be created
        

def checkLoginInfo(username, password):

    closest_username, closest_password, account = getClosestUserInfo(username)

    if (username == closest_username):
        if(password == closest_password):
            return "success", account
        else:
            return "password_error", None
    else:
        return "username_error", None


