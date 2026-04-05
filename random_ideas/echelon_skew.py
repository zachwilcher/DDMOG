import sys
from magicutils.distance_magic.io_utils import load
import pathlib

def print_echelon_skew(digraph):
    A = digraph.adjacency_matrix()
    S = A.transpose() - A
    print(S.echelon_form())


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <adjacency matrix>")
    path = pathlib.Path(sys.argv[1])
    if path.is_dir():
        for item in path.iterdir():
            if item.suffix == ".txt":
                print(item)
                print_echelon_skew(load(item))
    else:
        digraph = load(path)
        print_echelon_skew(digraph)


if __name__ == "__main__":
    main()