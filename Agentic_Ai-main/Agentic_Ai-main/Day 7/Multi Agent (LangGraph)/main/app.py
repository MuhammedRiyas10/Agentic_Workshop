import streamlit as st
import fitz  # PyMuPDF
from graphs.langgraph_setup import initialize_graph
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# UI setup
st.set_page_config(page_title="LangGraph Research AI", layout="centered")
st.title("🔎 Multi-Agent Research & Summarization System")

# Input query
query = st.text_input("Enter your research question:")

# PDF Upload
uploaded_file = st.file_uploader("📄 Optionally upload a PDF for RAG", type="pdf")

# Extract PDF text
pdf_text = ""
if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        pdf_text = "\n".join(page.get_text() for page in doc)

    # Show preview of extracted content
    if pdf_text.strip():
        st.subheader("📄 Extracted PDF Content Preview")
        st.code(pdf_text[:1000], language="text")  # First 1000 characters
    else:
        st.warning("⚠️ No extractable text found in this PDF.")

# Run Agents Button
if st.button("Run Agents") and query:
    with st.spinner("🤖 Agents thinking..."):
        graph = initialize_graph()
        result = graph.invoke({
            "query": query,
            "uploaded_pdf_text": pdf_text.strip() if pdf_text else None
        })

        answer = result.get("final_output", "⚠️ No output generated.")
        st.success("✅ Answer Generated!")
        st.markdown("📋 **Final Answer:**")
        st.markdown(answer)
