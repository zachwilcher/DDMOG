from sage.graphs.connectivity import is_connected
from magicutils.graphs import create_bipartite
from magicutils.check_magic import check_magic
from magicutils.ddmog_iterator import DDMOGIterator
import numpy as np
import time
from pathlib import Path


graph_number = 1 
order = 6
dir_path = Path(f"ddmog_order_{order}")
dir_path.mkdir(parents=True, exist_ok=True)

start_time = time.time()
for digraph in DDMOGIterator(order):
    if is_connected(digraph):
        end_time = time.time()
        print(f"found a ddmog in {end_time - start_time} seconds")
        plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
        plot.save(f"ddmog_order_{order}/{graph_number}.png")
    graph_number += 1

    start_time = time.time()