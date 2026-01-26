from sage.graphs.connectivity import is_connected
from magicutils.ddmog_iterator import DDMOGIterator
from magicutils.ddmog_stitcher import DDMOGStitcher, DDMOGStitcherCallback
from magicutils.check_magic import save
import time
import math

def find_sparsest_ddmog(order):

    print(f"Searching for the sparsest DDMOG of order {order}...")
    start_time = time.time()
    sparsest_digraph = None
    ddmogs = 0
    for digraph in DDMOGIterator(order):
        #if is_connected(digraph):
        ddmogs += 1
        if (sparsest_digraph is None) or (digraph.size() < sparsest_digraph.size()):
            sparsest_digraph = digraph
    
        if (ddmogs > 0) and (ddmogs % 500000 == 0):
            print(f"Found {ddmogs} DDMOGs of order {order} in {time.time() - start_time:.2f} seconds...")
    
    print(f"Found all {ddmogs} DDMOGs of order {order} in {time.time() - start_time:.2f} seconds.")
    

print("\n\n\n\n\n\n\n")
print("Searching for sparsest DDMOGs with orders 5 to 9 by iterating over all DDMOGs.")
print("---------------------------------------------------------------")
for order in range(5, 10):
    find_sparsest_ddmog(order)

print("---------------------------------------------------------------")
print("\n\n\n\n\n\n\n")

class MyStitcherCallback(DDMOGStitcherCallback):
    found_digraphs = []

    def __call__(self, digraph):
        MyStitcherCallback.found_digraphs.append(digraph)
        self.stop_search()
        

print("Searching for DDMOGs with ceil(3n/2) edges with orders > 5 with SAT solver.")
print("---------------------------------------------------------------")
for order in range(5, 40):
    MyStitcherCallback.found_digraphs = []
    max_size = math.ceil(3 * order / 2) 
    stitcher = DDMOGStitcher(order, 3, 4)
    stitcher.stitch(max_size, MyStitcherCallback, max_time=3600)
    print(f"Found {len(MyStitcherCallback.found_digraphs)} DDMOGs of order {order} with at most {max_size} edges.")

