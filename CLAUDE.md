# Ontology-Grounded Agent Learning Project

## 1. Purpose

This repository is a **learning project**, not a speed-coding or vibe-coding exercise.

The goal is to learn, hands-on, how an **ontology-grounded AI agent** can use:

- RDF
- Turtle (`.ttl`)
- SPARQL
- Python
- RDFLib
- an LLM/agent only after the RDF/SPARQL foundation is understood

The project should stay intentionally small and transparent so that I understand every architectural and implementation decision.

The final goal is to be able to explain, at AI Architect level:

1. What an ontology is.
2. What a knowledge graph is.
3. How RDF represents knowledge as triples.
4. How ontology/schema and instance data differ.
5. How SPARQL queries a knowledge graph.
6. How an agent can use ontology + graph data as grounding.
7. How an ontology-grounded agent differs from a prompt-and-tool/MCP-based agent.
8. When ontology/KG architecture is useful and when it adds unnecessary complexity.

---

## 2. My Background

I am an SAP BTP / AI Technology Architect with experience in:

- SAP CAP / CDS
- SAP S/4HANA APIs
- OData / REST APIs
- Python
- LangChain
- SAP AI Core / Generative AI Hub
- agentic AI
- multi-agent systems
- MCP/tool-based agents
- enterprise integration and security

I am comfortable with relational databases, normalized schemas, foreign keys, APIs, and enterprise application architecture.

I am **fairly new to ontology, RDF, knowledge graphs, and SPARQL**.

When teaching concepts, relate them to things I already know where useful, especially:

- CDS entities and associations
- relational database tables and foreign keys
- OData entity relationships
- SAP S/4HANA business objects
- MCP tools / enterprise APIs

Do not assume prior semantic-web knowledge.

---

## 3. Project Scenario

Use one small business scenario throughout the project so that ontology concepts remain concrete.

### Scenario: Sales Order Exception Agent

A user should eventually be able to ask something like:

> Why is sales order SO100 delayed, and which supplier is involved?

The small business domain should initially contain only these concepts:

- Customer
- SalesOrder
- SalesOrderItem
- Delivery
- Material
- Supplier

Example semantic relationships:

```text
Customer --places--> SalesOrder
SalesOrder --contains--> SalesOrderItem
SalesOrderItem --references--> Material
SalesOrder --fulfilledBy--> Delivery
Delivery --fulfills--> SalesOrderItem
Material --suppliedBy--> Supplier
```

Example instance data may eventually look like:

```text
ACME --places--> SO100
SO100 --contains--> SO100_ITEM10
SO100_ITEM10 --references--> MAT100
SO100 --fulfilledBy--> DEL800
DEL800 --fulfills--> SO100_ITEM10
MAT100 --suppliedBy--> SUP300

SO100 --status--> DELAYED
MAT100 --availabilityStatus--> OUT_OF_STOCK
```

Keep the graph very small at first.

Do not expand the domain unless there is a learning reason to do so.

---

## 4. Technology Constraints

For the initial learning project, use only:

- Python
- RDF
- Turtle
- SPARQL
- RDFLib

Do **not** introduce any of the following unless I explicitly ask for them later:

- SAP HANA Cloud
- SAP Business Data Cloud
- SAP Datasphere
- Neo4j
- MCP servers
- vector databases
- RAG
- Docker
- Kubernetes
- cloud deployment
- complex frameworks
- graph frameworks other than RDFLib

The purpose is to understand the fundamentals that map conceptually to enterprise RDF/SPARQL implementations such as SAP HANA Cloud Knowledge Graph capabilities.

---

## 5. Learning-First Development Rules

### Most important rule

**Do not build the project autonomously.**

We will build it one small step at a time.

For every development step:

1. Explain the concept we are about to use.
2. Explain why we need it in this project.
3. Show the exact file(s) we would create or modify.
4. Show the proposed code.
5. Explain the important lines of code.
6. Explain what result I should expect when I run it.
7. Stop.
8. Ask me whether I want to proceed with that change / next development step.

Do not continue to the next stage until I approve.

### Do not hide complexity

Do not say only:

> "I created the graph for you."

Instead explain what is happening, for example:

- which statement is the subject
- which value is the predicate
- which value is the object
- whether something is a class or an instance
- whether a triple belongs to ontology/schema or instance data
- what SPARQL pattern is matching

### Do not over-engineer

Prefer the smallest implementation that demonstrates the concept.

If 10 lines of code can teach the idea, do not generate 100 lines.

### Challenge me

Occasionally ask me short conceptual questions before moving on, such as:

- Is `SalesOrder` a class or an instance here?
- What is the predicate in this triple?
- Why would this relationship be useful to an agent?
- Could this have been represented with a relational FK? What does the semantic representation add?

The objective is understanding, not merely obtaining a working repository.

---

## 6. Development Stages

Follow these stages in order unless I explicitly change the plan.

### Stage 0 — Project setup

Goal:

- Create the minimal Python project structure.
- Explain every dependency before installing it.
- Introduce RDFLib only.

Do not create the ontology yet.

Stop after showing the proposed project structure and setup commands.

---

### Stage 1 — RDF fundamentals

Goal:

Understand RDF triples before building an ontology.

Use a tiny example such as:

```text
ACME --places--> SO100
```

Teach:

- subject
- predicate
- object
- URI / IRI at a practical level
- literals
- namespaces

Create only enough Python/RDFLib code to add and print a few triples.

Do not introduce OWL reasoning yet.

---

### Stage 2 — Create the business ontology/schema

Goal:

Define the semantic model for:

- Customer
- SalesOrder
- SalesOrderItem
- Delivery
- Material
- Supplier

and relationships such as:

- places
- fulfilledBy
- contains
- suppliedBy

