import os
from graph.graph import learning_graph
from graph.schema import AgentState
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger()

# Define the input file and type (text or pdf)
SOURCE_FILE = "data/youtube_transcripts/reacthooks.txt"  # change to .pdf if needed
SOURCE_TYPE = "text"  # or "pdf"

def run_learning_pipeline(source_file, source_type):
    logger.info("[START] Starting Learning Signal Flow")

    # Step 1: Create initial agent state
    initial_state = AgentState(
        input_path=source_file,
        input_type=source_type
    )

    # Step 2: Load the LangGraph flow
    app = learning_graph()

    # Step 3: Run the graph with the initial state
    final_state = app.invoke(initial_state)

    # Step 4: Output final result
    logger.info("\n[✅ COMPLETED] Extracted Skills and Recommendations:")
    print("📌 Skills Found:", final_state.extracted_skills)
    print("📚 Enriched Concepts:", final_state.enriched_concepts)
    print("🧠 Mapped Profile:", final_state.profile)
    print("➡️ Follow-Up Suggestions:\n", final_state.recommendations)

if __name__ == "__main__":
    run_learning_pipeline(SOURCE_FILE, SOURCE_TYPE)
