import sys
from magicutils.distance_magic.io_utils import load
from pathlib import Path

def test_subgraph(child, parent):
    found_subgraph = parent.subgraph_search(child)
    return found_subgraph

def main():
    if len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} <subgraph> <parent graph>")
    child_path = Path(sys.argv[1])
    parent_path = Path(sys.argv[2])

    children = {}
    if child_path.is_dir():
        for path in child_path.iterdir():
            if path.suffix == ".txt":
                child = load(path)
                children[path] = child
    parents = {}
    if parent_path.is_dir():
        for path in parent_path.iterdir():
            if path.suffix == ".txt":
                parent = load(path)
                parents[path] = parent



if __name__ == "__main__":
    main()