"""
Python program for computing the graph isomorphism classes for a DDMOG with minimal edges.
"""
import sys
import math
from pathlib import Path
from sage.graphs.connectivity import is_connected
from magicutils.distance_magic.ddmog_stitcher import DDMOGStitcher, DDMOGStitcherCallback
from magicutils.distance_magic.io_utils import save, save_plot
import math

# options to force resulting graphs to be connected or disconnected
require_disconnected = True
require_connected = False
save_plots = True
# max search time in seconds
max_search_time = None

assert (not require_disconnected) or (not require_connected)

class MyStitcherCallback(DDMOGStitcherCallback):

    def __call__(self, digraph):
        MyStitcherCallback.solution_count += 1

        connected = is_connected(digraph)
        order = digraph.order()

        print(f"Found a {"" if connected else "dis"}connected DDMOG of order {order}.")

        if require_disconnected and connected:
            return
        if require_connected and (not connected):
            return


        found = False
        for index, graph in enumerate(MyStitcherCallback.digraph_classes):
            if graph.is_isomorphic(digraph):
                found = True
                MyStitcherCallback.digraph_class_sizes[index] += 1
                break
        if not found:
            MyStitcherCallback.digraph_classes.append(digraph)
            MyStitcherCallback.digraph_class_sizes.append(1)

            graph_file_str = f"order_{order}_ddmog"
            graph_file_str += f"_{len(MyStitcherCallback.digraph_classes)}"
            if not connected:
                graph_file_str += "_not_connected"
            graph_file_str += ".txt"
            graph_path = MyStitcherCallback.results_directory / graph_file_str
            save(digraph, graph_path)

            if save_plots:
                save_plot(digraph, graph_path.with_suffix(".png"))
        
        
        
def main(order):
    """Attempts to find a DDMOG with math.ceil(3 * order / 2) edges
    or math.ceil(3 * order / 2) + 1 edges if n = 2 (mod 4)"""

    # ensure results_directory exists
    results_directory_str = f"sparsest_order_{order}_classes"
    results_directory = Path(results_directory_str)
    results_directory.mkdir(parents=True, exist_ok=True)


    max_size = math.ceil(3 * order / 2)
    # no DDMOGs exist with 3n/2 edges when n = 2 (mod 4)
    if order % 4 == 2:
        max_size += 1

    min_degree = 3
    max_degree = 4
    # The graph can be 3-regular only when n = 0 (mod 4)
    if (order % 4 == 0):
        max_degree = 3
            
    # initialize custom class variables ... 
    MyStitcherCallback.results_directory = results_directory
    MyStitcherCallback.solution_count = 0
    MyStitcherCallback.digraph_classes = []
    MyStitcherCallback.digraph_class_sizes = []

    stitcher = DDMOGStitcher(order, min_degree, max_degree)
    stitcher.stitch(max_size, MyStitcherCallback, max_search_time)
    print(MyStitcherCallback.digraph_class_sizes)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <order>")
    else:
        order_str = sys.argv[1]
        order = int(order_str)
        main(order)