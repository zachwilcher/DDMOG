"""
Module for constructing graphs labeled with integers.
All digraphs are assumed to have vertices be the integers 0 through n-1
where n is the order of the graph.
"""

from sage.graphs.digraph import DiGraph
import itertools
from magicutils.check_magic import get_vertex_imbalance, get_graph_imbalance

def create_bipartite(m, n):
    """Requires (m + n)*(m + n + 1) % 4 == 0 and m >= 3 and n >= 3. 
    Create a bipartite graph K_{m,n} with a DDM labeling as specified
    in Theorem 5 of Difference Distance magic oriented graphs by Alison Marr et. al."""

    if not ((m + n)*(m + n + 1) % 4 == 0 and m >= 3 and n >= 3):
        raise ValueError("m and n do not satisfy the necessary conditions.")

    s = m // 4
    t = n // 4
    X1 = None
    X2 = None
    Y1 = None
    Y2 = None

    # The closed interval [a, b] corresponds to list(range(a-1, b)) in python

    if (m % 4 == 0) and (n % 4 == 0):
        X1 = list(range(0, s)) + list(range(3*s + 4 * t, 4*s + 4 * t))
        X2 = list(range(s, 2*s)) + list(range(2*s + 4*t, 3*s + 4*t))
        Y1 = list(range(2*s, 2*s + t)) + list(range(2*s + 3*t, 2*s + 4*t))
        Y2 = list(range(2*s + t, 2*s + 3*t))
    elif (m % 4 == 0) and (n % 4 == 3):
        X1 = list(range(2*t + 1, s + 2*t + 1)) + list(range(3*s + 2*t + 1, 4*s + 2*t + 1))
        X2 = list(range(s + 2*t + 1, 3*s + 2*t + 1))
        Y1 = [4*s + 4*t + 2] + list(range(t + 1, 2*t + 1)) + list(range(4*s + 2*t + 1, 4*s + 3*t + 1))
        Y2 = list(range(0, t + 1)) + list(range(4*s + 3*t + 1, 4*s + 4*t + 2))
    elif (m % 4 == 1) and (n % 4 == 3):
        #TODO
        X1 = None
        X2 = None
        Y1 = None
        Y2 = None
    elif (m % 4 == 1) and (n % 4 == 2):
        #TODO
        X1 = None
        X2 = None
        Y1 = None
        Y2 = None
    elif (m % 4 == 2) and (n % 4 == 2):
        #TODO
        X1 = None
        X2 = None
        Y1 = None
        Y2 = None

    digraph = DiGraph()
    digraph.add_vertices(X1)
    digraph.add_vertices(X2)
    digraph.add_vertices(Y1)
    digraph.add_vertices(Y2)
    # X1 -> Y1 -> X2 -> Y2 -> X1
    digraph.add_edges(itertools.product(X1, Y1))
    digraph.add_edges(itertools.product(Y1, X2))
    digraph.add_edges(itertools.product(X2, Y2))
    digraph.add_edges(itertools.product(Y2, X1))
    # labels are integers 1 through m + n
    # not 0 through m + n - 1
    for vertex in digraph.vertex_iterator():
        label = vertex + 1
        digraph.set_vertex(vertex, label)
    return digraph


def balance_ddmog(digraph):
    """Balance a ddmog with imbalance 1 using 
    Theorem 3.7 from "New results on Difference Distance Magic Labeling.
    Requires that the input digraph has imbalance 1.
    """

    if get_graph_imbalance(digraph) != 1:
        raise ValueError("Input digraph does not have imbalance 1.")

    S_plus = []
    S_minus = []
    new_digraph = digraph.copy()
    for vertex in new_digraph.vertex_iterator():
        # update the labels
        old_label = new_digraph.get_vertex(vertex)
        new_label = old_label + 1
        new_digraph.set_vertex(vertex, new_label)

        # sort the vertex into the appropriate set
        imbalance = get_vertex_imbalance(new_digraph, vertex)
        if imbalance == 1:
            S_plus.append(vertex)
        elif imbalance == -1:
            S_minus.append(vertex)

    new_vertex = digraph.order()
    new_digraph.add_vertex(new_vertex)
    new_digraph.set_vertex(new_vertex, 1)

    for vertex in S_minus:
        new_digraph.add_edge(new_vertex, vertex)
    for vertex in S_plus:
        new_digraph.add_edge(vertex, new_vertex)

    return new_digraph


