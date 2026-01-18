from sage.graphs.connectivity import is_connected
from magicutils.graphs import create_bipartite
from magicutils.check_magic import check_magic
from magicutils.ddmog_iterator import DDMOGIterator
import numpy as np
import time
from pathlib import Path
import math

def find_sparsest_ddmog(order):

    start_time = time.time()
    sparsest_digraph = None
    ddmogs = 0
    for digraph in DDMOGIterator(order):
        if is_connected(digraph):
            ddmogs += 1
            if (sparsest_digraph is None) or (digraph.size() < sparsest_digraph.size()):
                sparsest_digraph = digraph
    
        if ddmogs % 1000 == 0:
            print(f"Found {ddmogs} DDMOGs...")
    
    end_time = time.time()
    
    print(f"Found {ddmogs} DDMOGs of order {order} in {end_time - start_time:.2f} seconds.")
    
    plot = sparsest_digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(f"sparsest_order_{order}_ddmog.png")


def save(digraph, name):

    with open(Path(f"{name}.txt"), "w") as f:
        f.write(digraph.adjacency_matrix().str())
    plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(f"{name}.png")

min_order = 5
max_order = 14

for order in range(min_order, max_order + 1):

    order_index = order - min_order
    sparsest_ddmog = None
    coarsest_ddmog = None
    highest_degree_ddmog = None

    total_oriented_graphs = 3 ** (math.comb(order, 2))
    ddmogs = 0
    start_time = time.time()
    for digraph in DDMOGIterator(order):
        if is_connected(digraph):
            ddmogs += 1
            
            if (sparsest_ddmog is None) or (digraph.size() < sparsest_ddmog.size()):
                sparsest_ddmog = digraph

            if (coarsest_ddmog is None) or (digraph.size() > coarsest_ddmog.size()):
                coarsest_ddmog = digraph
            
            if (highest_degree_ddmog is None) or (max(digraph.degree()) > max(highest_degree_ddmog.degree())):
                highest_degree_ddmog = digraph

        if ddmogs % 500000 == 0:
            print(f"Found {ddmogs} DDMOGs... of order {order} in {time.time() - start_time}")
    end_time = time.time()
    print(f"Found all {ddmogs} DDMOGs of order {order} in {end_time - start_time:.2f} seconds.")

    save(sparsest_ddmog, f"results/order_{order}_sparsest__ddmog")
    save(coarsest_ddmog, f"results/order_{order}_coarsest_ddmog")
    save(highest_degree_ddmog, f"results/order_{order}_highest_degree_ddmog")



