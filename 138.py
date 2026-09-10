"""This module is for finding large disconnected minimal sparsity DDMOGs by tacking on x copies of K_{3,3} to
some minimal sparsity base graph. Valid labelings are found for each graph with brute force using ddm.ddmo_generator,
then the labeling of the base graph and the difference triples used on the K_{3,3} instances are extracted and
written to a human readable latex table."""
from ddm.ddmo_generator import ddmo_generator
from ddm.sagemath import load_graph, save_graph, disjoint_union, hash_graph, get_adj_matrix, get_label_vec
from ddm.text import save_olg
from pathlib import Path
import sys

#H = load_graph(Path("graphs/H.txt"))
#W4 = load_graph(Path("graphs/W4.txt"))
#O = load_graph(Path("graphs/O.txt"))
#Q = load_graph(Path("graphs/Q.txt"))
K33 = load_graph(Path("graphs/K33.txt"))

cache_path = Path(".cache/138_graphs")
cache_path.mkdir(parents=True, exist_ok=True)

def add_K33_instances(base_graph, x):
    result = base_graph
    for _ in range(x):
        result = disjoint_union(result, K33)
    return result

def find_ddm_labeling(graph):

    result = None

    hash = hash_graph(graph, no_labels=True)
    cached_graph_path = (cache_path / hash).with_suffix(".txt")
    if cached_graph_path.is_file():
        result = load_graph(cached_graph_path)
    else:
        forced_edges = []
        for (u,v,_) in graph.edges():
            forced_edges.append((u,v))

        result = None
        for digraph in ddmo_generator(graph, forced_edges=forced_edges):
            result = digraph
            save_graph(result, cached_graph_path)
            break

    return result

def find_less_than_138(base_graph, start, increment):
    """Given a DDMOG, add on copies of K33 and find DDM labelings of the new graph until n > 138,
    and summarize the results in a table."""

    max_graph_order = 138
    max_triples_per_row = 8

    og_base_graph_labels = []
    for i in range(base_graph.order()):
        label = int(base_graph.get_vertex(i))
        og_base_graph_labels.append(label)

    # x is the number of K_{3,3} instances tacked on to the base graph
    x = start

    # s is the string containing the latex code for the table
    s = ""

    while base_graph.order() + K33.order() * x <= max_graph_order:

        #
        # ----- Find a valid labeling of G \sqcup xK_{3,3} -----
        #

        unlabeled_graph = add_K33_instances(base_graph, x)
        print(f"Adding on {x} copies of K33 to order {base_graph.order()} graph (n = {unlabeled_graph.order()})...")

        graph = find_ddm_labeling(unlabeled_graph)
        if graph is None:
            raise RuntimeError("No DDM labeling was found using the specified base graph!")

        base_graph_labels = [0] * base_graph.order()
        for v in range(base_graph.order()):
            label = int(graph.get_vertex(v))
            og_label = og_base_graph_labels[v]
            base_graph_labels[og_label - 1] = label

        triples = []
        for i in range(x):
            offset = base_graph.order() + K33.order() * i
            # The orientation of K33 used guarantees the triples will be in the following locations.
            triple1 = [graph.get_vertex(offset + j) for j in [2, 1, 0]]
            triple2 = [graph.get_vertex(offset + j) for j in [5, 4, 3]]
            if (triple1[0] + triple1[1] != triple1[2]) or (triple2[0] + triple2[1] != triple2[2]):
                raise RuntimeError("The labeling found does not have difference triples in the expected positions!")

            triples.append(triple1)
            triples.append(triple2)

        A = get_adj_matrix(base_graph)
        n = base_graph.order() + K33.order() * x
        base_graph_path = Path(f"138/{n}-base-graph.txt")
        save_olg(A, base_graph_labels, base_graph_path)
        triples_path = Path(f"138/{n}-difference-triples.txt")
        with open(triples_path, "w") as f:
            f.write("difference triples\n")
            for triple in triples:
                f.write(f"({triple[0]}, {triple[1]}, {triple[2]})\n")

        x += increment


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <path to base graph> <start> <increment>")
        return 1
    base_graph_path = Path(sys.argv[1])
    start = int(sys.argv[2])
    increment = int(sys.argv[3])
    base_graph = load_graph(base_graph_path)
    find_less_than_138(base_graph, start, increment)

if __name__ == "__main__":
    main()