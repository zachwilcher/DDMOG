import math
from magicutils.ddmog_stitcher import DDMOGStitcher, DDMOGStitcherCallback
from magicutils.check_magic import save
import numpy as np
from sage.graphs.connectivity import connected_components

def get_adjacency_matrix(digraph):
    n = digraph.order()
    A = np.zeros((n, n), dtype=np.int64)
    for i, j, label in digraph.edge_iterator():
        A[i][j] = 1
    return A

class MyStitcherCallback(DDMOGStitcherCallback):
    found_digraphs = []

    def __call__(self, digraph):
        MyStitcherCallback.found_digraphs.append(digraph)
        

order = 12
MyStitcherCallback.found_digraphs = []
max_size = math.ceil(3 * order / 2) 
stitcher = DDMOGStitcher(order, 3, 4)
stitcher.stitch(max_size, MyStitcherCallback, max_time=3600)

print(f"Found {len(MyStitcherCallback.found_digraphs)} DDMOGs of order {order} with at most {max_size} edges.")

digraph = MyStitcherCallback.found_digraphs[0]
save(digraph, "order_12_case_study")
A = get_adjacency_matrix(digraph)
S = np.transpose(A) - A

components = connected_components(digraph)

for vertex in components[0]:
    print(S[vertex][:])

print("---------------")
for vertex in components[1]:
    print(S[vertex][:])
