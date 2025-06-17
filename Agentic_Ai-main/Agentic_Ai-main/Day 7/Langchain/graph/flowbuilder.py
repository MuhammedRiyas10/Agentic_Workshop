from langgraph.graph import StateGraph
from graph.nodesconfig import input_node, concept_node, profile_node, recommender_node

def build_flow():
    builder = StateGraph()

    # Add nodes
    builder.add_node("input_parser", input_node)
    builder.add_node("concept_detector", concept_node)
    builder.add_node("profile_mapper", profile_node)
    builder.add_node("recommender", recommender_node)

    # Define flow
    builder.set_entry_point("input_parser")
    builder.add_edge("input_parser", "concept_detector")
    builder.add_edge("concept_detector", "profile_mapper")
    builder.add_edge("profile_mapper", "recommender")

    return builder.compile()
