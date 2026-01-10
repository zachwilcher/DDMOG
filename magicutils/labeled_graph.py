
class LabeledGraph:
    def __init__(self, graph, group):
        self.graph = graph
        self.group = group
    

    def compute_weight(self, vertex):

        accumulate = lambda nodes: reduce(lambda a, b: self.graph.get_vertex(a) * self.graph.get_vertex(b), nodes)

        in_nbhd = self.graph.neighbors_in(vertex)
        out_nbhd = self.graph.neighbors_out(vertex)

        weight = accumulate(in_nbhd) - accumulate(out_nbhd)

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
    

