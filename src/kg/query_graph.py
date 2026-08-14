"""
SPARQL-based query functions for the sales knowledge graph.
Each function wraps one business question as a parameterised SPARQL query.
"""
from rdflib import Graph, Namespace

from .load_graph import load_graph

SALES = Namespace("http://example.org/sales/")


def get_order_status(g: Graph, order_id: str) -> str | None:
    """Return the status of a sales order, or None if not found."""
    query = """
        PREFIX sales: <http://example.org/sales/>
        SELECT ?status
        WHERE {
            ?order  sales:status  ?status .
        }
    """
    for row in g.query(query, initBindings={"order": SALES[order_id]}):
        return str(row.status)
    return None


def get_customer_for_order(g: Graph, order_id: str) -> str | None:
    """Return the customer ID who placed the order, or None if not found."""
    query = """
        PREFIX sales: <http://example.org/sales/>
        SELECT ?customer
        WHERE {
            ?customer  sales:places  ?order .
        }
    """
    for row in g.query(query, initBindings={"order": SALES[order_id]}):
        return str(row.customer).rsplit("/", maxsplit=1)[-1]
    return None


def get_delivery_for_order(g: Graph, order_id: str) -> str | None:
    """Return the delivery ID fulfilling the order, or None if not found."""
    query = """
        PREFIX sales: <http://example.org/sales/>
        SELECT ?delivery
        WHERE {
            ?order  sales:fulfilledBy  ?delivery .
        }
    """
    for row in g.query(query, initBindings={"order": SALES[order_id]}):
        return str(row.delivery).rsplit("/", maxsplit=1)[-1]
    return None


def get_order_details(g: Graph, order_id: str) -> dict | None:
    """
    Traverse order → item → material → supplier in one query.
    Returns material ID, availability status, and supplier ID, or None if not found.
    """
    query = """
        PREFIX sales: <http://example.org/sales/>
        SELECT ?material ?availabilityStatus ?supplier
        WHERE {
            ?order     sales:contains            ?item .
            ?item      sales:references          ?material .
            ?material  sales:availabilityStatus  ?availabilityStatus .
            ?material  sales:suppliedBy          ?supplier .
        }
    """
    for row in g.query(query, initBindings={"order": SALES[order_id]}):
        return {
            "material":            str(row.material).rsplit("/", maxsplit=1)[-1],
            "availability_status": str(row.availabilityStatus),
            "supplier":            str(row.supplier).rsplit("/", maxsplit=1)[-1],
        }
    return None


def main() -> None:
    """Load the graph and print details for each known order."""
    graph = load_graph()

    for order_id in ("SO100", "SO101", "SO102"):
        print(f"Order: {order_id}")
        print(f"  Status   : {get_order_status(graph, order_id)}")
        print(f"  Customer : {get_customer_for_order(graph, order_id)}")
        print(f"  Delivery : {get_delivery_for_order(graph, order_id)}")
        details = get_order_details(graph, order_id)
        if details:
            print(f"  Material : {details['material']}")
            print(f"  Avail.   : {details['availability_status']}")
            print(f"  Supplier : {details['supplier']}")
        print()


if __name__ == "__main__":
    main()
