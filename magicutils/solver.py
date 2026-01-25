
import numpy as np

class Solver:
    """Solves the subset sum problem where the integers to be summed are given 
    by plus or minus of each of the numbers in the vector 'coefficients'."""
    def __init__(self, coefficients):
        self.coefficients = coefficients
    
    def solve(self, goal, max_vars=None):
        raise NotImplementedError("Subclasses must implement this method.")

class BacktrackingSolverImpl(Solver):
    def __init__(self, coefficients):
        super().__init__(coefficients)

        # list of maximum possible sums on and before each index
        self.maximum_sums = [0] * len(self.coefficients)
        for i in range(len(self.coefficients)):
            for coefficient in self.coefficients[:i+1]:
                self.maximum_sums[i] += abs(coefficient)
    
    def solve(self, goal, max_vars=None):
        """"""
        max_vars = len(self.coefficients) if max_vars is None else max_vars
        
        stack = []
        stack.append((len(self.coefficients) - 1, np.zeros(len(self.coefficients), dtype=np.int64), 0, 0))

        while len(stack) > 0:
            (index, solution, current_sum, nonzero_vars) = stack.pop()


            if index == -1 or \
                abs(current_sum - goal) > self.maximum_sums[index] or \
                (nonzero_vars >= max_vars):
                if current_sum == goal:
                    yield solution
            elif self.coefficients[index] == 0:
                # ensure we don't waste time on trying to find
                # the right number to use when we just multiply 
                # it with 0.
                stack.append((index - 1, solution, current_sum, nonzero_vars))
            else:
                #new_solution = np.copy(solution)
                #new_solution[index] = 0
                stack.append((index - 1, solution, current_sum, nonzero_vars))

                new_solution = np.copy(solution)
                new_solution[index] = 1
                stack.append((index - 1, new_solution, current_sum + self.coefficients[index], nonzero_vars + 1))

                new_solution = np.copy(solution)
                new_solution[index] = -1
                stack.append((index - 1, new_solution, current_sum - self.coefficients[index], nonzero_vars + 1))

class MusserSumsetImpl(Solver):
    def __init__(self, coefficients):
        super().__init__(coefficients)
    
    def solve(self, goal, max_vars=None):
        # TODO
        pass