Clearly distinguish:

```text
Ontology / schema
vs
Instance / business data
```

Use Turtle because it is readable.

Explain the `.ttl` file line by line.

Keep ontology semantics minimal. Do not introduce advanced OWL constructs unless needed for a specific lesson.

---

### Stage 3 — Add instance data

Goal:

Populate the graph with a very small dataset such as:

```text
ACME -> SO100 -> DEL800 -> MAT100 -> SUP300
```

and simple properties such as status.

Explain how the instance triples conform to the ontology/schema.

At this stage, explicitly compare the representation with a normalized relational schema and foreign keys.

---

### Stage 4 — Learn SPARQL manually

Goal:

Query the graph without an LLM.

Start with extremely simple queries:

1. Find an order.
2. Find the customer for an order.
3. Find the delivery for an order.
4. Traverse from order to material.
5. Traverse from order to supplier.

For every SPARQL query:

- show the query
- explain `SELECT`
- explain variables such as `?order`
- explain each triple pattern
- show how graph traversal happens
- show expected results

Do not generate complex SPARQL until I understand basic graph patterns.

---

### Stage 5 — Query the KG from Python

Goal:

Use RDFLib to execute the SPARQL we already understand.

Create small Python functions around graph queries only after showing the raw SPARQL first.

Avoid hiding SPARQL behind abstraction too early.

Example progression:

```text
raw SPARQL
    ↓
Python executes SPARQL
    ↓
small helper function
```

not:

```text
large framework
    ↓
I never see the graph query
```

---

### Stage 6 — Introduce ontology-grounded agent behavior

Do not begin this stage until RDF and SPARQL are comfortable.

Goal:

Add a small LLM-powered agent that can answer questions using the graph.

Before writing code, explain the architecture.

We should explicitly decide together:

- which LLM/API to use
- how the LLM accesses the graph
- whether the LLM generates SPARQL or invokes constrained graph-query functions
- what ontology/schema context is provided to the LLM
- what guardrails prevent arbitrary or invalid graph queries

Do not select an LLM framework automatically.

Start with the simplest possible implementation.

---

### Stage 7 — Compare architectures

Once the basic agent works, help me compare:

#### A. Prompt + tool agent

```text
User
  ↓
LLM
  ↓
Tool descriptions
  ↓
APIs
```

#### B. Ontology-grounded agent

```text
User
  ↓
LLM / Agent
  ↓
Ontology + Knowledge Graph
  ↓
Semantic relationships / facts
```

#### C. Hybrid architecture

```text
                 Ontology / KG
                /
User -> Agent
                \
                 APIs / tools
```

Discuss trade-offs including:

- semantic grounding
- hallucination risk
- explainability
- graph traversal
- cross-domain relationships
- live operational data
- freshness
- source of truth
- governance
- complexity
- maintenance
- scalability

The goal is architectural judgment, not declaring one approach universally better.

---

## 7. Coding Style

Keep code suitable for learning.

Prefer:

- small files
- descriptive names
- plain Python
- explicit SPARQL
- comments only where they add understanding
- type hints when useful but not excessive
- minimal dependencies

Avoid:

- unnecessary design patterns
- premature abstractions
- large class hierarchies
- auto-generated boilerplate
- complex configuration systems
- code that I cannot explain in an interview

If you recommend an abstraction, first show the simpler implementation and explain why the abstraction becomes useful.

---

## 8. How to Work With Me

When I say something technically inaccurate, correct me directly and explain why.

When multiple architectural choices exist, do not silently choose one. Present the relevant trade-off and recommend the simplest option for this learning objective.

If I ask an architectural question, answer that question before generating more code.

If I ask to continue development, continue from the last approved step rather than rebuilding or redesigning the project.

Do not modify multiple files at once unless the current lesson genuinely requires it.

Do not run ahead because you can infer the next steps.

---

## 9. Response Format During Development

For each development step, use roughly this structure:

### Concept
Explain what we are learning.

### Why it matters
Relate it to the ontology-grounded agent.

### Proposed change
Show the file(s) or command(s) involved.

### Code
Show the exact code before applying it.

### Walkthrough
Explain the important parts.

### Expected result
Show what I should expect when running it.

### Check my understanding
Ask one or two short questions when useful.

### Proceed?
Stop and ask whether I want to implement/proceed.

Do not automatically proceed beyond this point.

---

## 10. Context / Notes I May Update

I may add project decisions, learning notes, or constraints here as we progress.

### Current decisions

- Use Python.
- Use RDF / Turtle.
- Use SPARQL.
- Use RDFLib locally.
- Stay local in VS Code initially.
- No HANA Cloud initially.
- No SAP BDC initially.
- No MCP initially.
- No Neo4j.
- No vector database.
- Learning is more important than development speed.
- Every major code change requires explanation and my approval before proceeding.

### My notes

Add notes here as the project evolves.

---

## 11. Start Here

When I first ask you to begin this project:

**Do not create the whole repository.**

Start only with **Stage 0 — Project setup**.

Explain:

1. the minimal directory structure you recommend,
2. why RDFLib is needed,
3. the Python virtual-environment/setup commands,
4. what each initial file will eventually be responsible for.

Then stop and ask whether I want to proceed with creating the project structure.

## 12. Project Structure

The project structure should look something like this as we move step by step.
Do not create all the files at once. We will create as we proceed.
We can add additional files if required.

ontology-grounded-sales-agent/
│
├── CLAUDE.md
├── requirements.txt
│
├── data/
│   └── sales_ontology.ttl
│
├── src/
│   ├── load_graph.py
│   ├── query_graph.py
│   └── agent.py          # later
│
└── README.md

Keep updating README.md as we move step by step.

