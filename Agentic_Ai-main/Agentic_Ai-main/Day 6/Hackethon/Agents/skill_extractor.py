from typing import List

def extract_skills(text: str) -> List[str]:
    if not text.strip():
        return ["There is no text provided."]
    known_skills = ["Python", "prompt engineering", "UI/UX", "Figma", "FlutterFlow", "team collaboration"]
    return [skill for skill in known_skills if skill.lower() in text.lower()]
