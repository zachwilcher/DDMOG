"""Module for working with text and file
representations of oriented and labeled graphs (OLGs)"""
import numpy as np

graph_order_header="graph order"
adjacency_matrix_header = "adjacency matrix"
label_vector_header = "label vector"

def save_olg(A, label_vec, path):
    """Write the adjacency matrix and label vector to a file at path"""
    n = A.shape[0]
    with open(path, "w") as f:
        f.write(graph_order_header + "\n")
        n_str = str(n)
        f.write(n_str + "\n")
        f.write(adjacency_matrix_header + "\n")
        for i in range(n):
            for j in range(n):
                if A[i,j] == 1:
                    f.write("1")
                elif A[i,j] == 0:
                    f.write("0")

                if j != n-1:
                    f.write(" ")
                else:
                    f.write("\n")

        f.write(label_vector_header + "\n")
        for i in range(n):
            label_str = str(label_vec[i])
            f.write(label_str)
            if i != n -1:
                f.write(" ")



def load_olg(path):
    """Load an adjacency matrix and label vector from the file at path."""
    with open(path) as f:
        line = f.readline()
        if line != graph_order_header + "\n":
            raise ValueError("Invalid Format (missing graph order)")

        line = f.readline()
        n = int(line)

        line = f.readline()
        if line != adjacency_matrix_header + "\n":
            raise ValueError("Invalid Format (missing adjacency matrix)")
        A = np.empty(shape=(n,n), dtype=np.int8)
        
        for i in range(n):
            for j in range(n):
                c = f.read(1)
                if c == "0":
                    A[i,j] = 0
                elif c == "1":
                    A[i,j] = 1

                c = f.read(1)
                if (j != n - 1) and (c != " "):
                    raise ValueError("Invalid Format (bad entry spacing for adjacency matrix)")
                
                if (j == n - 1) and (c != "\n"):
                    raise ValueError("Invalid Format (bad row spacing for adjacency matrix)")

        line = f.readline()    
        if line != label_vector_header + "\n":
            raise ValueError("Invalid Format (missing label vector)")
        label_vec = np.empty(n, dtype=np.int64)

        line = f.readline()
        label_strs = line.split(" ")
        if len(label_strs) != n:
            raise ValueError("Invalid Format (incorrect number of labels)")
        for i in range(n):
            label = int(label_strs[i])
            label_vec[i] = label

        return A, label_vec


def old_load_olg(path):
    """Legacy load function for files with adjacency matrices
    in sagemath's matrix.to_str() format."""

    with open(path, "r") as f:
        A_str = f.read()
        rows = A_str.strip().split("\n")
        n = len(rows)
        A = np.zeros((n, n), dtype=np.int8)
        label_vec = np.arange(1, n+1, dtype=np.int64)
        for i, row in enumerate(rows):
            entries = row.strip("[]").split()
            for j, entry in enumerate(entries):
                if entry == '1':
                    A[i,j] = 1
        return A, label_vec

