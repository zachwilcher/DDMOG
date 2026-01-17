"""
Module for checking if digraphs labeled with integers satisfy DDMOG conditions.
All digraphs are assumed to have vertices be the integers 0 through n-1!!!
"""

def get_weights(digraph):
    weights = [0 for _ in range(digraph.order())]

    for edge in digraph.edges(labels=False, ignore_direction=True):

        source = edge[0]
        destination = edge[1]
        source_label = digraph.get_vertex(source)
        destination_label = digraph.get_vertex(destination)

        weights[source] += -destination_label
        weights[destination] += source_label

    return weights

def check_magic(digraph):
    """Check if a digraph is DDMOG."""
    weights = get_weights(digraph)
    return all([weight == 0 for weight in weights])

def get_vertex_imbalance(digraph, vertex):
    return len(digraph.neighbors_in(vertex)) - len(digraph.neighbors_out(vertex))

def get_graph_imbalance(digraph):
    imbalances = [abs(get_vertex_imbalance(digraph, vertex)) for vertex in digraph.vertex_iterator()]
    max_imbalance = max(imbalances)
    return max_imbalance
    

 
