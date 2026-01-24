from productions.production_base import Production
from hypergraph.node import Node

import math

EPSILON = 1e-6


def sort_nodes_clockwise(nodes, center):
    cx, cy = center.x, center.y

    def angle_key(node):
        dx = node.x - cx
        dy = node.y - cy
        return -math.atan2(dy, dx)  # Minus dla clockwise

    # Sortuj listę
    sorted_nodes = sorted(nodes, key=angle_key)
    return sorted_nodes

class P5(Production):
    """Production P5: breaks the quadrilateral element marked for refinement, if all its edges are broken
    it sets value of attribute R of new hyperedges with label Q to 0
    """

    def __init__(self):
        super().__init__(
            name="P5",
            description="Break quadrilateral element if all its edges are broken"
        )

    def can_apply(self, graph):
        """Check if P5 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """

        for hyperedge in graph.edges:
            if hyperedge.label == "Q" and len(hyperedge.nodes) == 4 and hyperedge.R == 1:
                nodes = hyperedge.nodes

                midpoints = []
                for i in range(4):
                    for j in range(4):
                        node_a = nodes[i]
                        node_b = nodes[j]

                        if (node_a.x == node_b.x) and (node_a.y == node_b.y):
                            continue

                        mid_x = (node_a.x + node_b.x) / 2
                        mid_y = (node_a.y + node_b.y) / 2
                        found_mid = None
                        for node in graph.nodes:
                            if abs(node.x - mid_x) < EPSILON and abs(node.y - mid_y) < EPSILON:
                                found_mid = node
                                break

                        midpoints.append(found_mid)

                midpoints = [edge for edge in midpoints if edge is not None]
                unique_edges = list(dict.fromkeys(midpoints))
                midpoints = unique_edges
                edges = midpoints
                # edges = []
                # for i in range(4):
                #     node_a = nodes[i]
                #     node_b = nodes[(i + 1) % 4]
                #
                #     mid_x, mid_y = (node_a.x + node_b.x) / 2, (node_a.y + node_b.y) / 2
                #
                #     found_mid = None
                #     for node in graph.nodes:
                #         if abs(node.x - mid_x) < EPSILON and abs(node.y - mid_y) < EPSILON:
                #             found_mid = node
                #             break
                #
                #     if not found_mid:
                #         break
                #
                #     edges.append(found_mid)

                if len(edges) == 4:
                    return True, {
                        'hyperedge': hyperedge,
                        'nodes': nodes,
                        'edges': edges 
                    }
        
        return False, None

    def apply(self, graph, matched_elements):
        hyperedge = matched_elements['hyperedge']
        n = matched_elements['nodes']
        m = matched_elements['edges']
        # print("tutaj")

        graph.remove_edge(hyperedge)

        center_node = graph.add_node(hyperedge.x, hyperedge.y)
        edges = []

        sorted_nodes_n = sort_nodes_clockwise(n, center_node)
        sorted_nodes_m = sort_nodes_clockwise(m, center_node)
        # print("elo elo 320")
        # for node in sorted_nodes_n:
        #     print(node)
        # print()
        # for node in sorted_nodes_m:
        #     print(node)
        # print()
        shift = 0
        node_1 = sorted_nodes_n[0]
        node_2 = sorted_nodes_n[1]
        # print(node_1)
        # print(node_2)
        x_b = (node_2.x + node_1.x) / 2
        y_b = (node_2.y + node_1.y) / 2
        # print(x_b, y_b)
        while True:
            print(sorted_nodes_m[shift])
            if ((x_b - 0.1 < sorted_nodes_m[shift].x < x_b + 0.1)
                    and (y_b - 0.1 < sorted_nodes_m[shift].y < y_b + 0.1)):
                break
            else:
                shift += 1
        # print("shift" + str(shift))
        for i in range(4):
            edge = graph.add_edge(m[i], center_node)
            edges.append(edge)

        n = sorted_nodes_n
        m = sorted_nodes_m

        graph.add_hyperedge([n[0], m[(0 + shift) % 4], center_node, m[(3 + shift) % 4]], label="Q")
        graph.add_hyperedge([m[(0 + shift) % 4], n[1], m[(1 + shift) % 4], center_node], label="Q")
        graph.add_hyperedge([center_node, m[(1 + shift) % 4], n[2], m[(2 + shift) % 4]], label="Q")
        graph.add_hyperedge([m[(3 + shift) % 4], center_node, m[(2 + shift) % 4], n[3]], label="Q")
        
        print(f"[{self.name}] Broke quadrilateral hyperedge into 4 smaller quadrilaterals.")
        print(f"[{self.name}] Hyperedge R set to 0: {edges}")

        return {
            'marked_hyperedge': matched_elements['hyperedge'],
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }
