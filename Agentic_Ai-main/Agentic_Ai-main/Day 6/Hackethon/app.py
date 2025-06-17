import streamlit as st
import json
from agents.skill_extractor import extract_skills
from agents.rag_enricher import enrich_skills
from utils.content_loader import load_input
from utils.text_loader import load_text
from utils.profile_manager import update_profile

st.title("🧠 AI Skill Extractor + RAG Enricher")

input_type = st.selectbox("Choose input type", ["Text", "Upload Chat File (.txt)", "URL"])
user_input = ""

if input_type == "Text":
    user_input = st.text_area("Enter the text you want to analyze")
elif input_type == "Upload Chat File (.txt)":
    uploaded_file = st.file_uploader("Upload .txt file", type="txt")
    if uploaded_file:
        user_input = uploaded_file.read().decode("utf-8")
elif input_type == "URL":
    url = st.text_input("Enter a URL")
    if url:
        user_input = load_input("url", url)

if st.button("🔍 Extract & Enrich Skills") and user_input:
    with st.spinner("🔍 Extracting skills..."):
        skills = extract_skills(user_input)
        st.success("✅ Skills Extracted")
        st.markdown("\n".join([f"- {skill}" for skill in skills]))

    with st.spinner("📚 Enriching skills using RAG..."):
        enriched = enrich_skills(skills)
        st.success("✅ Skills Enriched")
        for skill, definition in enriched.items():
            st.markdown(f"**{skill}**: {definition}")

    update_profile(skills)
    st.success("👤 Profile Updated")

    st.subheader("📊 Enriched Skills Table")
    st.table({"Skill": list(enriched.keys()), "Definition": list(enriched.values())})

    st.subheader("📥 Download Updated Profile")
    try:
        with open("profiles/profile.json", "r") as f:
            profile_data = json.load(f)
        st.download_button(
            label="Download Profile JSON",
            data=json.dumps(profile_data, indent=2),
            file_name="updated_profile.json",
            mime="application/json"
        )
    except FileNotFoundError:
        st.warning("Profile not found. Please run extraction first.")
