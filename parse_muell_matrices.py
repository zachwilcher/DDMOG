import numpy as np
from sage.graphs.digraph import DiGraph
from ddm.sagemath import is_graph_trivial, is_graph_ddm, save_plot
from ddm.ddmog_iterator import DDMOGIterator
from pathlib import Path

def parse_muell_ddmogs():
    muell_ddmogs = []
    n = 8
    path = Path("muell_order_8_adjacency_matrices.txt")
    total_examples = 8240

    with open(path, "r") as f:
        graph_number = 1
        while graph_number <= total_examples:
            f.readline()
            f.readline()
            digraph = DiGraph()
            digraph.add_vertices(range(n))
            for i in range(n):
                digraph.set_vertex(i, i+1)

            for i in range(n):
                row_str = f.readline().strip()
                entries = row_str.split(", ")
                for j, entry in enumerate(entries):
                    if entry == '1':
                        digraph.add_edge((i, j))
            
            if not is_graph_ddm(digraph):
                print(f"Graph {graph_number} is not DDMOG!")
                
            muell_ddmogs.append(digraph)
            graph_number += 1
    return muell_ddmogs



def main():
    n = 8
    muell_graphs = parse_muell_ddmogs()
    non_muell_graphs = []
    for digraph in DDMOGIterator(n):
        if not is_graph_trivial(digraph):
            if digraph not in muell_graphs:
                non_muell_graphs.append(digraph)
    
    save_plot(non_muell_graphs[0], Path("non_muell.png"))

if __name__ == "__main__":
    main()