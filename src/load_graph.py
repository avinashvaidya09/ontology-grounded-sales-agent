from rdflib import Graph

g = Graph()
g.parse("data/sales_ontology.ttl", format="turtle")

print(f"Loaded {len(g)} triples\n")

for subject, predicate, obj in g:
    print(f"  Subject  : {subject}")
    print(f"  Predicate: {predicate}")
    print(f"  Object   : {obj}")
    print()
