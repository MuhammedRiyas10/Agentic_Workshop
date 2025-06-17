from langchain_community.embeddings import OpenAIEmbeddings

def get_embeddings():
    return OpenAIEmbeddings()  # Replace with HuggingFaceEmbeddings if needed
