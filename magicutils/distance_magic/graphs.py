"""
Module for constructing graphs labeled with integers.
All digraphs are assumed to have vertices be the integers 0 through n-1
where n is the order of the graph.
"""

from sage.graphs.digraph import DiGraph
import itertools
from magicutils.distance_magic.check_magic import get_vertex_imbalance, get_graph_imbalance
from magicutils.skolem import skolem, near_skolem

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

def bipartite_3_3(digraph, part1, part2):
    """Connect the vertices specified in part1 to part2 so they are the parts of K_{3,3}
    with a magic orientation.
    """

    edges = [
        (part2[0], part1[0]), (part1[0], part2[1]), (part1[0], part2[2]),
        (part1[1], part2[0]), (part2[1], part1[1]), (part2[2], part1[1]),
        (part1[2], part2[0]), (part2[1], part1[2]), (part2[2], part1[2]),
    ]
    digraph.add_edges(edges)


def disjoint_bipartite(x):
    """\
    Assumes x >= 0
    Create a DDMOG consisting of 2(x+1) copies of K_{3,3}
    using a Skolem sequence
    """
    # there are 6 * 2*(x + 1) vertices meaning, there
    # are 12 * (x + 1) / 3 parts
    seq_order = 4 * (x + 1)
    skolem_seq = skolem(n)
    # This construction can be found in Skolem's "Some remarks on the triples systems of Steiner"
    difference_triples = [(pair[1] - pair[0], pair[0] + seq_order, pair[1] + seq_order) for pair in skolem_seq]

    digraph = DiGraph()
    n = 6 * 2 * (x + 1)
    digraph.add_vertices(range(n))

    for vertex in digraph.vertex_iterator():
        label = vertex + 1
        digraph.set_vertex(vertex, label)

    for i in range(0, len(difference_triples), 2):
        triple1 = difference_triples[i]
        triple2 = difference_triples[i+1]
        part1 = (triple1[0] - 1, triple1[1] - 1, triple1[2] - 1)
        part2 = (triple2[0] - 1, triple2[1] - 1, triple2[2] - 1)
        bipartite_3_3(digraph, part1, part2)

    return digraph

def wheel_disjoint_bipartite(x):
    """Create a DDMOG consisting of a wheel graph and x copies of K_{3,3}"""


    """
    n = 6x + 5
    The idea is to look at the parity of x. 
    If x is even, then we use the values: 1, n, n - 1, n - 2, n - 3 on the wheel graph.
    If x is odd, then we use the values: 2, n, n - 1, n - 2, n - 3 on the wheel graph.

    What remains is to partition the integers 2, 3, ... n - 4 into difference triples
    or the integers 1, 3, 4, 5, ... n - 4 into difference triples.

    Such a partition can be constructed using near-skolem sequences.
    By taking the defect to be 1 when x is odd and the defect to be 2 when x is even.
    What order sequence?
    There are 6x numbers we wish to partition. Each part contains 3 numbers so,
    there are 6x/3 parts. Hence an order 2x sequence yields the necessary pairs.
    """


    digraph = DiGraph()
    n = 6 * x + 5
    digraph.add_vertices(range(n))

    for vertex in digraph.vertex_iterator():
        label = vertex + 1
        digraph.set_vertex(vertex, label)

    if x % 2 == 0:
        edges = [
            (0, n-1), (0, n-4), (n-2, 0), (n-3, 0),
            (n-1, n-3), (n-3, n-2), (n-2, n-4), (n-4, n-1)
        ]
        digraph.add_edges(edges)
    else:
        edges = [
            (1, n-1), (1, n-4), (n-2, 1), (n-3, 1),
            (n-1, n-2), (n-2, n-3), (n-3, n-4), (n-4, n-1)
        ]
        digraph.add_edges(edges)

    if x == 0:
        return digraph

    seq_order = 2 * x
    skolem_seq = near_skolem(seq_order, 1 if x % 2 == 1 else 2)

    # triples are arranged as (a,b,c)
    # where a + b = c and a <= b
    difference_triples = [(pair[1] - pair[0], pair[0] + seq_order, pair[1] + seq_order) for pair in skolem_seq]
    
    for i in range(0, len(difference_triples), 2):
        triple1 = difference_triples[i]
        triple2 = difference_triples[i+1]
        part1 = (triple1[0] - 1, triple1[1] - 1, triple1[2] - 1)
        part2 = (triple2[0] - 1, triple2[1] - 1, triple2[2] - 1)
        bipartite_3_3(digraph, part1, part2)

    return digraph
