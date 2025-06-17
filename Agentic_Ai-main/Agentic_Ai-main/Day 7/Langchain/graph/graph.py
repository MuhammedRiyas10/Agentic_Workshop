from langgraph.graph import StateGraph
from graph.schema import AgentState
from agents.input_parser import parse_input
from agents.concept_detector import detect_concepts
from agents.profile_mapper import update_profile
from agents.recommender_agent import recommend_next_steps

def learning_graph():
    builder = StateGraph(AgentState)

    # Add nodes (agents)
    builder.add_node("InputParser", parse_input)
    builder.add_node("ConceptDetector", detect_concepts)
    builder.add_node("ProfileMapper", update_profile)
    builder.add_node("Recommender", recommend_next_steps)

    # Define flow
    builder.set_entry_point("InputParser")
    builder.add_edge("InputParser", "ConceptDetector")
    builder.add_edge("ConceptDetector", "ProfileMapper")
    builder.add_edge("ProfileMapper", "Recommender")
    builder.set_finish_point("Recommender")

    return builder.compile()
