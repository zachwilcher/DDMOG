import sys
import math
from pathlib import Path
from sage.graphs.connectivity import is_connected
from magicutils.distance_magic.ddmog_stitcher import DDMOGStitcher, DDMOGStitcherCallback
from magicutils.distance_magic.io_utils import save
import math

results_directory = "sparsest_ddmogs"
require_connected = False
max_search_time = 7200

# ensure results_directory exists
Path(results_directory).mkdir(parents=True, exist_ok=True)

class MyStitcherCallback(DDMOGStitcherCallback):
    def __call__(self, digraph):

        connected = is_connected(digraph)
        order = digraph.order()

        print(f"Found a {"" if connected else "dis"}connected DDMOG of order {order}.")

        path_str = f"{results_directory}/order_{order}_ddmog"
        if not connected:
            path_str += "_not_connected"
        path_str += ".txt"
        path = Path(path_str)

        if require_connected and connected:
            save(digraph, path)
            self.stop_search()
        elif not require_connected:
            save(digraph, path)
            self.stop_search()
        
        
def main(starting_order, max_order):
    """Attempts to find a DDMOG with math.ceil(3 * order / 2) edges
    or math.ceil(3 * order / 2) + 1 edges if n = 2 (mod 4)"""

    for order in range(starting_order, max_order + 1):
        max_size = math.ceil(3 * order / 2)
        # no DDMOGs exist with 3n/2 edges when n = 2 (mod 4)
        if order % 4 == 2:
            max_size += 1
        min_degree = 3
        max_degree = 3
        # The graph can be 3-regular only when n = 0,3 (mod 4)
        if (order % 4 != 0) or (order % 4 != 3):
            max_degree = 4
        stitcher = DDMOGStitcher(order, min_degree, max_degree)
        stitcher.stitch(max_size, MyStitcherCallback, max_search_time)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <starting order> <max order>")
    else:

        starting_order_str = sys.argv[1]
        starting_order = int(starting_order_str)

        max_order_str = sys.argv[2]
        max_order = int(max_order_str)
        main(starting_order, max_order)