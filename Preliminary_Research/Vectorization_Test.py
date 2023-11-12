from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import word_tokenize

# Sample documents
documents = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?",
]

# Tokenize using NLTK's word_tokenize
tokenized_documents = [word_tokenize(doc) for doc in documents]

# CountVectorizer (Bag of Words)
count_vectorizer = CountVectorizer()
X_count = count_vectorizer.fit_transform([' '.join(tokens) for tokens in tokenized_documents])

# TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform([' '.join(tokens) for tokens in tokenized_documents])

print(f"tokenized document: {tokenized_documents}")

# To see the vocabulary (unique words)
print("Vocabulary for CountVectorizer:")
print(count_vectorizer.get_feature_names_out())

print("\nVocabulary for TF-IDF Vectorizer:")
print(tfidf_vectorizer.get_feature_names_out())

# To see the vectorized representation of documents
print("\nVectorized representation for CountVectorizer:")
print(X_count.toarray())

print("\nVectorized representation for TF-IDF Vectorizer:")
print(X_tfidf.toarray())
