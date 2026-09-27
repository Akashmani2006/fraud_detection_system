from langgraph.graph import StateGraph, START, END

from app.graph.state import FraudState
from app.graph.nodes import (
    velocity_node,
    geo_node,
    merchant_node,
    merge_node,
    auto_clear_node,
    escalate_node
)
graph = StateGraph(FraudState)
graph.add_node("velocity", velocity_node)
graph.add_node("geo", geo_node)
graph.add_node("merchant", merchant_node)
graph.add_node("merge", merge_node)
graph.add_node("auto_clear", auto_clear_node)
graph.add_node("escalate", escalate_node)



graph.add_edge(START, "velocity")
graph.add_edge(START, "geo")
graph.add_edge(START, "merchant")

graph.add_edge("velocity", "merge")
graph.add_edge("geo", "merge")
graph.add_edge("merchant", "merge")


graph.add_conditional_edges(
    "merge",
    lambda state: state["decision"],
    {
        "AUTO_CLEAR": "auto_clear",
        "ESCALATE": "escalate"
    }
)

graph.add_edge("auto_clear", END)
graph.add_edge("escalate", END)

app = graph.compile()