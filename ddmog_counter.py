import numpy as np
import sys
import time
from numba import njit

@njit
def sumset(array, goal):
    stack = []
    l = len(array)
    stack.append((l - 1, np.zeros(l, dtype=np.int64)))

    while len(stack) > 0:
        (index, solution) = stack.pop()
        if index == -1:
            if sum(solution) == goal:
                yield solution
        else:
            attempt1 = np.copy(solution)
            stack.append((index - 1, attempt1))

            attempt2 = np.copy(solution)
            attempt2[index] = array[index]
            stack.append((index - 1, attempt2))

            attempt3 = np.copy(solution)
            attempt3[index] = -array[index]
            stack.append((index - 1, attempt3))
@njit
def ddmog_counter(A, vertex, nontrivial_flags=0):
    n = A.shape[0]
    """A is the adjacency matrix"""
    label_vector = np.arange(1, n+1, dtype=np.int64)

    nontrivial_count = 0
    if vertex == n:
        #
        # At this point, A is the adjacency matrix of a nontrivial DDMOG.
        #
        
        nontrivial_count += 1
    else:
        # Compute weight of vertex.
        # S = A - A.T
        # weight = np.dot(S[vertex], label_vector)
        weight = 0
        for i in range(n):
            weight += (A[vertex, i] - A[i, vertex]) * label_vector[i]

        vertex_mask = 1 << vertex

        # For each valid way to connect the current vertex to other
        # vertices in the graph, move on to the next vertex.
        for solution in sumset(label_vector[vertex + 1:], -weight):

            # copy state
            A_copy = np.copy(A)
            new_flags = nontrivial_flags

            # Add edges into or out of vertex according to solution
            for label in solution:
                other_vertex = abs(label) - 1

                # If there is an arc between vertex and other_vertex, update 
                # flags to save the fact that these vertices are not isolated.
                other_vertex_mask = 1 << other_vertex
                if label != 0:
                    new_flags |= vertex_mask
                    new_flags |= other_vertex_mask

                if label > 0:
                    A_copy[vertex, other_vertex] = 1
                elif label < 0:
                    A_copy[other_vertex, vertex] = 1

            # Only recurse if the current vertex is not isolated
            if (new_flags & vertex_mask) == vertex_mask:
                nontrivial_count += ddmog_counter(A_copy, vertex + 1, new_flags)

    return nontrivial_count

def main(n):
    start_time = time.time()
    A = np.zeros(shape=(n,n), dtype=np.int64)
    nontrivial_count = ddmog_counter(A, 0)
    end_time = time.time()
    print(f"Found {nontrivial_count} nontrivial DDMOGs of order {n} in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <number of vertices>")
    else:
        n = int(sys.argv[1])
        main(n)   
    

