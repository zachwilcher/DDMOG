"""
We guess that by adding pairs of copies of K_{3,3}
to certain base graphs, the graph remains DDMO. 
However, the labeling scheme using Langford sequences
does not work until n >= 138. 
This program uses a SAT solver to try and guess the remaining cases.
"""
from magicutils.distance_magic.io_utils import load, save
from magicutils.distance_magic.ddmo_generator import ddmo_generator
from magicutils.distance_magic.check_magic import check_magic
from sage.graphs.digraph import DiGraph
from pathlib import Path

output_dir = "disconnected_conjecture"
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Pick out the graphs that we conjectured can be used as base graphs for adding
# on x pairs of K_{3,3} Note that these choices are a bit arbitrary. 
# For example, we probably could have used sparsest_ddmogs/order_20_ddmog.txt
# for the modulo 8 case.
base_graphs = {
    0: DiGraph(),
    1: load("sparsest_ddmogs/order_13_ddmog.txt"),
    2: load("sparsest_ddmogs/order_14_ddmog_not_connected.txt"),
    3: load("sparsest_ddmogs/order_15_ddmog_not_connected.txt"),
    4: load("sparsest_ddmogs/order_16_ddmog_not_connected.txt"),
    5: load("sparsest_ddmogs/order_5_ddmog.txt"),
    6: load("sparsest_ddmogs/order_18_ddmog_not_connected.txt"),
    7: load("sparsest_ddmogs/order_19_ddmog_not_connected.txt"),
    8: load("sparsest_ddmogs/order_32_ddmog_not_connected.txt"),
    9: load("sparsest_ddmogs/order_21_ddmog_not_connected.txt"),
    10: load("sparsest_ddmogs/order_22_ddmog_not_connected.txt"),
    11: load("sparsest_ddmogs/order_11_ddmog_not_connected.txt")
}

K33_pair = load("sparsest_ddmogs/order_12_ddmog_not_connected.txt")

def add_K33_pairs(graph, x):
    """Add x pairs of K_{3,3} to the graph
    with vertices of the K_{3,3} pairs
    starting at n and going up to 12x + n
    i.e. the vertices of the original graph remain
    unchanged.

    Assumes graph vertices are integers from 0 to n - 1

    Note the returned graph has no labels but keeps the edge orientations
    of the original graph.
    """

    n = graph.order()

    result = DiGraph()
    result.add_vertices(range(n + 12 * x))

    for (u,v,_) in graph.edges():
        result.add_edge(u,v)

    other_order = K33_pair.order()
    for i in range(x):
        for (u,v,_) in K33_pair.edges():
            result.add_edge(n + other_order*i + u, n + other_order*i + v)

    return result


def main():
    x = 0
    while True:
        x += 1
        for base_graph in base_graphs.values():
            n = base_graph.order()
            digraph = add_K33_pairs(base_graph, x)
            if (digraph.order() > 138) or (digraph.order() <= 38):
                # We have constructions for > 138 or <= 38 
                continue
            
            # preserve the edge connections of the K_{3,3} pairs
            # since there is essentially only one valid orientation
            forced_edges = []
            for (u,v,_) in digraph.edges():
                if (u >= n) and (v >= n):
                    forced_edges.append((u,v))
            
            print(f"Trying to add {x} pairs of K_3,3 to order {base_graph.order()} graph...")
            for result in ddmo_generator(digraph, forced_edges=forced_edges):
                assert(check_magic(result), "ddmo_generator did not return a DDMOG...")
                print(f"Found DDM orientation and labeling of order {result.order()} graph!")
                name = f"order_{result.order()}_ddmog"
                save(result, f"{output_dir}/{name}.txt")
                break

        # if x > 12, then n >= 12 * x > 144 which we already have constructions for.
        if x > 12:
            break



if __name__ == "__main__":
    main()