"""
A backtracking search over possible DDMOG's on n vertices.

Essentially, for each vertex, we find possible ways to
connect it to other vertices in the graph so that the weight is 0.
Then, upon reaching later vertices, we have an initial weight
that we need to reduce to 0.

"""

import numpy as np
from sage.graphs.digraph import DiGraph

class Solver:

    def __init__(self, coefficients):
        self.coefficients = coefficients

        # list of maximum possible sums on and after each index
        self.maximum_sums = [0] * len(self.coefficients)
        for i in range(len(self.coefficients)):
            for coefficient in self.coefficients[i:]:
                self.maximum_sums[i] += abs(coefficient)
    
    def solve(self, goal):
        
        stack = []
        stack.append((0, np.zeros(len(self.coefficients), dtype=np.int64), 0))

        while len(stack) > 0:
            (index, solution, current_sum) = stack.pop()


            if index == len(solution) or abs(current_sum - goal) > self.maximum_sums[index]:
                if current_sum == goal:
                    yield solution
            elif self.coefficients[index] == 0:
                # ensure we don't waste time on trying to find
                # the right number to use when we just multiply 
                # it with 0.
                stack.append((index + 1, solution, current_sum))
            else:
                #new_solution = np.copy(solution)
                #new_solution[index] = 0
                stack.append((index + 1, solution, current_sum))

                new_solution = np.copy(solution)
                new_solution[index] = 1
                stack.append((index + 1, new_solution, current_sum + self.coefficients[index]))

                new_solution = np.copy(solution)
                new_solution[index] = -1
                stack.append((index + 1, new_solution, current_sum - self.coefficients[index]))

class DDMOGIterator:
    def __init__(self, n):
        self.n = n

        self.base_digraph = DiGraph()
        self.base_digraph.add_vertices(range(self.n))
        for vertex in self.base_digraph.vertex_iterator():
            label = vertex + 1
            self.base_digraph.set_vertex(vertex, label)
    
    def __iter__(self):
        
        vertex_labels = np.empty(self.n, dtype=np.int64)

        for vertex in self.base_digraph.vertex_iterator():
            label = self.base_digraph.get_vertex(vertex)
            vertex_labels[vertex] = label

        solvers = []
        for i in range(self.n):
            # [0, 0, ..., 1, 1]
            # ignore up to and including the current vertex
            mask = np.append(np.zeros(i + 1, dtype=np.int64), np.ones(self.n - (i + 1), dtype=np.int64))
            coefficient_vector = mask * vertex_labels
            solvers.append(Solver(coefficient_vector))

        stack = []

        # start the backtracking at vertex 0 with a goal weight of 0
        stack.append((0, solvers[0].solve(0), None))

        while len(stack) > 0:
            
            (vertex, solver, current_solution) = stack[-1]
            next_solution = next(solver, None)
            stack[-1] = (vertex, solver, next_solution)
            if next_solution is None:
                # no more possible solutions, backtrack
                stack.pop()
            elif vertex == (self.n - 1):
                # found n solutions
                # the current solution should just be all 0s
                # but we can build the graph now.
                yield self.build_graph(stack)
            else:
                new_goal = 0
                next_vertex = vertex + 1
                for vertex, _, solution in stack:
                    label = vertex_labels[vertex]
                    new_goal -= label * solution[next_vertex]
                new_solver = solvers[next_vertex].solve(-new_goal)
                stack.append((next_vertex, new_solver, None))
                

    def build_graph(self, stack):

        digraph = self.base_digraph.copy()

        for vertex, solver, current_solution in stack:
            solution = current_solution
            for other_vertex, edge_orientation in enumerate(solution):
                if edge_orientation == 1:
                    digraph.add_edge(other_vertex, vertex)
                elif edge_orientation == -1:
                    digraph.add_edge(vertex, other_vertex)

        return digraph
             