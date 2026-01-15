
from sage.graphs.digraph import DiGraph
from sage.groups.abelian_gps.abelian_group import AbelianGroup
from magicutils.labeled_graph import LabeledGraph
import itertools

def make_graph1():
    edges = [
        (1,2), (1,4), (6,1),
        (2,3), (2,4), (6,2),
        (4,3), (3,6),

        (5,6), (7,5), (8,5), (5,9),
        (6,7), (6,8), (10,6),
        (8,7), (9,7), (7,10),
        (9,8), (8,10),
        (10,9)
    ]
    graph = DiGraph(edges)

    return LabeledGraph(graph)

def make_cycle(length):
    group = AbelianGroup([length])
    labels = group.list()

    graph = DiGraph()
    length = len(labels)
    for i in range(length):
        graph.add_vertex(i)
        graph.set_vertex(i, labels[i])

    for source in range(length):
        target = (source - 1) % length
        graph.add_edge(source, target)


    return LabeledGraph(graph, group)

class PossibleGraphIterator:
    def __init__(self, n, staring_size = 1, ending_size=None):
        self.n = n
        self.starting_size = staring_size
        self.ending_size = ending_size

        self.graph = DiGraph()
        for i in range(1, self.n + 1, 1):
            self.graph.add_vertex(i)
        
        self.possible_edges = []
        for x in range(1, self.n + 1, 1):
            for y in range(x + 1, self.n + 1, 1):
                # edge = f"({x},{y})"
                edge = (x,y)
                self.possible_edges.append(edge)

        if self.ending_size is None:
            self.ending_size = len(self.possible_edges)
        

    def __iter__(self):
        """Iterate through all possible directed graphs on n vertices."""

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
                    
