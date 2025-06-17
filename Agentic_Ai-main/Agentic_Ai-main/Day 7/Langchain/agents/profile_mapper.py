import json
import os

def update_profile(profile_path: str, concepts: list) -> dict:
    """
    Adds new concepts to the user profile (if not already present).
    """
    if not os.path.exists(profile_path):
        profile = {"skills": []}
    else:
        with open(profile_path, "r") as f:
            profile = json.load(f)

    existing_skills = set(profile.get("skills", []))
    updated_skills = existing_skills.union(set(concepts))

    profile["skills"] = list(updated_skills)

    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)

    return profile
