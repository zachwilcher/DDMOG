import numpy as np

def is_ddm(A, label_vec):
    """Check if the oriented graph represented by A is ddm when vertex i is labeled with label_vec[i]"""
    S = A.T - A
    weights = S @ label_vec
    return np.all(weights == weights[0])

def is_trivial(A):
    """Check if the oriented graph represented by A has any isolated vertices."""
    degrees = np.sum(A, axis=0) + np.sum(A, axis=1)
    return np.any(degrees == 0)

def is_connected(A):
    """Check whether the oriented graph represented by A is (weakly) connected.
    That is, if the underlying undirected graph is connected.
    """

    # Simple bfs search through the graph's vertices
    n = A.shape[0]

    visited = [False] * n
    stack = []

    stack.append(0)
    visited[0] = True
    while len(stack) > 0:
        vertex = stack.pop()
        for other in range(n):
            if (other != vertex) and (A[vertex, other] == 1 or A[other, vertex] == 1):
                stack.append(other)
                visited[other] = True

    return all(visited)


def is_balanced(A):
    """Check if every vertex in the oriented graph represented by A has the same number
    of incoming arc as outgoing arcs.
    """
    return np.all(np.sum(A, axis=0) == np.sum(A, axis=1))
