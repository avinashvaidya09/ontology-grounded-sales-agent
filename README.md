# Ontology-Grounded Sales Agent

A learning project exploring RDF, SPARQL, and ontology-grounded AI agents
using the Python RDFLib library.

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

# Upgrade pip, then install dependencies in two steps
# (avoids pip dependency resolution depth errors)
pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bash
# Load the graph and print all triples
python3 -m src.load_graph

# Run SPARQL queries across all orders
python3 -m src.query_graph

# Run Agent A (tool-based)
python3 -m src.agent_a

# Run Agent B (SPARQL-generating) — coming soon
python3 -m src.agent_b
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
│   ├── rdf_basics.py         # Learning reference: manual triple creation in Python
│   ├── load_graph.py         # Loads sales_ontology.ttl into an RDFLib graph
│   ├── query_graph.py        # SPARQL query functions
│   ├── ai_core.py            # AI Core credentials + LLM initialisation
│   ├── agent_a.py            # Agent A: tool-based (restrictive)
│   └── agent_b.py            # Agent B: SPARQL-generating (flexible)
│
└── README.md
```

## Knowledge graph

The ontology in `data/sales_ontology.ttl` has two sections:

**Schema (ontology layer)** — classes and relationships:

```
Customer, SalesOrder, SalesOrderItem, Delivery, Material, Supplier

Customer       --places------->  SalesOrder
SalesOrder     --contains------>  SalesOrderItem
SalesOrder     --fulfilledBy--->  Delivery
Delivery       --fulfills------>  SalesOrderItem
SalesOrderItem --references--->  Material
Material       --suppliedBy--->  Supplier
```

**Instance data** — the specific business records (3 orders, 2 customers, 2 suppliers):

```
ACME   --places-->  SO100  (status: DELAYED,    material: MAT100, availability: OUT_OF_STOCK, supplier: SUP300)
ACME   --places-->  SO102  (status: PENDING,    material: MAT102, availability: LOW_STOCK,    supplier: SUP300)
GLOBEX --places-->  SO101  (status: CONFIRMED,  material: MAT101, availability: IN_STOCK,     supplier: SUP301)
```

## Stages

- Stage 0 — Project setup ✓
- Stage 1 — RDF fundamentals ✓
- Stage 2 — Business ontology ✓
- Stage 3 — Instance data ✓
- Stage 4 — SPARQL queries ✓
- Stage 5 — Python + SPARQL ✓
- Stage 6 — LLM-powered agent ← next
- Stage 7 — Architecture comparison

---

## Agent architecture (Stage 6)

Two agents are implemented using SAP AI Core via the Gen AI Hub SDK.

### Agent A — Tool-based (restrictive)

The LLM is given a fixed set of Python functions as tools. It cannot go outside them.

```
User question
      ↓
LLM + tool descriptions (function names + docstrings)
      ↓
LLM selects a tool: get_order_details("SO100")
      ↓
Python executes the SPARQL (query_graph.py)
      ↓
LLM formats the result as a natural language answer
```

- Schema knowledge is encoded in tool descriptions, not raw RDF
- Equivalent to an MCP/function-calling agent
- Safe: hallucinated property names are impossible — the SPARQL is pre-written

### Agent B — SPARQL-generating (flexible)

The LLM receives the ontology schema and generates SPARQL directly.

```
User question
      ↓
LLM + ontology schema (Turtle schema section in system prompt)
      ↓
LLM generates a SPARQL query
      ↓
Python executes it via g.query()
      ↓
LLM formats the result as a natural language answer
```

- Can answer questions not anticipated by pre-built functions
- LLM must know exact property names and traversal direction from the schema
- Risk: invalid SPARQL if the LLM misreads the schema

### Context provided to the LLM

| Agent | What the LLM sees |
|---|---|
| Agent A | Tool names, parameter names, and docstrings — schema is implicit |
| Agent B | The schema section of `sales_ontology.ttl` pasted into the system prompt |

### In the real world (SAP HANA Cloud KG, enterprise)

Large enterprise ontologies have thousands of classes — the full schema does not fit in a prompt.
Common approaches:

| Approach | How it works | When to use |
|---|---|---|
| Static schema in system prompt | Full schema pasted in | Small ontologies (like this project) |
| Schema summarisation | Pre-generate a compact natural-language description of the ontology | Medium ontologies |
| Schema retrieval | Embed schema fragments, retrieve relevant ones per query (RAG-like) | Large ontologies |
| Few-shot SPARQL examples | Include 3–5 example question/query pairs so the LLM learns the patterns | Any size, improves accuracy |

In SAP HANA Cloud KG, data from S/4HANA (via OData/BAPI) is extracted, mapped to RDF triples
by an ETL pipeline, and loaded into the graph store. The SPARQL endpoint is then exposed to agents.
The ontology schema acts as the grounding layer — the agent reasons over named semantic relationships
rather than guessing from column names or API descriptions.
