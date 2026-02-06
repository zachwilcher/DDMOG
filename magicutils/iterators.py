"""Module for iterating over variations of DiGraphs"""
import itertools
from sage.graphs.digraph import DiGraph

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

class OrientedGraphIterator:
    def __init__(self, n, starting_size = 0, ending_size=None):
        self.n = n
        self.starting_size = starting_size
        self.ending_size = ending_size

        self.graph = DiGraph()
        for i in range(self.n):
            self.graph.add_vertex(i)
        
        self.possible_edges = []
        for x in range(self.n):
            for y in range(x + 1, self.n):
                # edge = f"({x},{y})"
                edge = (x,y)
                self.possible_edges.append(edge)

        if self.ending_size is None:
            self.ending_size = len(self.possible_edges)
        

    def __iter__(self):
        """Iterate through all possible oriented graphs on n vertices."""

        for size in range(self.starting_size, self.ending_size + 1, 1):

            for combination in itertools.combinations(self.possible_edges, size):

                orientations = itertools.product([False, True], repeat=len(combination))
                for orientation in orientations:

                    new_graph = self.graph.copy()
                    for reverse_edge, edge in zip(orientation, combination):
                        if reverse_edge is False:
                            new_graph.add_edge(edge[0], edge[1])
                        else:
                            new_graph.add_edge(edge[1], edge[0])
                
                    yield new_graph
                    