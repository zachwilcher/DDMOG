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


for order in range(5, 9 + 1):
    total_oriented_graphs = 3 ** (math.comb(order, 2))
    ddmogs = 0
    start_time = time.time()
    for digraph in DDMOGIterator(order):
        if is_connected(digraph):
            ddmogs += 1
    end_time = time.time()
    print(f"Found {ddmogs} DDMOGs of order {order} in {end_time - start_time:.2f} seconds.")
