import json
import os

PROFILE_PATH = "profiles/profile.json"

def update_profile(skills):
    os.makedirs("profiles", exist_ok=True)
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            profile = json.load(f)
    else:
        profile = {"skills": []}

    new_skills = [s.strip("*•- ").strip() for s in skills if s.strip()]
    profile["skills"] = list(set(profile["skills"] + new_skills))

    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)
