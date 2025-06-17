from agents.input_parser import parse_input
from agents.concept_detector import detect_concepts
from agents.profile_mapper import update_profile
from agents.recommender_agent import recommend_next_steps

# Step 1: Input Parser Node
def input_node(state):
    source_path = state["source"]
    parsed_text = parse_input(source_path)
    return {"parsed_text": parsed_text, **state}

# Step 2: Concept Detection Node
def concept_node(state):
    parsed_text = state["parsed_text"]
    concepts = detect_concepts(parsed_text)
    return {"concepts": concepts, **state}

# Step 3: Profile Mapping Node
def profile_node(state):
    profile_path = state["profile_path"]
    concepts = state["concepts"]
    updated_profile = update_profile(profile_path, concepts)
    return {"profile": updated_profile, **state}

# Step 4: RAG Recommendation Node
def recommender_node(state):
    skills = state["profile"].get("skills", [])
    recommendations = recommend_next_steps(skills)
    return {"recommendations": recommendations, **state}
