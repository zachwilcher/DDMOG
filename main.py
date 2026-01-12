from magicutils.labeled_graph import LabeledGraph
from magicutils import product
from magicutils import graphs
from magicutils.permutate import GraphLabelPermutator, DiGraphEdgePermutator


def visualize(lg, filename):
    plot = lg.graph.plot(
        vertex_labels = lg.pretty_label,
        vertex_size = 700
    )
    plot.save(filename)

# try out the cartesian direct product with cycle graph
cyclelg = graphs.make_cycle(3)
new_cyclelg = product.cartesian_direct(cyclelg, cyclelg)

print(f"C_3 \\box C_3 is {"magic" if new_cyclelg.check_magic() else "not magic"}")
visualize(new_cyclelg, "cartesian_direct.png")

# try out the tensor direct product with cycle graphs
cyclelg = graphs.make_cycle(3)
new_cyclelg = product.tensor_direct(cyclelg, cyclelg)

print(f"C_3 \\times C_3 is {"magic" if new_cyclelg.check_magic() else "not magic"}")
visualize(new_cyclelg, "tensor_direct.png")

# try out the lexicographic direct product with cycle graphs
cyclelg = graphs.make_cycle(3)
new_cyclelg = product.lexicographic_direct(cyclelg, cyclelg)
print(f"C_3 \\circ C_3] is {"magic" if new_cyclelg.check_magic() else "not magic"}")
visualize(new_cyclelg, "lexicographic_direct.png")

# try out the strong direct product with cycle graphs
cyclelg = graphs.make_cycle(3)
new_cyclelg = product.strong_direct(cyclelg, cyclelg)
print(f"C_3 \\boxtimes C_3 is {"magic" if new_cyclelg.check_magic() else "not magic"}")
visualize(new_cyclelg, "strong_direct.png")

# see if graph1 is magic
lg = graphs.make_graph1()

print(f"graph1 is {"magic" if lg.check_magic() else "not magic"}")
visualize(lg, "graph1.png")

# try out permutations of cyclclg

lg = graphs.make_cycle(4)
label_permutator = GraphLabelPermutator(lg.graph)
found_new_magic_orientation = False
found_antimagic_orientation = False
for i, permuted_graph in enumerate(label_permutator):
    if i == 0:
        continue
    permuted_lg = LabeledGraph(permuted_graph, lg.group)
    is_magic = permuted_lg.check_magic()
    if is_magic and (not found_new_magic_orientation):
        found_new_magic_orientation = True
        print(f"C4 permutation {i} is magic")
        visualize(permuted_lg, f"C4_permutation_{i}.png")
    
    if (not is_magic) and (not found_antimagic_orientation):
        found_antimagic_orientation = True
        print(f"C4 permutation {i} is not magic")
        visualize(permuted_lg, f"C4_permutation_{i}.png")
    
    if found_new_magic_orientation and found_antimagic_orientation:
        break