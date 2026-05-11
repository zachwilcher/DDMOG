"""Module for interfacing with sagemath"""
import numpy as np
from sage.graphs.digraph import DiGraph
from .text import save_olg, load_olg
from .checks import is_trivial, is_ddm

def get_adj_matrix(digraph):
    """Convert an oriented graph represented by a sagemath DiGraph
    to as numpy adjacency matrix."""
    n = digraph.order()
    vertices = digraph.vertices()
    A = np.zeros((n,n), dtype=np.int8)

    # digraph.adjacency_matrix() returns a sagemath matrix.
    # the docs don't say anything about numpy
    for i, v1 in enumerate(vertices):
        for j, v2 in enumerate(vertices):
            if digraph.has_edge(v1, v2):
                A[i,j] = 1
    return A


def get_label_vec(digraph):
    """Put the labels used for a sagemath graph in a numpy array
    (Assumes the labels are integers).
    """
    n = digraph.order()
    label_vec = np.empty(n, dtype=np.int64)
    vertices = digraph.vertices()
    for i, v in enumerate(vertices):
        label_vec[i] = digraph.get_vertex(v)
    return label_vec

def create_graph(A, label_vec=None):
    """Turn a numpy adjacency matrix into a sagemath DiGraph.
    label_vec can be used to specify the labels used on the graph.
    By default we set the label of vertex i to i + 1.
    """

    n = A.shape[0]
    digraph = DiGraph()
    digraph.add_vertices(range(n))

    if label_vec is None:
        label_vec = np.arange(1, n+1, dtype=np.int64)

    for i in range(n):
        digraph.set_vertex(i, label_vec[i])
        for j in range(n):
            if A[i,j] == 1:
                digraph.add_edge(i,j)
    return digraph

def save_graph(digraph, path): 
    """Write a sagemath graph to disk"""
    A = get_adj_matrix(digraph)
    label_vec = get_label_vec(digraph)
    save_olg(A, label_vec, path)

def load_graph(path):
    """Load a sagemath graph from disk"""
    A, label_vec = load_olg(path)
    digraph = create_graph(A, label_vec)
    return digraph

def save_plot(digraph, path):
    """Create a visual plot of a sagemath graph"""
    plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(path)

def is_graph_trivial(digraph):
    """Check if the graph has any isolated vertices."""
    A = get_adj_matrix(digraph)
    result = is_trivial(A)
    return result

def is_graph_ddm(digraph):
    """Check if the graph has a DDM labeling."""
    A = get_adj_matrix(digraph)
    label_vec = get_label_vec(digraph)
    result = is_ddm(A, label_vec)
    return result