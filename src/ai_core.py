"""
SAP AI Core connectivity — loads credentials and initialises the LLM.
Import get_llm() from this module; do not instantiate LLMs elsewhere.
"""
import json
import os

from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain_core.language_models.chat_models import BaseChatModel


def load_credentials(path: str = "aicore_service_key.json") -> None:
    """Read AI Core service key JSON and set required environment variables."""
    with open(path, encoding="utf-8") as f:
        sk = json.load(f)
    os.environ["AICORE_BASE_URL"]       = sk["serviceurls"]["AI_API_URL"]
    os.environ["AICORE_AUTH_URL"]       = sk["url"]
    os.environ["AICORE_CLIENT_ID"]      = sk["clientid"]
    os.environ["AICORE_CLIENT_SECRET"]  = sk["clientsecret"]
    os.environ["AICORE_RESOURCE_GROUP"] = "default"


def get_llm(model: str = "gpt-4o") -> BaseChatModel:
    """Return an initialised LangChain-compatible LLM via the Gen AI Hub proxy."""
    proxy_client = get_proxy_client("gen-ai-hub")
    return init_llm(model, proxy_client=proxy_client)
