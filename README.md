# Ontology-Grounded Sales Agent

A hands-on learning project exploring RDF, SPARQL, and ontology-grounded AI agents
using Python and RDFLib — built step-by-step to understand the foundations before
introducing an LLM.

> **Want to learn this hands-on?**
> Create an empty project, copy `CLAUDE.md` into it, and open it with Claude Code.
> Claude will teach you every concept and build the project with you one step at a time —
> explaining RDF, SPARQL, and agent architecture before writing a single line of code.

## Table of contents

- [Scenario](#scenario)
- [Requirements](#requirements)
- [Setup](#setup)
- [Run](#run)
- [Project structure](#project-structure)
- [Knowledge graph](#knowledge-graph)
- [Learning stages](#learning-stages)
- [Agent architecture](#agent-architecture)
  - [Agent A — Tool-based](#agent-a--tool-based-constrained)
  - [Agent B — SPARQL-generating](#agent-b--sparql-generating-flexible)
  - [Schema context per agent](#schema-context-provided-to-each-agent)
  - [Scaling to enterprise ontologies](#scaling-to-enterprise-ontologies-eg-sap-hana-cloud-kg)
- [Architecture comparison](#architecture-comparison-stage-7)
  - [Pattern A — Tool/MCP](#pattern-a--prompt--tool-agent-agent-a)
  - [Pattern B — Ontology-grounded](#pattern-b--ontology-grounded-agent-agent-b)
  - [Pattern C — Hybrid](#pattern-c--hybrid-enterprise-target-architecture)
  - [Trade-off table](#trade-off-table)
- [Web UI](#web-ui)

## Scenario

A Sales Order Exception Agent that can answer questions like:

> "Why is sales order SO100 delayed, and which supplier is involved?"

## Requirements

- Python 3.12 — required for `pydantic-core` (Rust extension) to build correctly
- SAP AI Core service key (`aicore_service_key.json` at project root — not committed to git)

## Setup

```bash
# Ensure Python 3.12 is installed
python3.12 --version
# If not: brew install python@3.12

# Create virtual environment with Python 3.12
python3.12 -m venv .venv
source .venv/bin/activate

# Upgrade pip, then install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bash
# Run SPARQL queries across all orders (no LLM required)
python3 -m src.kg.query_graph

# Run Agent A (tool-based) — CLI demo
python3 -m src.agents.agent_a

# Run Agent B (SPARQL-generating) — CLI demo
python3 -m src.agents.agent_b

# Start the full chat UI (FastAPI + uvicorn)
python3 -m uvicorn src.app:app --reload --port 5000
# Then open http://localhost:5000
# Knowledge graph visualisation: http://localhost:5000/graph
```

## Project structure

```
ontology-grounded-sales-agent/
│
├── requirements.txt          # Python dependencies
├── aicore_service_key.json   # AI Core credentials (not committed to git)
│
├── data/
│   ├── rdf_basics.ttl        # Learning reference: three hand-written triples
│   └── sales_ontology.ttl    # Business ontology (schema + instance data)
│
├── src/
│   ├── kg/
│   │   ├── load_graph.py     # Loads sales_ontology.ttl into an RDFLib graph
│   │   └── query_graph.py    # SPARQL query functions
│   ├── agents/
│   │   ├── agent_a.py        # Agent A: tool-based (constrained)
│   │   └── agent_b.py        # Agent B: SPARQL-generating (flexible)
│   ├── llm/
│   │   ├── ai_core.py        # AI Core credentials + LLM initialisation
│   │   └── llm_config.py     # System prompt constants for all agents
│   ├── templates/
│   │   ├── index.html        # Chat UI — agent selector, message history, typing indicator
│   │   └── graph.html        # D3.js force-directed knowledge graph visualisation
│   ├── rdf_basics.py         # Learning reference: manual triple creation in Python
│   └── app.py                # FastAPI server — /chat, /graph, /graph-data, /history
│
└── README.md
```

## Knowledge graph

The ontology in `data/sales_ontology.ttl` has two sections.

**Schema (ontology layer)** — classes and object/datatype properties:

```
Customer, SalesOrder, SalesOrderItem, Delivery, Material, Supplier

Customer       --places------->  SalesOrder
SalesOrder     --contains------>  SalesOrderItem
SalesOrder     --fulfilledBy--->  Delivery
Delivery       --fulfills------>  SalesOrderItem
SalesOrderItem --references--->  Material
Material       --suppliedBy--->  Supplier

SalesOrder.status              string literal  (DELAYED | CONFIRMED | PENDING)
Material.availabilityStatus    string literal  (OUT_OF_STOCK | IN_STOCK | LOW_STOCK)
```

**Instance data** — 3 customers, 8 orders, 13 order items, 8 deliveries, 6 materials, 3 suppliers:

```
ACME    --places-->  SO100  DELAYED    MAT100  OUT_OF_STOCK  SUP300
ACME    --places-->  SO102  PENDING    MAT102  LOW_STOCK     SUP300
ACME    --places-->  SO103  CONFIRMED  MAT101  IN_STOCK      SUP301
                            (also)     MAT103  IN_STOCK      SUP300
ACME    --places-->  SO107  CONFIRMED  MAT101  IN_STOCK      SUP301
                            (also)     MAT105  OUT_OF_STOCK  SUP302

GLOBEX  --places-->  SO101  CONFIRMED  MAT101  IN_STOCK      SUP301
GLOBEX  --places-->  SO104  DELAYED    MAT100  OUT_OF_STOCK  SUP300
                            (also)     MAT104  OUT_OF_STOCK  SUP302

INITECH --places-->  SO105  PENDING    MAT102  LOW_STOCK     SUP300
INITECH --places-->  SO106  DELAYED    MAT103  IN_STOCK      SUP300
                            (also)     MAT105  OUT_OF_STOCK  SUP302
```

Several materials are shared across orders (e.g. MAT100 appears in SO100 and SO104),
and SUP302 supplies multiple out-of-stock materials — enabling cross-order reasoning.

## Learning stages

| Stage | Topic | Status |
|-------|-------|--------|
| 0 | Project setup | ✓ |
| 1 | RDF fundamentals (triples, URIs, literals, namespaces) | ✓ |
| 2 | Business ontology in Turtle | ✓ |
| 3 | Instance data + comparison with relational schema | ✓ |
| 4 | Manual SPARQL queries | ✓ |
| 5 | Python + SPARQL via RDFLib | ✓ |
| 6 | LLM-powered agents (Agent A + Agent B) + web UI | ✓ |
| 7 | Architecture comparison (tool-based vs ontology-grounded vs hybrid) | ✓ |

## Agent architecture

Both agents are implemented using SAP AI Core via the Gen AI Hub SDK (gpt-4o).

### Agent A — Tool-based (constrained)

The LLM is given a fixed set of Python functions as tools. It cannot query outside them.

```
User question
      ↓
LLM + tool descriptions (function signatures + docstrings)
      ↓
LLM selects a tool: get_order_details("SO100")
      ↓
Python executes pre-written SPARQL (query_graph.py)
      ↓
LLM formats the result as a natural language answer
```

- Schema knowledge is encoded in tool descriptions, not raw RDF
- Equivalent to an MCP / function-calling agent
- Safe: hallucinated property names are impossible — the SPARQL is pre-written
- Limited: can only answer questions covered by the pre-built functions

### Agent B — SPARQL-generating (flexible)

The LLM receives the ontology schema and writes SPARQL dynamically.

```
User question
      ↓
LLM + ontology schema (classes, properties, few-shot examples in system prompt)
      ↓
LLM generates a SPARQL SELECT query
      ↓
Python executes it via g.query()  →  results logged to terminal
      ↓
LLM formats the result as a natural language answer
```

- Can answer questions not anticipated by pre-built functions
- More flexible: any traversal across the graph is possible
- Risk: the LLM must use exact property names and correct literal quoting
- Key lesson: status values are string literals (`"DELAYED"`) not URIs (`sales:DELAYED`)

### Schema context provided to each agent

| Agent | What the LLM sees |
|---|---|
| Agent A | Tool names, parameter names, and docstrings — schema is implicit |
| Agent B | Classes, properties, literal types, CORRECT/WRONG examples, few-shot SPARQL queries |

### Scaling to enterprise ontologies (e.g. SAP HANA Cloud KG)

Large enterprise ontologies have thousands of classes — the full schema never fits in a prompt.

| Approach | How it works | When to use |
|---|---|---|
| Static schema in system prompt | Full schema pasted in | Small ontologies (like this project) |
| Schema summarisation | Pre-generate a compact natural-language description | Medium ontologies |
| Schema retrieval | Embed schema fragments, retrieve relevant ones per query (RAG-like) | Large ontologies |
| Few-shot SPARQL examples | Include 3–5 example question/query pairs | Any size — improves accuracy |

In SAP HANA Cloud KG, data from S/4HANA (via OData/BAPI) is extracted, mapped to RDF
triples by an ETL pipeline, and loaded into the graph store. The SPARQL endpoint is then
exposed to agents. The ontology schema acts as the grounding layer — the agent reasons
over named semantic relationships rather than guessing from column names or API descriptions.

## Architecture comparison (Stage 7)

### Pattern A — Prompt + Tool agent (Agent A)

```
User question
      ↓
LLM reads tool descriptions (function names + docstrings)
      ↓
Calls: get_order_details("SO100")
      ↓
Pre-written Python function runs pre-written SPARQL
      ↓
LLM formats the result
```

Equivalent to an MCP server or OData API agent. The LLM selects from a fixed menu of
functions — it never touches the data model directly. Schema knowledge is implicit in
the function signatures. Every SAP CAP service with an LLM routing layer is this pattern.

### Pattern B — Ontology-grounded agent (Agent B)

```
User question
      ↓
LLM reads the ontology schema (classes, properties, literal types, few-shot SPARQL)
      ↓
LLM writes SPARQL dynamically
      ↓
Python executes it against the knowledge graph
      ↓
LLM formats the result
```

The LLM reasons over named semantic relationships, not function signatures. Any traversal
path the ontology defines is reachable — including ones never anticipated at design time.

### Pattern C — Hybrid (enterprise target architecture)

```
                 ┌─ Ontology / KG  (reference data, relationships, classifications)
User ──► Agent ──┤
                 └─ APIs / tools   (live operational data, real-time transactional state)
```

Example: the KG holds semantic relationships (MAT100 is supplied by SUP300, SUP300 is in
Germany, Germany has import restrictions) but the live stock level comes from an S/4HANA
OData call at query time.

### Trade-off table

| Dimension | A — Tool/MCP | B — Ontology-grounded | C — Hybrid |
|---|---|---|---|
| Semantic grounding | Weak — schema buried in docstrings | Strong — relationships explicit in ontology | Strong for reference data |
| Hallucination risk | Low for facts (SPARQL pre-written) | Medium — LLM can write invalid SPARQL | Mixed |
| Explainability | Medium — tool call is logged, SPARQL hidden | High — generated SPARQL is the reasoning trace | High for KG path |
| Graph traversal | Only pre-written paths | Any path the ontology defines | Full traversal over KG portion |
| Cross-domain reasoning | Only if you wrote the join | Natural — KG encodes relationships explicitly | Best |
| Live / operational data | Yes, if tools call live APIs | No — graph is loaded at startup | Yes — API side is real-time |
| Freshness | As fresh as the API | Stale — requires ETL to reload | Mixed |
| Complexity | Low initially; grows with tool count | Medium — requires ontology design upfront | Highest |
| Maintenance | New concept → new tools + docstrings | New concept → new triples; agents pick it up | Both layers |

---

> **Note:** The architecture descriptions and trade-off observations above are based on
> personal learning and reading from technical sources. They reflect an evolving
> understanding, not definitive recommendations. Each pattern has valid use cases
> depending on context. Readers are encouraged to evaluate the trade-offs against
> their own requirements.

## Web UI

The FastAPI application (`src/app.py`) exposes:

| Route | Purpose |
|---|---|
| `GET /` | Chat UI with agent selector and message history |
| `GET /graph` | D3.js force-directed knowledge graph visualisation |
| `GET /graph-data` | JSON nodes + edges for the D3 visualisation |
| `GET /history/{agent}` | Retrieve in-session chat history for agent `a` or `b` |
| `POST /chat` | Send a question to the selected agent; returns the answer |

Chat history is stored in-memory on the server and persists across agent switches
for the duration of the server session. It is cleared on server restart.
