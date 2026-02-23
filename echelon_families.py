from sage.graphs.connectivity import is_connected
from magicutils.distance_magic.ddmog_iterator import DDMOGIterator
from magicutils.distance_magic.ddmog_stitcher import DDMOGStitcher, DDMOGStitcherCallback
from magicutils.distance_magic.check_magic import save
import math
import numpy as np
from pathlib import Path

class MyStitcherCallback(DDMOGStitcherCallback):
    # list of pairs
    # (identifying subgraph, whole digraph)
    graph_classes = []

    count = 0

    def reset():
        MyStitcherCallback.graph_classes = []

    def __call__(self, digraph):
        MyStitcherCallback.count += 1
        if MyStitcherCallback.count > 2:
            self.stop_search()

        flag = False       
        for collection in MyStitcherCallback.graph_classes:
            id_digraph = collection[0]
            if id_digraph.is_isomorphic(digraph):
                collection.append(digraph)
                flag = True
        if flag is False:
            MyStitcherCallback.graph_classes.append([digraph])

        
        


def sparsest_echelon_families(order):

    MyStitcherCallback.reset()
    max_size = math.ceil(3 * order / 2)
    if order % 4 == 2:
        stitcher = DDMOGStitcher(order, 3, 4)
        stitcher.stitch(max_size + 1, MyStitcherCallback)
    if order % 2 == 0:
        stitcher = DDMOGStitcher(order, 3, 3)
        stitcher.stitch(max_size, MyStitcherCallback)
    else:
        stitcher = DDMOGStitcher(order, 3, 4)
        stitcher.stitch(max_size, MyStitcherCallback)
    


order = 17
d = sparsest_echelon_families(order)


n = 0
for collection in MyStitcherCallback.graph_classes:
    n += 1
    print(f"class {n} has {len(collection)} entries")
    k = 0
    for digraph in collection:
        k += 1
        folder_path = Path(f"patterns{order}/{n}")
        folder_path.mkdir(parents=True, exist_ok=True)
        save(digraph, f"patterns{order}/{n}/{k}")