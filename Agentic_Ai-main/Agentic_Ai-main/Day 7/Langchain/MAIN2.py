import streamlit as st
import spacy
import networkx as nx
import random
import json
import requests
from typing import List, Dict
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Initialize Gemini 2.0 Flash (replace with your API key)
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with actual key
genai.configure(api_key=GOOGLE_API_KEY)
model = GenerativeModel("gemini-2.0-flash")

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Simulated knowledge base for RAG (in practice, use a vector DB like Pinecone)
KNOWLEDGE_BASE = {
    "memoization": [
        {"title": "Dynamic Programming Tutorial", "url": "https://example.com/dp", "type": "tutorial"},
        {"title": "Memoization Code Lab", "url": "https://example.com/memo-lab", "type": "code_lab"}
    ],
    "reactive programming": [
        {"title": "RxJS Basics", "url": "https://example.com/rxjs", "type": "tutorial"},
        {"title": "Reactive Streams Project", "url": "https://example.com/reactive-project", "type": "project"}
    ]
}

# Input Parsing Agent
class InputParsingAgent:
    def parse_input(self, input_data: str, input_type: str) -> List[str]:
        """Parse raw input (URL, chat export, or text) into structured content."""
        if input_type == "url":
            # Simulate URL content extraction (e.g., Reddit thread, YouTube transcript)
            return self._parse_url(input_data)
        elif input_type == "chat_export":
            # Simulate Discord/Reddit chat export parsing
            return self._parse_chat_export(input_data)
        else:
            # Direct text input
            return input_data.split("\n")

    def _parse_url(self, url: str) -> List[str]:
        # Mock URL parsing (in practice, use APIs like YouTube Data API or web scraping)
        return [
            "User1: I learned about memoization in Python today!",
            "User2: Check out reactive programming with RxJS, it's awesome."
        ]

    def _parse_chat_export(self, chat_text: str) -> List[str]:
        # Mock chat export parsing
        lines = chat_text.split("\n")
        return [line for line in lines if line.strip() and not line.startswith("[" or "#")]

# Concept Detection Agent
class ConceptDetectionAgent:
    def __init__(self):
        self.technical_terms = ["memoization", "reactive programming", "async await", "REST API"]

    def detect_concepts(self, content: List[str]) -> List[str]:
        """Identify technical topics and concepts in content using spaCy and predefined terms."""
        concepts = set()
        for text in content:
            doc = nlp(text)
            for token in doc:
                if token.text.lower() in self.technical_terms:
                    concepts.add(token.text.lower())
            # Additional entity recognition for emerging skills
            for ent in doc.ents:
                if ent.label_ in ["SKILL", "TECH"]:  # Custom labels (requires custom NER model)
                    concepts.add(ent.text.lower())
        return list(concepts)

# Profile Mapping Agent
class ProfileMappingAgent:
    def __init__(self):
        self.user_graph = nx.DiGraph()

    def update_profile(self, user_id: str, concepts: List[str]) -> None:
        """Update user's skill graph with detected concepts."""
        if user_id not in self.user_graph:
            self.user_graph.add_node(user_id, type="user")
        
        for concept in concepts:
            if concept not in self.user_graph:
                self.user_graph.add_node(concept, type="concept")
            self.user_graph.add_edge(user_id, concept, weight=1.0)
    
    def get_user_skills(self, user_id: str) -> List[str]:
        """Retrieve user's current skills from the graph."""
        if user_id in self.user_graph:
            return [node for node in self.user_graph.neighbors(user_id)]
        return []

# Follow-Up Recommender Agent (RAG-Enabled)
class FollowUpRecommenderAgent:
    def recommend(self, concepts: List[str], user_skills: List[str]) -> List[Dict]:
        """Generate follow-up recommendations using RAG with Gemini."""
        recommendations = []
        for concept in concepts:
            # Retrieve relevant resources from knowledge base
            if concept in KNOWLEDGE_BASE:
                resources = KNOWLEDGE_BASE[concept]
                # Augment with Gemini for contextual suggestions
                prompt = f"""
                Given the concept '{concept}' and user skills {user_skills}, suggest relevant learning resources.
                Current resources: {json.dumps(resources, indent=2)}
                Provide a JSON list of recommendations with title, url, and type.
                """
                response = model.generate_content(prompt)
                try:
                    new_recommendations = json.loads(response.text)
                    recommendations.extend(new_recommendations)
                except:
                    recommendations.extend(resources)  # Fallback to knowledge base
        return recommendations[:3]  # Limit to top 3 recommendations

# Streamlit App
def main():
    st.title("AI Learning Signal Extractor")
    st.write("Extract learning signals from informal sources and get personalized recommendations.")

    # Initialize session state for user profile
    if "user_id" not in st.session_state:
        st.session_state.user_id = "user_" + str(random.randint(1000, 9999))
    if "profile_agent" not in st.session_state:
        st.session_state.profile_agent = ProfileMappingAgent()

    # Input form
    input_type = st.selectbox("Input Type", ["Text", "URL", "Chat Export"])
    input_data = st.text_area("Enter your input (text, URL, or chat export)")
    
    if st.button("Process Input"):
        if input_data:
            # Initialize agents
            parser = InputParsingAgent()
            concept_detector = ConceptDetectionAgent()
            recommender = FollowUpRecommenderAgent()

            # Step 1: Parse input
            parsed_content = parser.parse_input(input_data, input_type.lower())
            st.subheader("Parsed Content")
            st.write(parsed_content)

            # Step 2: Detect concepts
            concepts = concept_detector.detect_concepts(parsed_content)
            st.subheader("Detected Concepts")
            st.write(concepts)

            # Step 3: Update user profile
            st.session_state.profile_agent.update_profile(st.session_state.user_id, concepts)
            user_skills = st.session_state.profile_agent.get_user_skills(st.session_state.user_id)
            st.subheader("Updated User Skills")
            st.write(user_skills)

            # Step 4: Generate recommendations
            recommendations = recommender.recommend(concepts, user_skills)
            st.subheader("Recommended Learning Resources")
            for rec in recommendations:
                st.write(f"- [{rec['title']}]({rec['url']}) ({rec['type']})")
        else:
            st.error("Please provide input data.")

if __name__ == "__main__":
    main()