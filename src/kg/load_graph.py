"""
Loads the sales ontology Turtle file into an RDFLib in-memory graph.
Used as the entry point for all graph queries.
"""
from rdflib import Graph


def load_graph(path: str = "data/sales_ontology.ttl") -> Graph:
    """Parse a Turtle file and return the populated RDF graph."""
    g = Graph()
    g.parse(path, format="turtle")
    return g
