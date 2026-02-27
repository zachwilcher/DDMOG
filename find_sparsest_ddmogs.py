import sys
import math
from pathlib import Path
from sage.graphs.connectivity import is_connected
from magicutils.distance_magic.ddmog_stitcher import DDMOGStitcher, DDMOGStitcherCallback
from magicutils.distance_magic.io_utils import save
import math

results_directory = "sparsest_ddmogs"
require_connected = False
max_search_time = 3600

# ensure results_directory exists
Path(results_directory).mkdir(parents=True, exist_ok=True)

class MyStitcherCallback(DDMOGStitcherCallback):
    def __call__(self, digraph):

        connected = is_connected(digraph)
        order = digraph.order()

        print(f"Found a {"" if connected else "dis"}connected DDMOG of order {order}.")

        name = f"{results_directory}/order_{order}_ddmog"
        if not connected:
            name += "_not_connected"

        if require_connected and connected:
            save(digraph, name)
            self.stop_search()
        elif not require_connected:
            save(digraph, name)
            self.stop_search()
        
        
def main(starting_order, max_order):
    """Attempts to find a DDMOG with math.ceil(3 * order / 2) edges"""

    for order in range(starting_order, max_order + 1):
        max_size = math.ceil(3 * order / 2)
        stitcher = DDMOGStitcher(order, 3, 4)
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