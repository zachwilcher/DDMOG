import sys
from magicutils.distance_magic.io_utils import load


def main():
    if len(sys.argv) != 2:
        print(f"Usage {sys.argv[0]} <matrix>")
        return
    digraph = load(sys.argv[1])

    parts = []
    vertex_id = lambda vertex: (digraph.in_degree(vertex), digraph.out_degree(vertex))

    for vertex in digraph.vertex_iterator():
        id = vertex_id(vertex)
        for part_index in range(len(parts)):
            part_id = vertex_id(parts[part_index][0])
            if id == part_id:
                parts[part_index].append(vertex)
                break
        else:
            parts.append([vertex])
    
    print(f"(in_degree, out_degree): vertices")
    for part in parts:
        print(f"{vertex_id(part[0])}: {list(map(lambda vertex: vertex + 1, part))}")



if __name__ == "__main__":
    main()