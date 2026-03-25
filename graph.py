import sqlite3
import networkx as nx
from pyvis.network import Network


def build_graph():
    conn = sqlite3.connect("data.db")
    G = nx.DiGraph()

    # Load tables
    sales_orders = conn.execute("SELECT * FROM sales_orders").fetchall()
    delivery_items = conn.execute("SELECT * FROM delivery_items").fetchall()
    billing_items = conn.execute("SELECT * FROM billing_items").fetchall()
    payments = conn.execute("SELECT * FROM payments").fetchall()

    # ----------------------------
    # 1. Customer → Order
    # ----------------------------
    for so in sales_orders:
        order = f"order_{so[0]}"
        customer = f"cust_{so[1]}"

        G.add_node(order)
        G.add_node(customer)
        G.add_edge(customer, order)

    # ----------------------------
    # 2. Order → Delivery
    # ----------------------------
    order_to_delivery = {}

    for d in delivery_items:
        delivery = f"del_{d[0]}"
        order = f"order_{d[1]}"

        G.add_node(delivery)
        G.add_node(order)

        G.add_edge(order, delivery)

        order_to_delivery.setdefault(d[1], set()).add(d[0])

    # ----------------------------
    # 3. Delivery → Billing
    # ----------------------------
    for b in billing_items:
        billing_doc = b[0]
        order = b[3]  # referenceSdDocument

        if order in order_to_delivery:
            for delivery in order_to_delivery[order]:
                G.add_edge(f"del_{delivery}", f"bill_{billing_doc}")

    # ----------------------------
    # 4. Billing → Product
    # ----------------------------
    for b in billing_items:
        bill = f"bill_{b[0]}"
        product = f"prod_{b[1]}"
        order = f"order_{b[3]}"

        G.add_node(product)
        G.add_edge(bill, product)

        # Product → Order (optional but useful)
        G.add_edge(product, order)

    # ----------------------------
    # 5. Billing → Payment
    # ----------------------------
    for p in payments:
        pay = f"pay_{p[0]}"
        bill_ref = f"bill_{p[1]}"

        G.add_node(pay)
        G.add_edge(bill_ref, pay)

    return G


# ----------------------------------------
# GRAPH VISUALIZATION WITH HIGHLIGHTING
# ----------------------------------------

def save_graph(highlight_nodes=None):
    if highlight_nodes is None:
        highlight_nodes = set()

    G = build_graph()
    net = Network(height="650px", directed=True)

    # Expand highlight (neighbors)
    expanded = set(highlight_nodes)
    for node in highlight_nodes:
        if node in G:
            expanded.update(G.neighbors(node))
            expanded.update(G.predecessors(node))

    # Node colors
    def get_color(node):
        if node.startswith("cust_"):
            return "red"
        elif node.startswith("order_"):
            return "purple"
        elif node.startswith("del_"):
            return "orange"
        elif node.startswith("bill_"):
            return "blue"
        elif node.startswith("prod_"):
            return "green"
        elif node.startswith("pay_"):
            return "black"
        return "gray"

    # Add nodes
    for node in G.nodes:
        base_color = get_color(node)

        if not highlight_nodes:
            color = base_color
            size = 10
        else:
            if node in expanded:
                color = base_color
                size = 18
            else:
                color = "lightgray"
                size = 5

        net.add_node(node, label=node, color=color, size=size)

    # Add edges
    for u, v in G.edges:
        if not highlight_nodes:
            net.add_edge(u, v)
        else:
            if u in expanded and v in expanded:
                net.add_edge(u, v, color="black", width=2)
            else:
                net.add_edge(u, v, color="lightgray", width=1)

    # Layout tuning
    net.repulsion(node_distance=180, central_gravity=0.1)

    net.save_graph("graph.html")


def save_filtered_graph(highlight_nodes):
    if not highlight_nodes:
        return  # nothing to show

    G = build_graph()

    # 🔥 Expand neighborhood
    expanded = set(highlight_nodes)

    for node in highlight_nodes:
        if node in G:
            expanded.update(G.neighbors(node))
            expanded.update(G.predecessors(node))

    # 🔥 Create subgraph
    subGraph = G.subgraph(expanded)

    net = Network(height="500px", directed=True)

    def get_color(node):
        if node.startswith("cust_"):
            return "red"
        elif node.startswith("order_"):
            return "purple"
        elif node.startswith("del_"):
            return "orange"
        elif node.startswith("bill_"):
            return "blue"
        elif node.startswith("prod_"):
            return "green"
        elif node.startswith("pay_"):
            return "black"
        return "gray"

    # Add nodes
    for node in subGraph.nodes:
        net.add_node(node, label=node, color=get_color(node), size=20)

    # Add edges
    for u, v in subGraph.edges:
        net.add_edge(u, v, color="black", width=2)

    net.repulsion(node_distance=200)

    net.save_graph("filtered_graph.html")
