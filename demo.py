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
        if is_connected(digraph):
            ddmogs += 1
            if (sparsest_digraph is None) or (digraph.size() < sparsest_digraph.size()):
                sparsest_digraph = digraph
    
            if (ddmogs > 0) and (ddmogs % 100000 == 0):
                print(f"Found {ddmogs} DDMOGs of order {order} in {time.time() - start_time:.2f} seconds...")
    
    print(f"Found all {ddmogs} DDMOGs of order {order} in {time.time() - start_time:.2f} seconds.")
    

#print("Searching for sparsest DDMOGs with orders 5 to 9 by iterating over all DDMOGs.")
#print("---------------------------------------------------------------")
#for order in range(5, 10):
#    find_sparsest_ddmog(order)
#
#print("---------------------------------------------------------------")
#print("\n\n\n\n\n\n\n")

class MyStitcherCallback(DDMOGStitcherCallback):
    found_digraphs = []
    found_ddmog_count = 0

    def __call__(self, digraph):
        MyStitcherCallback.found_ddmog_count += 1

        print(f"Found {MyStitcherCallback.found_ddmog_count} DDMOGs so far...")

        if not is_connected(digraph):
            MyStitcherCallback.found_digraphs.append(digraph)
            save(digraph, f"results/order_{digraph.order()}_ddmog_not_connected")
            self.stop_search()
        
min_order = 20
max_order = 20
print(f"Searching for DDMOGs with ceil(3n/2) edges and {min_order} <= n <= {max_order} with DDMOGStitcher.")
print("---------------------------------------------------------------")
for order in range(min_order, max_order + 1):
    MyStitcherCallback.found_ddmog_count = 0
    MyStitcherCallback.found_digraphs = []
    max_size = math.ceil(3 * order / 2)
    stitcher = DDMOGStitcher(order, 3, 3)
    stitcher.stitch(max_size, MyStitcherCallback)
    print(f"Found {len(MyStitcherCallback.found_digraphs)} DDMOGs of order {order} with at most {max_size} edges.")

