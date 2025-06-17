from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from agents.router_agent import router_node
from agents.web_agent import web_node
from agents.rag_agent import rag_node
from agents.summarizer_agent import summarizer_node

# 1. Define state schema
class AgentState(TypedDict):
    query: str
    route: Optional[str]
    web_result: Optional[str]
    rag_result: Optional[str]
    final_output: Optional[str]

# 2. Build LangGraph with schema
def initialize_graph():
    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("web", web_node)
    builder.add_node("rag", rag_node)
    builder.add_node("summarizer", summarizer_node)

    builder.set_entry_point("router")
    builder.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "web": "web",
            "rag": "rag",
            "llm": "summarizer"
        }
    )

    builder.add_edge("web", "summarizer")
    builder.add_edge("rag", "summarizer")

    return builder.compile()
