from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
import numpy as np    
import os
import getpass

filepath = "exampleDoc.docx"
api_key= "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"
pc = Pinecone(api_key='d489c9e2-5765-423f-ab5a-5da2eabb2d14')  # create a Pinecone instance
pinecone_index = pc.Index("iaintest1")




def UploadFile(filepath,api_key):
    loader = UnstructuredWordDocumentLoader(filepath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=350, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    doc_contents = [doc.page_content for doc in docs]
    
    # Embedding and indexing
    embedded_docs = embeddings.embed_documents(doc_contents)
    for i, doc in enumerate(docs):

        print(len(embedded_docs[i]))
        pinecone_index.upsert(vectors=[{"id": str(i), "values": embedded_docs[i], "metadata": {"text_chunk": docs[i].page_content}}])


UploadFile(filepath,api_key)










query = "Which character is bowser?"
api_key= "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"
pc = Pinecone(api_key='d489c9e2-5765-423f-ab5a-5da2eabb2d14')  
pinecone_index = pc.Index("iaintest1")

def GetResponse(query, api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    return_vectors = pinecone_index.query(
        vector=embeddings.embed_query(query),
        top_k=10,
        include_values=True
    )  # returns top_k matches
    metadata_list = []
    
    for i, match in enumerate(return_vectors['matches']):
        vector_id_to_fetch = match['id']
        metadata_result = pinecone_index.fetch([vector_id_to_fetch])
        metadata = metadata_result['vectors'][vector_id_to_fetch]['metadata']
        metadata_list.append(metadata)
    
    return metadata_list

print(GetResponse(query, api_key)[0])






