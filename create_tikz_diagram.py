import networkx as nx
import sys
from ddm.text import load_olg
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <path to graph> <output file path>")
        return
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    A,label_vec = load_olg(input_path)
    G = nx.from_numpy_array(A + A.T)
    n = A.shape[0]

    positions = nx.kamada_kawai_layout(G)
    
    with open(output_path, "w") as f:
        f.write("\\begin{tikzpicture}[scale=3]\n")
        f.write("   \\tikzset{\n")
        f.write("       labeled_vertex/.style = {circle, draw=black, fill=white, inner sep = 1.5pt, text=black, minimum size=20pt, very thick},\n")
        f.write("       arc/.style = {->, very thick}\n")
        f.write("   };\n")

        for vertex in positions.keys():
            pos = positions[vertex]
            label = label_vec[vertex]
            f.write(f"  \\node[labeled_vertex] ({label}) at ({pos[0]:.2f}, {pos[1]:.2f}) {{{label}}};\n")
        for vertex in range(n):
            for other in range(n):
                if A[vertex, other] == 1:
                    f.write(f"  \\draw[arc] ({label_vec[vertex]}) to ({label_vec[other]});\n")
            
        f.write("\\end{tikzpicture}\n")

if __name__ == "__main__":
    main()