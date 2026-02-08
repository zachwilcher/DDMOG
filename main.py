from magicutils.graphs import disjoint_bipartite
from magicutils.check_magic import check_magic, save




digraph = disjoint_bipartite(6)

save(digraph, "waht")
