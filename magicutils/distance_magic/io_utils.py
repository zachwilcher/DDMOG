"""Utility functions for writing and reading DDMOGs to disk.
All digraphs are assumed to have their vertices be the 0 through n - 1.
"""
from pathlib import Path
from sage.graphs.digraph import DiGraph

def save(digraph, name):
    with open(Path(f"{name}.txt"), "w") as f:
        f.write(digraph.adjacency_matrix().str())

def save_plot(digraph, name):
    plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(f"{name}.png")

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

def load(name):
    with open(Path(f"{name}.txt"), "r") as f:
        A_str = f.read()
    digraph = create_from_str(A_str)
    return digraph
