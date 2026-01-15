
from functools import reduce
from itertools import accumulate
from sage.groups.abelian_gps.abelian_group import AbelianGroup

class LabeledGraph:
    def __init__(self, graph, group=None):
        """If group is none, we assume the vertices on the graph are integer labels and the group is just Z."""
        self.graph = graph
        if group is not None:
            self.group = group
        else:
            self.group = AbelianGroup(1)
            generator = self.group.gen(0)
            for vertex in self.graph.vertex_iterator():
                self.graph.set_vertex(vertex, generator ** vertex)
    

    def compute_weight(self, vertex):
        in_weight = self.group(1)
        for v in self.graph.neighbors_in(vertex):
            in_weight *= self.graph.get_vertex(v)
        out_weight = self.group(1)
        for v in self.graph.neighbors_out(vertex):
            out_weight *= self.graph.get_vertex(v)
        weight = in_weight / out_weight
        # print(f"{vertex} ~ {in_weight.list()} / {out_weight.list()} = {weight.list()}")

        return weight

    def check_magic(self):
        """Determine the weight of each node in the digraph and return True iff each weight in the graph is the same"""
        magic_constant = None
        for x in self.graph.vertex_iterator():

            weight = self.compute_weight(x)

            if magic_constant is None:
                magic_constant = weight
            elif weight != magic_constant:
                return False

        return True
    
    def pretty_label(self, vertex):
        label = self.graph.get_vertex(vertex)
        string = ','.join(map(str, label.list()))
        # only put parenthesis around the powers if there is more than one generator
        if len(self.group.gens()) == 1:
            return string
        else:
            return f"({string})"
