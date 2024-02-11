import os
import getpass
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


filepath = "uploads\exampleDoc.docx"
api_key= "key"
query = "Which character is a plumber?"

def get_relevant_section(filepath,query,api_key):

    loader = UnstructuredWordDocumentLoader(filepath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=350, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_documents(docs, embeddings)

    
    docs = db.similarity_search(query)

    return docs[0].page_content

#print(get_relevant_section(filepath,query,api_key))

