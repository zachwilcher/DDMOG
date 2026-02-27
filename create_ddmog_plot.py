import sys
from magicutils.distance_magic.io_utils import save_plot, load
from os import listdir
from pathlib import Path

def main(matrix_path, output_path=None):
    """If output_path is None, then try to create the plot in the same directory
    as the matrix path with the same name."""

    digraph = load(matrix_path)


    if output_path is None:
        parent = matrix_path.parents[0]
        stem = matrix_path.stem
        output_path = Path(parent, f"{stem}.png")
    save_plot(digraph, output_path)
    


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <path to adjacency matrix> [output file path]")
    elif len(sys.argv) == 3:
        main(Path(sys.argv[1]), Path(sys.argv[2]))
    elif len(sys.argv) == 2:
        main(Path(sys.argv[1]))