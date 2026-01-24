from productions.production_base import Production

class P1(Production):
    """Production P1: Marks edges of quadrilateral element, marked
        for refinement, for breaking.
    """

    def __init__(self):
        super().__init__(
            name="P1",
            description="Marks edges of quadrilateral element, marked for refinement, for breaking."
        )

    def can_apply(self, graph, **kwargs):
        hyperedge = None

        for edge in graph.edges:
            if edge.label == "Q" and len(edge.nodes) == 4 and edge.R == 1:
                hyperedge = edge
  
        if not hyperedge:
            return False, None
        
        edges_found = []

        nodes = hyperedge.nodes

        for i in range(4):
            node1 = nodes[i]
            node2 = nodes[(i + 1) % 4]
            found_edge = graph.get_edge_between(node1, node2)

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
        if len(edges_found) != 4:
            return False, None
          
        return True, {
            'hyperedge': hyperedge,
            'nodes': hyperedge.nodes,
            'edges': edges_found
        }

    def apply(self, graph, matched_elements):
        """Apply P1 to mark the quadrilateral for refinement."""
        edges = matched_elements['edges']

        for edge in edges:
            edge.R = 1

        return {
            'marked_hyperedge': matched_elements['hyperedge'],
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }
