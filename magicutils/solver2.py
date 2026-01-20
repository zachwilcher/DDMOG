
import itertools
from sage.graphs.digraph import DiGraph
import numpy as np
from pathlib import Path

from sage.graphs.connectivity import is_connected

from magicutils.ddmog_iterator import Solver

from ortools.sat.python import cp_model
import math

def save(digraph, name):

    with open(Path(f"{name}.txt"), "w") as f:
        f.write(digraph.adjacency_matrix().str())
    plot = digraph.plot(vertex_labels=lambda vertex: str(digraph.get_vertex(vertex)))
    plot.save(f"{name}.png")

class SolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, choice_vars, rows, n):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.choice_vars = choice_vars
        self.rows = rows
        self.n = n

    def on_solution_callback(self):
        digraph = DiGraph()
        digraph.add_vertices(range(self.n))
        for vertex in digraph.vertex_iterator():
            label = vertex + 1
            digraph.set_vertex(vertex, label)

        for vertex in range(self.n):
            choice = self.value(self.choice_vars[vertex])
            S_row = self.rows[vertex][choice]

            for other_vertex, edge_orientation in enumerate(S_row):
                if edge_orientation == 1:
                    digraph.add_edge(vertex, other_vertex)
                elif edge_orientation == -1:
                    digraph.add_edge(other_vertex, vertex)
        
        if is_connected(digraph):
            print("Found a connected DDMOG!")
            save(digraph, f"results/order_{self.n}_ddmog")

class Solver2:
    def __init__(self, n, min_degree=1, max_degree=None):
        self.solution = None
        self. n = n
        self.stitched = False

        self.min_degree = min_degree
        if max_degree is None:
            max_degree = n - 1
        self.max_degree = max_degree

        solvers = []
        label_vectors = []

        # possible rows in the skew adjacency matrix of a DDMOG
        self.rows = []
        # the number of outgoing and incoming connections for each possible row
        self.degrees = []
        for i in range(n):

            self.degrees.append([])
            self.rows.append([])

            label = i + 1

            # number of columns to the left and right of column i
            l = i
            r = (n - 1) - i

            left_label_vector = np.fromiter(range(1, label), dtype=np.int64)
            right_label_vector = np.fromiter(range(label + 1, self.n + 1), dtype=np.int64)

            solver = None
            if max(l, r) == l:
                solver = Solver(left_label_vector)
                label_vectors.append(right_label_vector)
            else:
                solver = Solver(right_label_vector)
                label_vectors.append(left_label_vector)
            solvers.append(solver)

        # an array with a single 0. 
        one_zero_arr = np.zeros(1, dtype=np.int64)

        for i in range(n):
            
            # number of columns to the left and right of column i
            l = i
            r = (n - 1) - i

            solver = solvers[i]
            label_vector = label_vectors[i]
            coefficients = np.empty(min(l,r), dtype=np.int64)
            for part in itertools.product([-1, 0, 1], repeat=min(l,r)):
                coefficients[:] = part

                goal = -np.dot(coefficients, label_vector)
                gen = solver.solve(goal)
                if max(l,r) == l:
                    for left_part in gen:
                        row = np.concatenate((left_part, one_zero_arr, coefficients))
                        nonzero = np.count_nonzero(row)
                        if nonzero >= self.min_degree and nonzero <= self.max_degree:
                            self.rows[i].append(row)
                            self.degrees[i].append(nonzero)
                else:
                    for right_part in gen:
                        row = np.concatenate((coefficients, one_zero_arr, right_part))
                        nonzero = np.count_nonzero(row)
                        if nonzero >= self.min_degree and nonzero <= self.max_degree:
                            self.rows[i].append(row)
                            self.degrees[i].append(nonzero)
                


    def stitch(self, max_size=None):
        if self.stitched is True:
            return None
        
        if max_size is None:
            max_size = math.comb(self.n, 2)

        model = cp_model.CpModel()

        choice_vars = []
        degree_vars = []
        for i in range(self.n):
            possible_choices = len(self.rows[i])
            if possible_choices == 0:
                raise Exception(f"No possible rows for row {i}!")

            # inclusive range [0, possible_choices - 1]
            choice = model.new_int_var(0, possible_choices - 1, f"choice_{i}")
            choice_vars.append(choice)

            # associate the choice of row with the degree of that choice
            degree = model.new_int_var(self.min_degree, self.max_degree, f"degree_{i}")
            degree_vars.append(degree)
            model.add_element(choice, self.degrees[i], degree)
        

        # iterate over upper right triangle of the skew adjacency matrix
        # we skip the diagonal since it will just be all 0's 
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # need that S_{i,j} = -S_{j,i}
                S_ij = model.new_int_var(-1, 1, f"S_{{{i},{j}}}")
                S_ji = model.new_int_var(-1, 1, f"S_{{{j},{i}}}")
                model.add(S_ij == -S_ji)

                # S_{i,j} and S_{j,i} are one of the entries in our precomputed rows
                model.add_element(choice_vars[i], [row[j] for row in self.rows[i]], S_ij)
                model.add_element(choice_vars[j], [row[i] for row in self.rows[j]], S_ji)


        size = model.new_int_var(0, max_size, "size")
        # degree sum formula to specify the size variable
        model.add(2 * size == sum(degree_vars))

        # maximum graph size constraint!
        model.add(size <= max_size)


        solver = cp_model.CpSolver()
        solution_callback = SolutionCallback(choice_vars, self.rows, self.n)

        # solver.parameters.log_search_progress = True
        solver.parameters.enumerate_all_solutions = True
        status = solver.solve(model, solution_callback)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

            print("Found a solution!")

        self.stitched = True           


