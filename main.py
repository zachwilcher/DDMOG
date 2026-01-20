from sage.graphs.connectivity import is_connected
from magicutils.graphs import create_bipartite
from magicutils.check_magic import check_magic
from magicutils.ddmog_iterator import DDMOGIterator
from magicutils.solver2 import Solver2
import numpy as np
import time
from pathlib import Path
import math

def save(digraph, name):

    with open(Path(f"{name}.txt"), "w") as f:
        f.write(digraph.adjacency_matrix().str())
    plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(f"{name}.png")

def find_sparsest_ddmog(order):

    start_time = time.time()
    sparsest_digraph = None
    ddmogs = 0
    for digraph in DDMOGIterator(order):
        if is_connected(digraph):
            ddmogs += 1
            if (sparsest_digraph is None) or (digraph.size() < sparsest_digraph.size()):
                sparsest_digraph = digraph
    
        if ddmogs % 100000 == 0:
            print(f"Found {ddmogs} DDMOGs...")
    
    end_time = time.time()
    
    print(f"Found all {ddmogs} DDMOGs of order {order} in {end_time - start_time:.2f} seconds.")
    
    #save(sparsest_digraph, f"sparsest_order_{order}_ddmog")



def find_sparse_ddmog(max_size):
    min_order = 5
    max_order = 20

    for order in range(min_order, max_order + 1):

        order_index = order - min_order
        sparse_ddmog = None

        total_oriented_graphs = 3 ** (math.comb(order, 2))

        iterations = 0
        start_time = time.time()
        for digraph in DDMOGIterator(order, max_size):
            iterations += 1
            if is_connected(digraph):
                sparse_ddmog = digraph
                break
            if iterations % 1000000 == 0:
                print(f"Processed {iterations} graphs in {time.time() - start_time:.2f} seconds...")

        end_time = time.time()
        if sparse_ddmog is not None:
            print(f"Found a order {order} sparse DDMOG in {end_time - start_time:.2f} seconds.")
            #save(sparse_ddmog, f"results/order_{order}_sparse_ddmog")
        else:
            print(f"No order {order} sparse DDMOG found within size limit! (took {end_time - start_time:.2f} seconds)")

        #save(sparsest_ddmog, f"results/order_{order}_sparsest__ddmog")
        #save(coarsest_ddmog, f"results/order_{order}_coarsest_ddmog")
        #save(highest_degree_ddmog, f"results/order_{order}_highest_degree_ddmog")



order = 13
max_size = math.ceil(3 * order / 2) + 1
obj = Solver2(order)
print(f"Created solver with {sum(map(len,obj.rows))} rows")
print("Stitching...")
digraph = obj.stitch(max_size)

if digraph is not None:
    print(check_magic(digraph))
    save(digraph, f"results/order_{order}_ddmog")