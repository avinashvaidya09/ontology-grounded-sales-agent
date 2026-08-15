"""
FastAPI web server — serves the chat UI and routes questions to the active agent.
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rdflib.namespace import RDF

from .llm.ai_core import get_llm, load_credentials
from .agents import agent_a, agent_b
from .kg.load_graph import load_graph

app = FastAPI()

load_credentials()
_llm = get_llm()
_graph = load_graph()

SALES_URI = "http://example.org/sales/"
_REL_PREDS = {"places", "contains", "fulfilledBy", "fulfills", "references", "suppliedBy"}
_LIT_PREDS = {"status", "availabilityStatus"}


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""

    question: str
    agent: str = "a"


@app.get("/")
async def index():
    """Serve the chat UI."""
    return FileResponse("src/templates/index.html")


@app.get("/graph")
async def graph_page():
    """Serve the knowledge graph visualisation page."""
    return FileResponse("src/templates/graph.html")


@app.get("/graph-data")
async def graph_data():
    """Return KG nodes and edges as JSON for the D3 visualisation."""
    type_map: dict[str, str] = {}
    props_map: dict[str, dict] = {}
    edges: list[dict] = []

    for s, p, o in _graph:
        s_str, p_str, o_str = str(s), str(p), str(o)
        pred = p_str.rsplit("/", 1)[-1] if "/" in p_str else p_str.rsplit("#", 1)[-1]

        if p == RDF.type and s_str.startswith(SALES_URI) and o_str.startswith(SALES_URI):
            type_map[s_str.rsplit("/", 1)[-1]] = o_str.rsplit("/", 1)[-1]

        elif pred in _REL_PREDS and s_str.startswith(SALES_URI) and o_str.startswith(SALES_URI):
            edges.append({
                "source": s_str.rsplit("/", 1)[-1],
                "target": o_str.rsplit("/", 1)[-1],
                "label":  pred,
            })

        elif pred in _LIT_PREDS and s_str.startswith(SALES_URI):
            node_id = s_str.rsplit("/", 1)[-1]
            props_map.setdefault(node_id, {})[pred] = o_str

    nodes = [
        {"id": k, "type": v, "props": props_map.get(k, {})}
        for k, v in type_map.items()
    ]
    return {"nodes": nodes, "edges": edges}


@app.post("/chat")
async def chat(body: ChatRequest):
    """Route a question to the selected agent and return the answer."""
    if not body.question.strip():
        return {"error": "No question provided."}

    if body.agent == "a":
        answer = agent_a.run(body.question, _llm)
    elif body.agent == "b":
        answer = agent_b.run(body.question, _llm)
    else:
        answer = f"Unknown agent: {body.agent}"

    return {"answer": answer}
