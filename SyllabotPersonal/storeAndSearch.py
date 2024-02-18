import os
import getpass
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import textract

import nltk
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Set NLTK data path
nltk.data.path.append('/Users/iainmacdonald/nltk_data')

# Download 'punkt' tokenizer
nltk.download('punkt', download_dir='/Users/iainmacdonald/nltk_data')



filepath = "uploads/exampleDoc2.0.pdf"
api_key= "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"
query = "who is princess peach"

def get_relevant_section(filepath,query,api_key):
 
    loader = UnstructuredWordDocumentLoader(filepath)

    ogText = textract.process(filepath)
    print("Doc1.0",ogText)
    print("")

    from collections import namedtuple

    Document = namedtuple("Document", ["page_content", "metadata"])
    
    ogText = ogText.decode()

    document = Document(page_content=ogText, metadata={'source': 'uploads/exampleDoc.docx'})
    documents = [document]
    text_splitter = CharacterTextSplitter(chunk_size=350, chunk_overlap=20)

    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_documents(docs, embeddings)
    docs = db.similarity_search(query)
 
    return docs[0].page_content
 
#print(get_relevant_section(filepath,query,api_key))