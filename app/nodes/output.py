from app.state import State


def format_output(state: State) -> dict:
    """Builds the final answer from whatever is in state."""
    if state.get("error"):
        return {"answer": f"❌ {state['error']}"}

    ips = "\n  ".join(state["ips"])
    return {
        "answer": (
            f"✅ {state['domain']}\n"
            f"  main domain: {state['main_domain']}\n"
            f"  TLD: .{state['tld']}\n"
            f"  IP address(es):\n  {ips}"
        )
    }