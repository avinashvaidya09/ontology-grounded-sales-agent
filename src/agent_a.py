"""
Agent A — tool-based ontology-grounded agent.
The LLM calls pre-built Python functions backed by SPARQL queries.
It cannot go outside the defined tools.
"""
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from .ai_core import get_llm, load_credentials
from .load_graph import load_graph
from .query_graph import (
    get_customer_for_order,
    get_delivery_for_order,
    get_order_details,
    get_order_status,
)

_graph = load_graph()

# ── tools ─────────────────────────────────────────────────────────────────────

@tool
def check_order_status(order_id: str) -> str:
    """Return the current status of a sales order (e.g. DELAYED, CONFIRMED, PENDING)."""
    result = get_order_status(_graph, order_id)
    return result or f"No status found for order {order_id}."


@tool
def check_order_customer(order_id: str) -> str:
    """Return the customer who placed a sales order."""
    result = get_customer_for_order(_graph, order_id)
    return result or f"No customer found for order {order_id}."


@tool
def check_order_delivery(order_id: str) -> str:
    """Return the delivery ID fulfilling a sales order."""
    result = get_delivery_for_order(_graph, order_id)
    return result or f"No delivery found for order {order_id}."


@tool
def check_order_details(order_id: str) -> str:
    """Return the material, availability status, and supplier for a sales order."""
    result = get_order_details(_graph, order_id)
    if result:
        return (
            f"Material: {result['material']}, "
            f"Availability: {result['availability_status']}, "
            f"Supplier: {result['supplier']}"
        )
    return f"No details found for order {order_id}."


# ── agent ─────────────────────────────────────────────────────────────────────

_TOOLS    = [check_order_status, check_order_customer, check_order_delivery, check_order_details]
_TOOL_MAP = {t.name: t for t in _TOOLS}

_SYSTEM_PROMPT = """You are a sales order exception agent.
You have access to a knowledge graph containing sales orders, customers,
deliveries, materials, and suppliers.
Use the tools to look up facts. Do not guess — always call a tool first."""


def run(question: str, llm, max_iterations: int = 5) -> str:
    """Answer a question using tool calls backed by SPARQL queries.

    Loops until the LLM returns a text answer or max_iterations is reached.
    """
    llm_with_tools = llm.bind_tools(_TOOLS)
    messages = [SystemMessage(_SYSTEM_PROMPT), HumanMessage(question)]

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
    llm = get_llm()

    questions = [
        "Why is sales order SO100 delayed?",
        "Which customer placed SO101?",
        "What is the availability status of the material in SO102?",
    ]

    print("=== Agent A — Tool-based ===\n")
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {run(q, llm)}\n")
