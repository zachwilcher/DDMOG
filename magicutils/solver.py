
import numpy as np

class Solver:
    """Solves the subset sum problem where the integers to be summed are given 
    by plus or minus of each of the numbers in the vector 'coefficients'."""
    def __init__(self, coefficients):
        self.coefficients = coefficients
    
    def solve(self, goal, max_vars=None):
        """max_vars is the maximum number of non-zero variables in the solution."""
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

class SumsetSolverImpl(Solver):
    """Variation of David Musser's algorithm for solving the subset sum problem 
    as described on pg. 33 in their PhD thesis: Algorithms for Polynomial Factorization"""
    def __init__(self, coefficients):
        super().__init__(coefficients)
        self.generate_sumsets()


    def generate_sumsets(self):
        self.sumsets = []

        self.sumsets.append(set([0]))

        for i, coefficient in enumerate(self.coefficients):
            new_sumset = set()
            for s in self.sumsets[i]:
                new_sumset.add(s)
                new_sumset.add(s + coefficient)
                new_sumset.add(s - coefficient)
            self.sumsets.append(new_sumset)
    
    def solve(self, goal, max_vars=None):

        stack = []

        stack.append((len(self.coefficients) - 1, 0, np.zeros(len(self.coefficients), dtype=np.int64), 0))

        while len(stack) > 0:
            
            (index, current_sum, solution, nonzero_vars) = stack.pop()
            if (index == -1) or (nonzero_vars >= max_vars):
                if current_sum == goal:
                    yield solution
            elif self.coefficients[index] == 0:
                # Don't waste time determining possibilities with 0 coefficient
                stack.append((index - 1, current_sum, solution, nonzero_vars))
            else:
                if goal - (current_sum + self.coefficients[index]) in self.sumsets[index]:
                    new_solution = np.copy(solution)
                    new_solution[index] = 1
                    stack.append((index - 1, current_sum + self.coefficients[index], new_solution, nonzero_vars + 1))
                
                if goal - (current_sum - self.coefficients[index]) in self.sumsets[index]:
                    new_solution = np.copy(solution)
                    new_solution[index] = -1
                    stack.append((index - 1, current_sum - self.coefficients[index], new_solution, nonzero_vars + 1))
                
                if goal - (current_sum) in self.sumsets[index]:
                    stack.append((index - 1, current_sum, new_solution, nonzero_vars))
