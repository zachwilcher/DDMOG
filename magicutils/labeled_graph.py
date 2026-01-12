
from functools import reduce
from itertools import accumulate

class LabeledGraph:
    def __init__(self, graph, group):
        self.graph = graph
        self.group = group
    

    def compute_weight(self, vertex):



        in_weight = self.group(1)
        for v in self.graph.neighbors_in(vertex):
            in_weight *= self.graph.get_vertex(v)
        out_weight = self.group(1)
        for v in self.graph.neighbors_out(vertex):
            out_weight *= self.graph.get_vertex(v)
        weight = in_weight / out_weight
        print(f"{vertex} ~ {in_weight.list()} / {out_weight.list()} = {weight.list()}")

        return weight

    def check_magic(self):
        """Determine the weight of each node in the digraph and return True iff each weight in the graph is the same"""
        is_magic = True
        magic_constant = None
        for x in self.graph.vertex_iterator():

            weight = self.compute_weight(x)

            if magic_constant is None:
                magic_constant = weight
            else:
                is_magic = weight == magic_constant

        return is_magic
    

