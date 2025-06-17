from rag.retriever import get_relevant_docs
import google.generativeai as genai
from utils.promptutils import format_prompt  # We'll create this helper

import os

# 🔐 Set your Gemini API key securely
genai.configure(api_key=os.getenv("AIzaSyAyB_41yt2JxDyMEiC4MW6Xbp7Bylcfew0"))

# 🧠 Load the prompt template
with open("prompts/followup_recommender.prompt", "r") as f:
    prompt_template = f.read()

# Initialize Gemini Model
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

def recommend_next_steps(skills: list) -> str:
    """
    Uses RAG to fetch documents and recommend follow-up actions using Gemini.
    """
    docs = get_relevant_docs(", ".join(skills))
    docs_str = "\n".join([doc.page_content for doc in docs])

    prompt = format_prompt(prompt_template, skills=skills, docs=docs_str)

    response = gemini_model.generate_content(prompt)

    try:
        return response.text.strip()
    except:
        return "⚠️ Gemini model returned an unexpected response."
