import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI

# Setup
load_dotenv()

# Embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Gemini LLM
llm = GoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyBMeZz1rVfBNO7b0O0I4kcV07obEED4vFk",
    temperature=0.2
)

# Streamlit UI
st.set_page_config(page_title="RAG QA In-Memory", layout="wide")
st.title("📄 RAG QA  AI PDF Question Answering")

# Upload PDFs
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# Process PDFs
def process_documents(files):
    all_docs = []
    for file in files:
        # Save temporarily
        temp_path = os.path.join("temp", file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(file.read())

        loader = PyPDFLoader(temp_path)
        documents = loader.load()
        all_docs.extend(documents)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)
    return chunks

# Main app flow
if uploaded_files:
    with st.spinner("🔍 Processing PDFs and generating embeddings..."):
        chunks = process_documents(uploaded_files)
        vectorstore = FAISS.from_documents(chunks, embeddings)

        # Ask query
        query = st.text_input("Ask a question from the uploaded PDFs")
        if query:
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

            with st.spinner("🤖 Generating answer..."):
                result = qa_chain({"query": query})
                st.markdown("### ✅ Answer")
                st.write(result["result"])

                st.markdown("### 🗨️ Here's what I found inside the PDF:")
                for doc in result["source_documents"]:
                    page = doc.metadata.get("page", "N/A")
                    # Fix line breaks by joining and trimming
                    content = ' '.join(doc.page_content.split())[:500] + "..."
                    st.markdown(f"📄 From page {page}:")
                    st.write(f"💬 {content}")
                    st.markdown("---")

else:
    st.info("Please upload at least one PDF file to begin.")
