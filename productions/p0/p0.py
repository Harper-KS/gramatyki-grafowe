from productions.production_base import Production

class P0(Production):
    """Production P0: Mark quadrilateral element for refinement.
    It sets value of attribute R of the hyperedge with label Q to 1
    """

    def __init__(self):
        super().__init__(
            name="P0",
            description="Mark quadrilateral element for refinement"
        )

    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """Check if P0 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges
        # print(1)
        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                # print(2)
                continue

            # Check if it's a quadrilateral (label Q and 4 nodes)
            if edge.label != "Q" or len(edge.nodes) != 4:
                # print(3)
                continue

            # Check if R = 0 (not yet marked for refinement)
            if edge.R != 0:
                # print(4)
                continue

            # Check refinement criterion
            if not refinement_criterion:
                # print(5)
                continue

            # Find the 4 edges connecting the nodes
            nodes = edge.nodes
            edges_found = []

            for i in range(4):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 4]
                found_edge = graph.get_edge_between(node1, node2)
                # if found_edge is None:
                #     print("geg")
                #     break
                edges_found.append(found_edge)
                edges_found.append(found_edge)
                n3 = nodes[(i + 2) % 4]
                found_edge_3 = graph.get_edge_between(node1, n3)
                n4 = nodes[(i + 3) % 4]
                found_edge_4 = graph.get_edge_between(node1, n4)
                edges_found.append(found_edge_3)
                edges_found.append(found_edge_4)

            edges_found = [edge for edge in edges_found if edge is not None]
            unique_edges = list(dict.fromkeys(edges_found))
            edges_found = unique_edges
            # print(len(edges_found))
            if len(edges_found) == 4:
                return True, {
                    'hyperedge': edge,
                    'nodes': nodes,
                    'edges': edges_found
                }
        # print(-1)
        return False, None

    def apply(self, graph, matched_elements):
        """Apply P0 to mark the quadrilateral for refinement."""
        hyperedge = matched_elements['hyperedge']

        # Mark the hyperedge for refinement
        hyperedge.R = 1

        print(f"[{self.name}] Marked quadrilateral hyperedge for refinement (R: 0 -> 1)")
        print(f"[{self.name}] Hyperedge: {hyperedge}")

        return {
            'marked_hyperedge': hyperedge,
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }
