def router_node(state):
    query = state["query"].lower()

    if any(kw in query for kw in ["latest", "current", "news", "today", "now"]):
        route = "web"
    elif any(kw in query for kw in ["data", "report", "dataset", "chart"]):
        route = "rag"
    else:
        route = "llm"

    return {**state, "route": route}
