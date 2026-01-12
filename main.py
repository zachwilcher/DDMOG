from magicutils.labeled_graph import LabeledGraph
from magicutils import product
from magicutils import graphs


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

# see if the graph1 is magic

lg = graphs.make_graph1()

print(f"graph1 is {"magic" if lg.check_magic() else "not magic"}")
visualize(lg, "graph1.png")
