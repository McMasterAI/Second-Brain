import textract
import re

def preprocess_text(document_path):
    # Extract text from the document
    loader = textract.process(document_path)
    text_content = loader.decode("utf-8")
    processed_file = open("SeparatedFile2",'w')
 
    # Remove non-alphabetic characters and convert to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_content).lower()
 
    # Split the text into a list of words
    words = cleaned_text.split()
    processed_file.write(cleaned_text)
    return words
 
filePath= "BreakingBad.docx"
print(preprocess_text(filePath))