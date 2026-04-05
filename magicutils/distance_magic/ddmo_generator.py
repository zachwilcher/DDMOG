"""Python module for iterating through possible 
difference distance magic orientations of a given undirected graph."""

from ortools.sat.python import cp_model
import threading
from queue import Queue
from sage.graphs.digraph import DiGraph


class DDMOSolverSolutionCallback(cp_model.CpSolverSolutionCallback):

    def __init__(self, G, solution_queue, label_vars, dir_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.label_vars = label_vars
        self.G = G
        self.solution_queue = solution_queue
        self.dir_vars = dir_vars
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        # we just build the digraph
        digraph = DiGraph()
        for vertex in self.G.vertex_iterator():
            digraph.add_vertex(vertex)
            label = self.value(self.label_vars[vertex])
            digraph.set_vertex(vertex, label)
        for (u,v), dir_var in self.dir_vars.items():
            if self.value(dir_var) == 1:
                digraph.add_edge(u,v)
            else:
                digraph.add_edge(v,u)
        self.solution_queue.put(digraph)


def ddmo_generator(G, forced_labels={}, forced_edges=[]):
    """
        Find DDM labelings and orientations of an unoriented graph G.
        Note: This function assumes that the vertices of G are integers.
        forced_labels is a dict mapping vertices to labels
        forced_edges is a list of tuples of the form (u,v)
        if (u,v) is in forced_edges, we require that u is directed at v
    """

    n = G.order()
    vertices = G.vertices()

    # create a list of edges with a consistent ordering of the vertices
    edges = []
    for (u, v, _) in G.edge_iterator(sort_vertices=True):
        if u < v:
            edges.append((u,v))
        else:
            edges.append((v,u))

    model = cp_model.CpModel()

    # vertex label variables
    label_vars = {vertex: model.new_int_var(1, n, f"vertex {vertex} label") for vertex in vertices}
    model.add_all_different(list(label_vars.values()))

    for vertex, label in forced_labels.items():
        model.add(label_vars[vertex] == label)

    # edge direction vars
    # (u,v) == True means u is directed at v
    # (u,v) == False means v is directed at u
    dir_vars = {edge: model.new_bool_var(f"edge {edge}") for edge in edges}

    for (u, v) in forced_edges:
        if u < v:
            model.add(dir_vars[(u,v)] == 1)
        else:
            model.add(dir_vars[(v,u)] == 0)

    for u in vertices:
        contributions = []
        for v in G.neighbors(u):
            contrib = model.new_int_var(-n, n, f"contrib_{v}_to_{u}")

            if u < v:
                edge_var = dir_vars[(u, v)]
                # If u -> v then v is an out-neighbor, subtract its label
                model.add(contrib == -label_vars[v]).only_enforce_if(edge_var)
                # If v -> u then v is an in-neighbor, add its label
                model.add(contrib == label_vars[v]).only_enforce_if(edge_var.Not())
            else:
                edge_var = dir_vars[(v, u)]
                # If v -> u then v is an in-neighbor, add its label
                model.add(contrib == label_vars[v]).only_enforce_if(edge_var)
                # If u -> v then v is an out-neighbor, subtract its label
                model.add(contrib == -label_vars[v]).only_enforce_if(edge_var.Not())

            contributions.append(contrib)

        model.add(sum(contributions) == 0)



    solution_queue = Queue()


    solver = cp_model.CpSolver()
    solver.enumerate_all_solutions = True
    #solver.parameters.num_search_workers = 1
    solver.parameters.cp_model_presolve = False
    solver.parameters.symmetry_level = 0

    # --------------------------------------------------------------
    # multi-threading to make the callback work like a generator
    # --------------------------------------------------------------

    def run_solver():
        callback = DDMOSolverSolutionCallback(G, solution_queue, label_vars, dir_vars)
        solver.solve(model, callback)
        # put None in the queue once the solver is done
        solution_queue.put(None)
    
    solver_thread = threading.Thread(target=run_solver)
    solver_thread.start()
    try:
        while True:
            result = solution_queue.get()

            # if None then the solver is done
            if result is None:
                break
            yield result
    finally:
        solver.stop_search()
        solver_thread.join()
