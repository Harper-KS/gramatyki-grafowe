from productions.production_base import Production
from hypergraph.hypergraph import HyperGraph
from typing import Dict, Optional, Tuple
import math

EPSILON = 1e-6

class P8(Production):
    def __init__(self):
        super().__init__(
            name="P8",
            description="Break pentagonal element marked for refinement into quadrilaterals"
        )
    
    def can_apply(self, graph, hyperedge=None):
        edges_to_check = graph.edges
        for edge in edges_to_check:
            if not edge.is_hyperedge():
                continue
            if edge.label != "P" or len(edge.nodes) != 5:
                continue
            if getattr(edge, 'R', 0) != 1:
                continue
            
            nodes = edge.nodes
            found_edges = []

            midpoints = []
            all_midpoints_found = True
            for i in range(5):
                for j in range(5):
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
            for m in midpoints:
                print(m)

            for i in range(5):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 5]
                
                found_edge = graph.get_edge_between(node1, node2)
                found_edges.append(found_edge)
                n3 = nodes[(i + 2) % 5]
                found_edge_3 = graph.get_edge_between(node1, n3)
                n4 = nodes[(i + 3) % 5]
                found_edge_4 = graph.get_edge_between(node1, n4)
                n5 = nodes[(i + 4) % 5]
                found_edge_5 = graph.get_edge_between(node1, n5)
                found_edges.append(found_edge_3)
                found_edges.append(found_edge_4)
                found_edges.append(found_edge_5)

            if len(midpoints) == 5:
                return True, {
                    'pentagon_hyperedge': edge,
                    'nodes': nodes,
                    'edges': found_edges,
                    'midpoints': midpoints
                }
            
        return False, None
    
    def apply(self, graph, matched_elements, midpoints=None):

        pentagon_he = matched_elements['pentagon_hyperedge']
        nodes = matched_elements['nodes']
        edges = matched_elements['edges']
        midpoints = matched_elements['midpoints']
        
        graph.remove_edge(pentagon_he)

        centroid_x = sum(node.x for node in nodes) / 5
        centroid_y = sum(node.y for node in nodes) / 5
        # centroid_z = sum(getattr(node, 'z', 0) for node in nodes) / 5

        # dodajemy centrale V
        centroid_node = graph.add_node(centroid_x, centroid_y)
        print("in P8 (apply)")
            
        # dadajemy krawedz pomiedzy srodiem a midpointami
        for midpoint in midpoints:
            print("Midpoint: ", midpoint.label)
            graph.add_edge(centroid_node, midpoint, 
                        is_border=False)
        
        # dodajemy quady
        new_quads = []

        nodes[3], nodes[4] = nodes[4], nodes[3]
        midpoints[0], midpoints[1] = midpoints[1], midpoints[0]

        for i in range(5):
            vertex = nodes[i]
            mid_next = midpoints[i]
            mid_prev = midpoints[(i + 1) % 5]

            quad_nodes = [vertex, mid_next, centroid_node, mid_prev]
            quad_he = graph.add_hyperedge(quad_nodes, label="Q")
            quad_he.R = 0
            new_quads.append(quad_he)
        
                
        return {
            'original_pentagon': pentagon_he,
            'centroid': centroid_node,
            'midpoints': midpoints,
            'new_quadrilaterals': new_quads,
            'nodes': nodes
        }
