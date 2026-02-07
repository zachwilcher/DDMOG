from magicutils.graphs import disjoint_bipartite
from magicutils.check_magic import check_magic, save

digraph = disjoint_bipartite(1)
save(digraph, "waht")
print(check_magic(digraph))
