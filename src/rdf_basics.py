"""
Learning reference: demonstrates manual RDF triple creation using RDFLib.
Shows subject, predicate, object structure before introducing Turtle files.
"""
from rdflib import Graph, Namespace, Literal

# A namespace is a base URI — a shared prefix for all our resources.
# EX.ACME expands to: http://example.org/sales/ACME
EX = Namespace("http://example.org/sales/")

# Graph() creates an empty, in-memory RDF graph.
# Think of it like an in-memory table that holds triples instead of rows.
g = Graph()

# Add triples: each call adds one (subject, predicate, object) statement.
g.add((EX.ACME,        EX.places,   EX.SO100        ))  # URI → URI
g.add((EX.SO100,       EX.status,   Literal("DELAYED")))  # URI → Literal
g.add((EX.SO100,       EX.contains, EX.SO100_ITEM10  ))  # URI → URI

# Iterate over the graph and print each triple.
print("All triples in the graph:\n")
for subject, predicate, obj in g:
    print(f"  Subject  : {subject}")
    print(f"  Predicate: {predicate}")
    print(f"  Object   : {obj}")
    print()
