
def get_special_O_vertices(O):
    O_undirected = O.to_undirected()
    vertices = list(O_undirected.get_vertices().keys())
    
    A = O_undirected.adjacency_matrix(vertices=vertices)
    walks = A ** 3

    # the non-special vertices are those in 3-cycles
    # or those adjacent to vertices in 3-cycles
    non_special_vertices = set()
    for i in range(13):
        if walks[i][i] == 3:
            vertex = vertices[i]
            non_special_vertices.add(vertex)
            n_set = set(O_undirected.neighbors(vertex))
            non_special_vertices.update(n_set)
    vertex_set = set(vertices)
    return list(vertex_set - non_special_vertices)

def get_special_H_vertex(H):
    H_undirected = H.to_undirected()
    vertices = list(H_undirected.get_vertices().keys())
    A = H_undirected.adjacency_matrix(vertices=vertices)
    walks = A ** 3
    claw_vertices = []
    for i in range(10):
        if walks[i][i] == 0:
            claw_vertices.append(vertices[i])

    claw_set = set(claw_vertices)
    for vertex in claw_vertices:
        n_set = set(H_undirected.neighbors(vertex))
        if n_set <= claw_set:
            return vertex
    return None