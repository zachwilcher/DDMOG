
from sage.graphs.digraph import DiGraph
from magicutils.check_magic import create_from_str

A_str = """\
[0 0 0 0 0 1 1 0 0 0 0 0 0]
[0 0 1 0 0 0 0 1 0 0 0 0 0]
[0 0 0 0 0 0 0 0 0 0 0 1 0]
[0 0 0 0 1 0 0 1 0 0 0 0 0]
[0 0 0 0 0 0 0 0 0 0 0 0 1]
[0 0 0 0 0 0 0 0 1 0 0 0 0]
[0 0 0 0 0 0 0 0 0 0 0 1 0]
[0 0 0 0 0 1 0 0 0 0 0 0 0]
[0 0 0 0 1 0 0 0 0 0 1 0 0]
[0 0 1 0 0 0 0 0 1 0 0 0 0]
[0 1 0 0 0 0 1 0 0 0 0 0 0]
[0 0 0 0 0 0 0 0 0 1 0 0 0]
[1 0 0 1 0 0 0 0 0 0 0 0 0]"""

digraph = create_from_str(A_str)

def print_graph_info(digraph):
    graph = digraph.to_undirected()
    print("Graph info:")
    print(f"order: {graph.order()}")
    print(f"size: {graph.size()}")
    print(f"average_degree: {graph.average_degree()}")
    print(f"chromatic number: {graph.chromatic_number()}")
    print(f"girth: {graph.girth()}")
    print(f"diameter: {graph.diameter()}")
    #print(f"is_circulant: {graph.is_circulant()}")
    print(f"genus: {graph.genus()}")
print_graph_info(digraph)


# ... not in the database