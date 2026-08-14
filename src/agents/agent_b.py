"""
Agent B — SPARQL-generating ontology-grounded agent.
The LLM receives the ontology schema and writes SPARQL directly.
More flexible than Agent A; requires the LLM to reason over the schema.
"""
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from ..llm.ai_core import get_llm, load_credentials
from ..llm.llm_config import AGENT_B_SYSTEM_PROMPT
from ..kg.load_graph import load_graph

_graph = load_graph()

# ── tool ──────────────────────────────────────────────────────────────────────


@tool
def execute_sparql(query: str) -> str:
    """Execute a SPARQL SELECT query against the sales knowledge graph and return the results."""
    try:
        print(f"\n[Agent B] SPARQL:\n{query}\n")
        results = _graph.query(query)
        rows = [
            ", ".join(
                f"{var}: {str(val).rsplit('/', maxsplit=1)[-1]}"
                for var, val in zip(results.vars, row)
            )
            for row in results
        ]
        return "\n".join(rows) if rows else "Query returned no results."
    except Exception as e:
        return f"SPARQL error: {e}"


# ── agent ─────────────────────────────────────────────────────────────────────

_TOOLS    = [execute_sparql]
_TOOL_MAP = {t.name: t for t in _TOOLS}


def run(question: str, llm, max_iterations: int = 5) -> str:
    """Answer a question by letting the LLM generate and execute SPARQL.

    Loops until the LLM returns a text answer or max_iterations is reached.
    """
    llm_with_tools = llm.bind_tools(_TOOLS)
    messages = [SystemMessage(AGENT_B_SYSTEM_PROMPT), HumanMessage(question)]

    for _ in range(max_iterations):
        response = llm_with_tools.invoke(messages)
        if not response.tool_calls:
            return response.content
        messages.append(response)
        for tc in response.tool_calls:
            result = _TOOL_MAP[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(str(result), tool_call_id=tc["id"]))

    return "Could not produce an answer within the allowed number of steps."


# ── demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    load_credentials()
    _llm = get_llm()

    questions = [
        "Why is sales order SO100 delayed?",
        "Which customer placed SO101?",
        "What is the availability status of the material in SO102?",
    ]

    print("=== Agent B — SPARQL-generating ===\n")
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {run(q, _llm)}\n")
