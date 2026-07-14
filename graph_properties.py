"""Module for determining various graph properties to assist in finding graphs in graph databases such as houseofgraphs"""
from pathlib import Path
import sys
from ddm.sagemath import load_graph


def print_dict(d: dict):
    
    for key in d.keys():
        key_str = str(key)
        value_str = str(d[key])
        print(f"{key_str}={value_str}")



def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path to graph>")
        return
    path = Path(sys.argv[1])
    digraph = load_graph(path)
    graph = digraph.to_undirected()
    components = graph.connected_components_subgraphs()
    for i, component in enumerate(components):
        d = dict()
        d["component index"] = i
        d["order"] = component.order()
        d["size"] = component.size()
        d["chromatic_number"] = component.chromatic_number()
        d["girth"] = component.girth()
        d["is_eulerian"] = graph.is_eulerian()
        d["vertex_connectivity"] = component.vertex_connectivity()
        d["eulerian"] = component.is_eulerian()
        d["crossing_number"] = component.crossing_number()
        d["spanning_trees"] = len(list(component.spanning_trees()))

        print_dict(d)
    

if __name__ == "__main__":
    main()