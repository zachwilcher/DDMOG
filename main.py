# monkey patch


from sage.graphs.digraph import DiGraph
from sage.groups.abelian_gps.abelian_group import AbelianGroup

from magicutils.labeled_graph import LabeledGraph
from magicutils import product


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


H = AbelianGroup([3])
G = create_cycle_graph(H.list())
lg = LabeledGraph(G, H)
newlg = product.tensor_direct(lg, lg)

def pretty_label(lg, vertex):
    label = lg.graph.get_vertex(vertex)

    return f"({','.join(map(str, label.list()))})"

p = newlg.graph.plot(vertex_labels = lambda v: pretty_label(newlg, v))
p.save('graph.png')
print(newlg.check_magic())
