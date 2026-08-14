# ═══════════════════════════════════════════════════════════════════════════════════════════
#                               Import and Init statements
# ═══════════════════════════════════════════════════════════════════════════════════════════

import argparse

from langchain_core.messages import HumanMessage
from langgraph.graph import START, StateGraph

from src.nodes import (
    SupervisorState,
    property_profile_agent_node,
    supervisor_command_node,
    transaction_history_agent_node,
)


# ═══════════════════════════════════════════════════════════════════════════════════════════
#                                   Graph Generation
# ═══════════════════════════════════════════════════════════════════════════════════════════

def build_graph() -> StateGraph:
    """Build graph using Command for dynamic routing."""

    graph = StateGraph(SupervisorState)

    graph.add_node("supervisor", supervisor_command_node)
    graph.add_node(
        "transaction_history_agent",
        transaction_history_agent_node
    )
    graph.add_node(
        "property_profile_agent",
        property_profile_agent_node
    )

    graph.add_edge(START, "supervisor")

    return graph.compile()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Command-based routing example"
    )

    parser.add_argument(
        "query",
        nargs="?",
        default="Tell me about the property at Sunset Boulevard"
    )

    args = parser.parse_args()

    print("EXAMPLE: Command-based Routing")
    print("=" * 70)
    print(f"Query: {args.query}\n")

    graph = build_graph()

    final_state = graph.invoke(
        {
            "messages": [
                HumanMessage(content=args.query)
            ]
        }
    )

    print("\n" + "=" * 70)
    print("STATE UPDATE:")
    print(
        f"  property_name: "
        f"'{final_state.get('property_name', '(not extracted)')}'"
    )
    print("=" * 70)