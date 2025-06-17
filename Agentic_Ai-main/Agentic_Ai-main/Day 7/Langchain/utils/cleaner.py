import re

def clean_text(text: str) -> str:
    """
    Removes extra whitespace, URLs, emojis, and special characters.
    """
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"\s+", " ", text)     # Normalize whitespace
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # Remove emojis/non-ASCII
    return text.strip()
