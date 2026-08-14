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

## Project structure

```
ontology-grounded-sales-agent/
│
├── requirements.txt          # Python dependencies (rdflib)
│
├── data/
│   └── sales_ontology.ttl    # Ontology schema + instance data (Stage 2+)
│
├── src/
│   ├── rdf_basics.py         # Learning reference: manual triple creation
│   ├── load_graph.py         # Loads the .ttl file into an RDFLib graph
│   ├── query_graph.py        # Runs SPARQL queries against the graph
│   └── agent.py              # LLM agent grounded on the KG (Stage 6+)
│
└── README.md
```

## Stages

- Stage 0 — Project setup ✓
- Stage 1 — RDF fundamentals ← in progress
- Stage 2 — Business ontology
- Stage 3 — Instance data
- Stage 4 — SPARQL queries
- Stage 5 — Python + SPARQL
- Stage 6 — LLM-powered agent
- Stage 7 — Architecture comparison
