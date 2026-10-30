from langgraph.graph import StateGraph, START, END

from app.state import State
from app.nodes.parse import parse_input
from app.nodes.validate import validate_domain
from app.nodes.resolve import resolve_ip
from app.nodes.output import format_output


def next_or_end(next_node: str):
    """Router factory: go to next_node, unless an error was set."""
    def router(state: State) -> str:
        return "format_output" if state.get("error") else next_node
    return router


def build_graph():
    builder = StateGraph(State)

    # Register nodes: (name, function)
    builder.add_node("parse_input", parse_input)
    builder.add_node("validate_domain", validate_domain)
    builder.add_node("resolve_ip", resolve_ip)
    builder.add_node("format_output", format_output)

    # Fixed edge: always start at parse_input
    builder.add_edge(START, "parse_input")

    # Conditional edges: after each step, go forward or jump to the output on error
    builder.add_conditional_edges(
        "parse_input", next_or_end("validate_domain"),
        ["validate_domain", "format_output"],
    )
    builder.add_conditional_edges(
        "validate_domain", next_or_end("resolve_ip"),
        ["resolve_ip", "format_output"],
    )
    builder.add_conditional_edges(
        "resolve_ip", next_or_end("format_output"),
        ["format_output"],
    )

    # Fixed edge: output is always last
    builder.add_edge("format_output", END)

    return builder.compile()


graph = build_graph()