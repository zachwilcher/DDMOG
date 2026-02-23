
from sage.graphs.digraph import DiGraph
from sage.groups.abelian_gps.abelian_group import AbelianGroup
from magicutils.labeled_graph import LabeledGraph

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

