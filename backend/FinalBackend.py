from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
import numpy as np    
import os
import getpass
import openai
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_DOCDATA_API_KEY = os.getenv("PINECONE_DOCDATA_API_KEY")
PINECONE_LOGIN_API_KEY = os.getenv("PINECONE_LOGIN_API_KEY")

pc = Pinecone(api_key=PINECONE_DOCDATA_API_KEY)  # create a Pinecone instance

def UploadFile(filepath,index_name):
    pinecone_index = pc.Index(index_name)
    print("THIS IS INDEX NAME! ", index_name)
    """
    Uploads a file for processing and indexing.

    Parameters:
        filepath (str): Path to the file to be uploaded.

    Returns:
        str: A success message indicating successful upload.
    """

    # Determine the type of file loader based on the file extension
    if filepath.endswith('.docx'):
        loader = UnstructuredWordDocumentLoader(filepath)
    elif filepath.endswith('.pdf'):
        loader = PyPDFLoader(filepath)
    else:
        raise ValueError("Unsupported file format. Supported formats: .docx, .pdf")
    
    # Load the content of the file
    file_content = loader.load()
    for i in range(len(file_content)):
        page_content = file_content[i].page_content

        # Preprocess the text content (replace newline characters, remove non-alphanumeric characters, and convert to lowercase)
        page_content = page_content.replace('\n', ' ')
        page_content = re.sub(r'[^a-zA-Z0-9\s]', '', page_content).lower()
        print(page_content)

        # Update the page content with preprocessed content
        file_content[i].page_content = page_content

    # Split the text content into chunks for processing
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=20, separator=" ")
    docs = text_splitter.split_documents(file_content)

    # Initialize OpenAI Embeddings service
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
 
    # Extract text content from each document
    doc_contents = [doc.page_content for doc in docs]

    # Embed the text content using OpenAI Embeddings service
    embedded_docs = embeddings.embed_documents(doc_contents)

    # Upsert embedded vectors into Pinecone index
    for i, doc in enumerate(docs):
        print(docs[i])
        pinecone_index.upsert(vectors=[{"id": str(i), "values": embedded_docs[i], "metadata": {"text_chunk": docs[i].page_content}}])

    # Return a success message
    return "Successfully Uploaded"


def GetResponse(query,index_name):
    pinecone_index = pc.Index(index_name)

    """
    Generates a response to a query using OpenAI's GPT model based on matching text chunks.

    Parameters:
        query (str): The query for which a response is to be generated.

    Returns:
        tuple: A tuple containing the text chunk used as context and the generated response.
    """

    # Initialize OpenAI Embeddings service
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Query Pinecone index to get top matching vectors
    return_vectors = pinecone_index.query(
        vector=embeddings.embed_query(query),
        top_k=10,
        include_values=True
    )  # returns top_k matches

    # Extract metadata for each matched vector
    metadata_list = []
    for i, match in enumerate(return_vectors['matches']):
        vector_id_to_fetch = match['id']
        metadata_result = pinecone_index.fetch([vector_id_to_fetch])
        metadata = metadata_result['vectors'][vector_id_to_fetch]['metadata']
        metadata_list.append(metadata)

    # Get the text chunk for the first matched metadata
    gpt_send = metadata_list[0]['text_chunk']

    # Set OpenAI API key
    openai.api_key = OPENAI_API_KEY

    # Generate response using GPT model
    completion = openai.chat.completions.create(model="gpt-4-0125-preview",
        messages=[
        {"role": "user", "content": "Based on this background information ONLY: " + gpt_send + "ONLY use that background information word for word to answer this question: " + query}
    ])

    # Extract and store the generated response
    send_back = completion.choices[0].message.content

    # Return the context text chunk and the generated response
    return gpt_send, send_back
