def truncate_text(text: str, max_words: int = 200) -> str:
    """
    Truncate text to a fixed number of words.
    """
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

def format_skills_list(skills: list) -> str:
    """
    Convert a skill list into a readable comma-separated string.
    """
    return ", ".join(skills)
