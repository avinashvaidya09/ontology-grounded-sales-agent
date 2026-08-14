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

# Run SPARQL queries across all orders
python3 src/query_graph.py
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
