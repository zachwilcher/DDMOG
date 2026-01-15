

def check_magic(digraph):
    """Check if a digraph is DDMOG."""

    weights = [0 for _ in range(digraph.order())]

    for edge in digraph.edges(labels=False, ignore_direction=True):

        source = edge[0]
        destination = edge[1]

        # assume the vertex is the label
        source_index = source - 1
        destination_index = destination - 1

        weights[source_index] += -destination
        weights[destination_index] += source

    return all([weight == 0 for weight in weights])
