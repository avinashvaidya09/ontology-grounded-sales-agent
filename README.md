# Ontology-Grounded Sales Agent

A learning project exploring RDF, SPARQL, and ontology-grounded AI agents
using the Python RDFLib library.

## Scenario

A Sales Order Exception Agent that can answer questions like:

> "Why is sales order SO100 delayed, and which supplier is involved?"

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
```

## Run

```bash
# Load the graph and print all triples
python3 src/load_graph.py
```

## Project structure

```
ontology-grounded-sales-agent/
│
├── requirements.txt          # Python dependencies (rdflib)
│
├── data/
│   ├── rdf_basics.ttl        # Learning reference: three hand-written triples
│   └── sales_ontology.ttl    # Business ontology (schema + instance data)
│
├── src/
│   ├── rdf_basics.py         # Learning reference: manual triple creation in Python
│   ├── load_graph.py         # Loads sales_ontology.ttl into an RDFLib graph
│   ├── query_graph.py        # SPARQL queries against the graph (Stage 4+)
│   └── agent.py              # LLM agent grounded on the KG (Stage 6+)
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

**Instance data** — the specific business records:

```
ACME  --places------->  SO100
SO100 --contains------>  SO100_ITEM10
SO100 --fulfilledBy--->  DEL800
DEL800 --fulfills----->  SO100_ITEM10
SO100_ITEM10 --references--> MAT100
MAT100 --suppliedBy--->  SUP300

SO100  status: DELAYED
MAT100 availabilityStatus: OUT_OF_STOCK
```

## Stages

- Stage 0 — Project setup ✓
- Stage 1 — RDF fundamentals ✓
- Stage 2 — Business ontology ✓
- Stage 3 — Instance data ✓
- Stage 4 — SPARQL queries ← next
- Stage 5 — Python + SPARQL
- Stage 6 — LLM-powered agent
- Stage 7 — Architecture comparison
