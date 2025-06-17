import google.generativeai as genai
import os
from utils.promptutils import format_prompt  # 👈 Reusing same helper

# 🔐 Configure Gemini API Key
genai.configure(api_key=os.getenv("AIzaSyAyB_41yt2JxDyMEiC4MW6Xbp7Bylcfew0"))

# 🧠 Load concept detection prompt template
with open("prompts/concept_detection.prompt", "r") as f:
    prompt_template = f.read()

# Initialize Gemini Model
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

def detect_concepts(parsed_text: str) -> list:
    """
    Returns a list of concepts or skills detected in the text using Gemini.
    """
    prompt = format_prompt(prompt_template, text=parsed_text)
    response = gemini_model.generate_content(prompt)

    try:
        return [c.strip() for c in response.text.split(",") if c.strip()]
    except:
        return ["⚠️ Gemini model failed to respond properly."]
