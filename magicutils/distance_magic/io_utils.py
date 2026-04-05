"""Utility functions for writing and reading DDMOGs to disk.
All digraphs are assumed to have their vertices be the integers 0 through n - 1.
"""
from sage.graphs.digraph import DiGraph

def save(digraph, path):
    # ensure we save the adjacency matrix
    # so that the ith row corresponds to the vertex with label - 1
    vertices = list(range(digraph.order()))
    for vertex in digraph.vertex_iterator():
        label = digraph.get_vertex(vertex)
        vertices[label - 1] = vertex
    with open(path, "w") as f:
        f.write(digraph.adjacency_matrix(vertices=vertices).str())

def save_plot(digraph, path):
    plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(path)

def create_from_str(A_str):
    rows = A_str.strip().split("\n")
    n = len(rows)
    digraph = DiGraph()
    digraph.add_vertices(range(n))

    for i in range(n):
        digraph.set_vertex(i, i+1)

    for i, row in enumerate(rows):
        entries = row.strip("[]").split()
        for j, entry in enumerate(entries):
            if entry == '1':
                digraph.add_edge((i, j))
    return digraph

def load(path):
    with open(path, "r") as f:
        A_str = f.read()
    digraph = create_from_str(A_str)
    return digraph
