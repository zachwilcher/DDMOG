from ddm.ddmo_generator import ddmo_generator
from ddm.sagemath import load_graph, save_graph, disjoint_union
from pathlib import Path

H = load_graph(Path("graphs/H.txt"))
W4 = load_graph(Path("graphs/W4.txt"))
O = load_graph(Path("graphs/O.txt"))
Q = load_graph(Path("graphs/Q.txt"))
K33 = load_graph(Path("graphs/K33.txt"))

def add_K33_instances(base_graph, x):
    result = base_graph
    for _ in range(x):
        result = disjoint_union(result, K33)
    return result

def find_ddm_labeling(graph):
    forced_edges = []
    for (u,v,_) in graph.edges():
        forced_edges.append((u,v))

    result = None
    for digraph in ddmo_generator(graph, forced_edges=forced_edges):
        result = digraph
        break
    return result

def create_table(base_graph):
    """Given a DDMOG, add on copies of K33 and find DDM labelings of the new graph until n > 138,
    and summarize the results in a table."""

    s = ""
    s += "\\begin{tabular}{| c | c |}\n"
    s += "\\hline\n"
    s += "\\(n\\) and \\(x\\) & Base Labeling and Difference Triples\\\\\n"
    s += "\\hline\n"

    og_base_graph_labels = []
    for i in range(base_graph.order()):
        label = int(base_graph.get_vertex(i))
        og_base_graph_labels.append(label)
    n = base_graph.order()
    x = 0
    while n + K33.order() <= 138:
        x += 1
        print(f"Adding on {x} copies of K33 to order {base_graph.order()} graph...")
        unlabeled_graph = add_K33_instances(base_graph, x)
        n = unlabeled_graph.order()
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
            # The orientation of K33 that we are using 
            # guarantees the triples will be in the following locations.
            triple1 = [graph.get_vertex(offset + j) for j in [2, 1, 0]]
            triple2 = [graph.get_vertex(offset + j) for j in [5, 4, 3]]
            triples.append(triple1)
            triples.append(triple2)

        s += f"\\(n={n}\\) & \n"
        s += ",".join(map(str,base_graph_labels))
        s += "\\\\\n"
        s += "\\cline{2-2}\n"
        s += f"\\(x={x}\\)\n"

        max_triples_per_row = 10
        for row in range(len(triples) // max_triples_per_row + 1):
            i = row * max_triples_per_row
            if i == len(triples):
                break
            s += "&"
            while (i < len(triples)) and (i // max_triples_per_row == row):
                triple = triples[i]
                triple_str = "(" + ",".join(map(str,triple)) + ")"
                s += triple_str
                if i < len(triples) - 1:
                    s += ","
                i += 1
            s += "\\\\\n"

        s += "\\hline \n"

    s += "\\end{tabular}"
    return s

base_graph = O
with open("test.tex", "w") as f:
    s = create_table(O) 
    f.write(s)
        
