import os
from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings
from rag.document_loader import load_documents

VECTOR_DB_PATH = "rag/faiss_index"

def build_vectorstore():
    documents = load_documents()
    embeddings = get_embeddings()
    vectordb = FAISS.from_documents(documents, embeddings)
    vectordb.save_local(VECTOR_DB_PATH)
    print("✅ Vectorstore built and saved.")

def load_vectorstore():
    embeddings = get_embeddings()
    return FAISS.load_local(VECTOR_DB_PATH, embeddings)
