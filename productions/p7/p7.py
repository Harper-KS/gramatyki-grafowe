from productions.production_base import Production


class P7(Production):

    '''
    Production P7: marks edges of pentagonal element, 
    marked for refinement, for breaking,
    it sets value of attribute R of each hyperedge with label E to 1
    '''

    def __init__(self):
        super().__init__(
            name="P7",
            description="Mark edges of pentagonal element for breaking",
        )

    def can_apply(self, graph, hyperedge=None):
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            if edge.label != "P" or len(edge.nodes) != 5 or edge.R != 1:
                continue

            nodes = edge.nodes
            edges_found = []

            for i in range(5):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 5]
                found_edge = graph.get_edge_between(node1, node2)

                edges_found.append(found_edge)
                n3 = nodes[(i + 2) % 5]
                found_edge_3 = graph.get_edge_between(node1, n3)
                n4 = nodes[(i + 3) % 5]
                found_edge_4 = graph.get_edge_between(node1, n4)
                n5 = nodes[(i + 4) % 5]
                found_edge_5 = graph.get_edge_between(node1, n5)
                edges_found.append(found_edge_3)
                edges_found.append(found_edge_4)
                edges_found.append(found_edge_5)
                edges_found.append(found_edge)

            edges_found = [edge for edge in edges_found if edge is not None]
            unique_edges = list(dict.fromkeys(edges_found))
            edges_found = unique_edges

            if len(edges_found) == 5:
                return True, {
                    "hyperedge": edge,
                    "nodes": nodes,
                    "edges": edges_found,
                }

        return False, None

    def apply(self, graph, matched_elements):

        for e in matched_elements["edges"]:
            e.R = 1

        print("Successfully applied P7")

        return {
            "hyperedge": matched_elements["hyperedge"],
            "nodes": matched_elements["nodes"],
            "marked_edges": matched_elements["edges"],
        }
