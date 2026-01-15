import itertools

class GraphLabelPermutator:
    def __init__(self, graph):
        self.graph = graph
    
    def __iter__(self):
        vertices = self.graph.vertices()
        for permutation in itertools.permutations(vertices):
            new_graph = self.graph.copy()
            for original_vertex, new_vertex in zip(vertices, permutation):
                label = self.graph.get_vertex(original_vertex)
                new_graph.set_vertex(new_vertex, label)
            yield new_graph


class DiGraphEdgePermutator:
    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        """"Iterate through all possible ways each edge can be oriented in a simple directed graph."""
        edges = self.graph.edges(labels=False)
        for orientations in itertools.product([False,True], repeat=len(edges)):
            new_graph = self.graph.copy()
            for reverse_edge, edge in zip(orientations, edges):
                if reverse_edge is True:
                    new_graph.reverse_edge(edge[0], edge[1])
            yield new_graph
