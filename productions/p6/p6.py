from productions.production_base import Production


class P6(Production):
    """
    Production P6: Mark pentagonal element for refinement.
    It sets value of attribute R of the hyperedge with label P to 1.
    """

    def __init__(self):
        super().__init__(
            name="P6",
            description="Mark pentagonal element for refinement"
        )

    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """
        Check if P6 can be applied to the graph.
        """
        # print("inside can_apply P6")
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges
        # print(hyperedge)
        # print(graph.edges)
        # print(hyperedges_to_check)

        count = 0
        for edge in hyperedges_to_check:
            # count += 1
            # print(count)
            # print(edge) # HyperEdge(1.70, 0.00, label=P, R=0, nodes=5)
            # must be hyperedge
            if not edge.is_hyperedge():
                # print("-1")
                continue

            # must be pentagon (label P and 5 nodes)
            if edge.label != "P" or len(edge.nodes) != 5:
                # print("-2")
                continue

            # must not be already marked
            if edge.R != 0:
                # print("-3")
                continue

            # external refinement criterion
            if not refinement_criterion:
                # print("-4")
                continue

            # check if all 5 surrounding edges E exist
            nodes = edge.nodes
            edges_found = []
            # print(nodes)
            for i in range(5):
                n1 = nodes[i]
                n2 = nodes[(i + 1) % 5]
                # print(i, n1, n2)
                # Node(2, -3, 0, label=V) Node(0, 1, 0, label=V), jest hiperedge ale niema edge
                found_edge = graph.get_edge_between(n1, n2)
                # if found_edge is None:
                n3 = nodes[(i + 2) % 5]
                found_edge_3 = graph.get_edge_between(n1, n3)
                n4 = nodes[(i + 3) % 5]
                found_edge_4 = graph.get_edge_between(n1, n4)
                n5 = nodes[(i + 4) % 5]
                found_edge_5 = graph.get_edge_between(n1, n5)

                edges_found.append(found_edge_3)
                edges_found.append(found_edge_4)
                edges_found.append(found_edge_5)
                    # print("-5")
                    # break
                edges_found.append(found_edge)
            # print(edges_found)
            edges_found = [edge for edge in edges_found if edge is not None]
            unique_edges = list(dict.fromkeys(edges_found))
            edges_found = unique_edges
            # print("len(edges_found)")
            # print(len(edges_found))
            # for e in edges_found:
            #     print(e)
            if len(edges_found) == 5:
                # print("-7")
                # print(edge)
                # print(nodes)
                # print(edges_found)
                # print("-7")
                return True, {
                    "hyperedge": edge,
                    "nodes": nodes,
                    "edges": edges_found
                }
        # print("-6")
        return False, None

    def apply(self, graph, matched_elements):
        """
        Mark the pentagon hyperedge (label P) for refinement.
        """

        hyperedge = matched_elements["hyperedge"]

        # mark for refinement
        hyperedge.R = 1

        print(f"[{self.name}] Marked pentagon hyperedge for refinement (R: 0 -> 1)")
        print(f"[{self.name}] Hyperedge: {hyperedge}")

        return {
            "marked_hyperedge": hyperedge,
            "nodes": matched_elements["nodes"],
            "edges": matched_elements["edges"]
        }
