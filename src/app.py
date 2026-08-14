"""
FastAPI web server — serves the chat UI and routes questions to the active agent.
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .llm.ai_core import get_llm, load_credentials
from .agents import agent_a, agent_b

app = FastAPI()

load_credentials()
_llm = get_llm()


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""

    question: str
    agent: str = "a"


@app.get("/")
async def index():
    """Serve the chat UI."""
    return FileResponse("src/templates/index.html")


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
