from app.state import State
from app.llm import structured_llm, SYSTEM_PROMPT


def parse_input(state: State) -> dict:
    """LLM node: messy text -> clean domain string."""
    try:
        result = structured_llm.invoke(
            [("system", SYSTEM_PROMPT), ("human", state["raw_input"])]
        )
    except Exception as e:
        return {"error": f"LLM call failed: {e}"}

    if not result.domain:
        return {"error": "I couldn't find a full domain (like google.com) in your message. Please include the TLD, e.g. .com, .in, .org."}

    return {"domain": result.domain.strip().lower()}