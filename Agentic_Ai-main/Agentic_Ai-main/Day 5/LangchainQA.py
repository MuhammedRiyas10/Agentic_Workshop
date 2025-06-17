import streamlit as st
import PyPDF2
import google.generativeai as genai
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set page config as the FIRST Streamlit command
st.set_page_config(page_title="📘 PDF Study Assistant", layout="centered")

# Configure the Gemini API
GEMINI_API_KEY = "AIzaSyDonBzngKXhdxepVLmsjKdZZtD5T6clmiE"  # Replace with a VALID Gemini API key (get from Google Cloud Console)
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini API: {e}. Please ensure your API key and model name are correct.")
    st.stop()

# Display success message after page config
st.success("✅ Gemini API initialized successfully.")

# Custom LLM wrapper for Gemini to use with LangChain
class GeminiLLM(LLM):
    def _call(self, prompt, stop=None):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")

    @property
    def _llm_type(self):
        return "gemini"

# Initialize the custom Gemini LLM for LangChain
llm = GeminiLLM()

# Function: Extract text from PDF
def extract_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        st.write(f"📄 Extracted text length: {len(text)} characters")
        return text
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
        return ""

# Function: Format extracted text into a professional paragraph
def format_extracted_text(extracted_text):
    cleaned_text = re.sub(r'\s+', ' ', extracted_text.strip())
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    paragraph = " ".join(sentences)
    if len(sentences) <= 1:
        phrases = re.split(r',\s*|\sand\s*|\s*-\s*', cleaned_text)
        phrases = [phrase.strip() for phrase in phrases if phrase.strip()]
        paragraph = ". ".join(phrases) + "."
    if paragraph:
        paragraph = paragraph[0].upper() + paragraph[1:]
    return paragraph if paragraph else "No meaningful content could be extracted from the PDF."

# Function: Summarize text using LangChain + Gemini
def summarize_text(text):
    try:
        # Split the text into chunks for LangChain processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text[:3000])
        documents = [Document(page_content=chunk) for chunk in chunks]

        # Use LangChain's summarize chain
        summarize_chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
        summary = summarize_chain.run(documents)
        st.write("📝 Summarization completed using LangChain.")
        return summary
    except Exception as e:
        raise Exception(f"Summarization failed: {str(e)}")

# Function: Generate MCQs using LangChain + Gemini
def generate_mcqs(summary):
    try:
        prompt = PromptTemplate(
            input_variables=["summary"],
            template="""
            Based on the summary below, generate 2 multiple-choice questions with 4 options each.
            Clearly mention the correct option at the end like: Answer: c)

            Summary:
            {summary}
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        mcqs = chain.run(summary=summary)
        st.write("❓ MCQ generation completed using LangChain.")
        return mcqs
    except Exception as e:
        raise Exception(f"MCQ generation failed: {str(e)}")

# Streamlit UI
st.title("🧠 PDF Summarizer & Quiz Generator (Gemini + LangChain)")

uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("📖 Extracting text..."):
        extracted_text = extract_pdf_text(uploaded_file)

    if extracted_text:
        st.success("✅ PDF content extracted!")
        
        # Format and display the extracted content
        formatted_content = format_extracted_text(extracted_text)
        st.subheader("🔍 Extracted Content from PDF")
        st.write(formatted_content)

        if st.button("📝 Generate Summary"):
            with st.spinner("✏ Summarizing using Gemini and LangChain..."):
                try:
                    summary = summarize_text(extracted_text)
                    st.subheader("📌 Summary of the PDF")
                    st.write(summary)
                    st.session_state['summary'] = summary  # Store summary in session state
                    st.success("✅ Summary generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error during summarization: {e}")

        # Check if summary exists in session state before showing MCQ button
        if 'summary' in st.session_state and st.session_state['summary']:
            if st.button("❓ Generate MCQs"):
                with st.spinner("🤖 Generating quiz questions..."):
                    try:
                        mcqs = generate_mcqs(st.session_state['summary'])
                        st.subheader("📋 Generated MCQs")
                        st.text_area("MCQs", mcqs, height=250)
                        st.success("✅ MCQs generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error during MCQ generation: {e}")
        else:
            st.warning("⚠ Please generate the summary first to proceed with MCQ generation.")
    else:
        st.error("❌ No text could be extracted from the PDF.")

