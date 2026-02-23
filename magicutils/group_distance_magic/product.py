from magicutils.labeled_graph import LabeledGraph
from sage.groups.abelian_gps.abelian_group import AbelianGroup

def x_direct(graph_product, lg1, lg2):
    new_graph = graph_product(lg1.graph, lg2.graph)

    gens_orders1 = lg1.group.gens_orders()
    gens_orders2 = lg2.group.gens_orders()
    new_gens_orders = gens_orders1 + gens_orders2
    new_group = AbelianGroup(new_gens_orders)

    # projections into group1 \oplus group2
    p1 = lambda x: new_group(x.list() + [0 for _ in gens_orders2])
    p2 = lambda y: new_group([0 for _ in gens_orders1] + y.list())

    for (v1, v2) in new_graph.vertex_iterator():
        label1 = lg1.graph.get_vertex(v1)
        label2 = lg2.graph.get_vertex(v2)

        new_label = p1(label1) * p2(label2)

        new_graph.set_vertex((v1, v2), new_label)
        #print(label1.list(), "+", label2.list(), "->", new_label.list())
    return LabeledGraph(new_graph, new_group)


def cartesian_direct(lg1, lg2):
    graph_product = lambda g1, g2: g1.cartesian_product(g2)
    return x_direct(graph_product, lg1, lg2)

def tensor_direct(lg1, lg2):
    graph_product = lambda g1, g2: g1.tensor_product(g2)
    return x_direct(graph_product, lg1, lg2)

def lexicographic_direct(lg1, lg2):
    graph_product = lambda g1, g2: g1.lexicographic_product(g2)
    return x_direct(graph_product, lg1, lg2)

def strong_direct(lg1, lg2):
    graph_product = lambda g1, g2: g1.strong_product(g2)
    return x_direct(graph_product, lg1, lg2)