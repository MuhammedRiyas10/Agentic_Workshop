import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyDonBzngKXhdxepVLmsjKdZZtD5T6clmiE")

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def summarizer_node(state):
    # Choose from available results or fallback to the query
    collected = state.get("web_result") or state.get("rag_result") or state["query"]

    prompt = f"""
    Summarize the following content clearly and concisely:

    {collected}
    """

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
    except Exception as e:
        summary = f"❌ Error in summarization: {e}"

    return {**state, "final_output": summary}
