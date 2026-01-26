from sage.graphs.connectivity import is_connected
from magicutils.ddmog_iterator import DDMOGIterator
from magicutils.ddmog_stitcher import DDMOGStitcher
import time
import math

def find_sparsest_ddmog(order):

    print(f"Searching for the sparsest DDMOG of order {order}...")
    start_time = time.time()
    sparsest_digraph = None
    ddmogs = 0
    for digraph in DDMOGIterator(order):
        if is_connected(digraph):
            ddmogs += 1
            if (sparsest_digraph is None) or (digraph.size() < sparsest_digraph.size()):
                sparsest_digraph = digraph
    
        if (ddmogs > 0) and (ddmogs % 100000 == 0):
            print(f"Found {ddmogs} DDMOGs in {time.time() - start_time:.2f} seconds...")
    
    print(f"Found all {ddmogs} DDMOGs of order {order} in {time.time() - start_time:.2f} seconds.")
    

#for order in range(5, 10):
#    find_sparsest_ddmog(order)

order = 8
#max_size = math.ceil(3 * order / 2) 
start_time = time.time()
stitcher = DDMOGStitcher(order)
print(f"Initialized DDMOG stitcher in {time.time() - start_time:.2f} seconds.")
start_time = time.time()
solution_count = 0
def callback(digraph):
    global start_time
    global solution_count
    if is_connected(digraph):
        solution_count += 1
        #print(f"Found {solution_count} DDMOGs of order {order} in {time.time() - start_time:.2f} seconds")
stitcher.stitch(None, callback)
print(f"Completed stitching in {time.time() - start_time:.2f} seconds.")
print(f"Found {solution_count} DDMOGs of order {order}.")
