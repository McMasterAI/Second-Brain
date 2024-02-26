from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

def register(username, password):
    pc = Pinecone(api_key='ec87c2c6-6c1f-4d66-a70a-031ff0ee3eef')  # create a Pinecone instance
    pinecone_index = pc.Index("login-info")   
    api_key = "KEYHERE"
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    embedded_username = embeddings.embed_query(username)
    pinecone_index.upsert(vectors=[{"id": username, "values": embedded_username, "metadata": {"password": password, "pinecone_account": "unique id"}}])
    print(username + " is registered in the pincone db")


def getClosestUserInfo(username):
    pc = Pinecone(api_key='ec87c2c6-6c1f-4d66-a70a-031ff0ee3eef')  # create a Pinecone instance
    pinecone_index = pc.Index("login-info")   
    api_key = "KEYHERE"
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    embedded_username = embeddings.embed_query(username)

    return_vectors = pinecone_index.query(
        vector=embedded_username,
        top_k=1,
        include_values=True
    )  # returns top_k matches

    metadata_list = []
    closest_username = ""
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
        return "username_error"
    else:
        return "success"
        

def checkLoginInfo(username, password):

    closest_username, closest_password, account = getClosestUserInfo(username)

    if (username == closest_username):
        if(password == closest_password):
            return "success", account
        else:
            return "password_error", None
    else:
        return "username_error", None


