import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph

output_dir = "./loops/"
os.makedirs(output_dir, exist_ok=True)


def create_initial_graph():
    graph = HyperGraph()

    coords = [(-4, 3), (2, 3), (4.5, 0), (2, -3), (-4, -3), (-5, -1), (-5, 1), (-3, 1), (0, 1), (0, -1), (-3, -1)]

    n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 = [
        graph.add_node(x, y, label='V')
        for x, y in coords
    ]
    borders = {(n1, n2), (n2, n3), (n3, n4), (n4, n5), (n5, n6), (n6, n7), (n7, n1)}
    inner = {(n1, n8), (n2, n9), (n4, n10), (n5, n11), (n8, n9), (n9, n10), (n10, n11), (n11, n8)}
    edges = []
    for i in borders:
        e = graph.add_edge(i[0], i[1], is_border=True)
        e.R = 0
        edges.append(e)

    for i in inner:
        e = graph.add_edge(i[0], i[1], label="E")
        e.R = 0
        edges.append(e)

    # pięciokąt
    p1 = graph.add_hyperedge([n2, n3, n4, n9, n10], label="P")
    p1.R = 0

    q1 = graph.add_hyperedge([n1, n2, n8, n9], label="Q")
    q2 = graph.add_hyperedge([n8, n9, n10, n11], label="Q")
    q1.R = 0
    q2.R = 0

    return graph


if __name__ == "__main__":
    print("Creating initial graph structure...")
    graph = create_initial_graph()

    print("\nGraph structure:")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len([e for e in graph.edges if not e.is_hyperedge()])}")
    print(f"Hyperedges: {len([e for e in graph.edges if e.is_hyperedge()])}")

    print("\nVisualizing graph...")
    graph.visualize(os.path.join(output_dir, "initial_graph.png"))

    print(f"\nGraph saved to: {os.path.join(output_dir, 'initial_graph.png')}")
    print("Done!")
