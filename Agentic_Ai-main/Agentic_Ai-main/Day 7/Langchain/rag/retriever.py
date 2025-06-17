from rag.vector_store import load_vectorstore

def get_relevant_docs(query: str, k: int = 4):
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)
    return docs
