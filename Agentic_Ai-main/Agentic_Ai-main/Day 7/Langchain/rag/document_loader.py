import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader

def load_documents(folder_path: str = "data/curated_docs") -> list:
    documents = []

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(full_path)
        elif filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(full_path)
        else:
            continue

        docs = loader.load()
        documents.extend(docs)

    return documents
