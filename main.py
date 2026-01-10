# monkey patch

from functools import reduce
from itertools import accumulate

from sage.graphs.digraph import DiGraph
from sage.groups.abelian_gps.abelian_group import AbelianGroup

from magicutils.labeled_graph import LabeledGraph


def create_cycle_graph(labels):
    G = DiGraph()
    length = len(labels)
    for i in range(length):
        G.add_vertex(i)
        G.set_vertex(i, labels[i])

    for source in range(length):
        target = (source + 1) % length
        G.add_edge(source, target)

    return G   


H = AbelianGroup([10])

labels = H.list()

G = create_cycle_graph(labels)

print(check_magic(G))