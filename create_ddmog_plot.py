import sys
from magicutils.distance_magic.io_utils import save_plot, load

def main(matrix_path, output_path):
    digraph = load(matrix_path)
    save_plot(output_path, digraph)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <path to adjacency matrix> <output file path>")
    else:
        main(sys.argv[1], sys.argv[2])