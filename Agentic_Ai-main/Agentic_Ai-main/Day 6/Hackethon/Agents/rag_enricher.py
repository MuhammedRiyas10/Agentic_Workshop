def enrich_skills(skills):
    enriched = {}
    for skill in skills:
        link = f"https://www.google.com/search?q={skill}+programming"
        enriched[skill] = f"[🔍 Learn more about {skill}]({link}) — click to explore."
    return enriched
