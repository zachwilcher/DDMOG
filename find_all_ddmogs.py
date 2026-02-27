"""Searches for all DDMOGs using DDMOGIterator"""
import sys
from magicutils.distance_magic.ddmog_iterator import DDMOGIterator
from sage.graphs.connectivity import is_connected
import time

require_connected = True

def main(starting_order = 5, max_order = None):

    try:
        order = starting_order
        ddmogs = 0
        while (max_order is None) or (order < max_order):
            ddmogs = 0
            start_time = time.time()
            for digraph in DDMOGIterator(order):
                if require_connected and is_connected(digraph):
                    ddmogs += 1
                elif not require_connected:
                    ddmogs += 1
            end_time = time.time()
            print(f"Found all {ddmogs} DDMOGs of order {order} in {end_time - start_time:.2f} seconds.")

            order += 1

    except KeyboardInterrupt:
        end_time = time.time()
        print(f"Found {ddmogs} DDMOGs of order {order} in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} [starting_order] [max_order]")

    starting_order = 5
    if len(sys.argv) >= 2:
        starting_order_str = sys.argv[1]
        starting_order = int(starting_order_str)
    max_order = None
    if len(sys.argv) >= 3:
        max_order_str = sys.argv[2]
        max_order = int(max_order_str)
    main(starting_order, max_order)