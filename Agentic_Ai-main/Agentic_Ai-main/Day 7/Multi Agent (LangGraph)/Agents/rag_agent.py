import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Define paths
DATA_DIR = "data"
INDEX_PATH = "embeddings/faiss_index"

# Create FAISS index if it doesn't exist
def create_vector_store():
    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_DIR, filename)
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDEX_PATH)

# Load FAISS index
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

# RAG Agent Function
def rag_node(state):
    query = state["query"]

    # Create index once if not exists
    if not os.path.exists(INDEX_PATH):
        create_vector_store()

    # Load index and search
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query, k=4)
    context = "\n\n".join([doc.page_content for doc in results])

    return {**state, "rag_result": context}
