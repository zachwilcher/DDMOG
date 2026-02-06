
from ortools.sat.python import cp_model
import numpy as np



class Callback(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)

    def on_solution_callback(self):
        pass

class SystemSolver:
    def __init__(self, S, x):
        self.S = S
        self.x = x
        self.n = len(x)
    
    def solve(self):

        # find permutations of x such that Sx = 0
        model = cp_model.CpModel()

        index_vars = []
        for i in range(self.n):
            index_var = model.NewIntVar(0, self.n - 1, f'x_{i}')
            index_vars.append(index_var)

        vars = []
        for i in range(self.n):
            model.add_element(index_vars[i], self.x, )
        model.add_all_different(index_vars)

        for i in range(self.n):
            constraint_expr = sum(self.S[i][j] * self.x[index_vars[j]] for j in range(self.n))
            model.Add(constraint_expr == 0)




