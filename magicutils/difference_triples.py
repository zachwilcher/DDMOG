
import numpy as np
from ortools.sat.python import cp_model

def change_base(n, b):
    """Get the string representation of n in base b"""
    digits = []
    while n > 0:
        digits.append(n % b)
        n = n // b
    s = "".join(map(str, reversed(digits)))
    return s

class Callback(cp_model.CpSolverSolutionCallback):
    def __init__(self, arr, index_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.arr = arr
        self.index_vars = index_vars
        self.solution_count = 0
        self.pretty_count = 0

    def on_solution_callback(self):
        self.solution_count += 1

        # build triples of indices
        triples = []

        ugly = False
        for i in range(0, len(self.arr), 3):
            triple = (
                self.value(self.index_vars[i]),
                self.value(self.index_vars[i + 1]),
                self.value(self.index_vars[i + 2]),
            )
            triples.append(triple)
            if ((self.arr[triple[0]] == 3) and (self.arr[triple[1]] != 12)) \
                or ((self.arr[triple[0]] != 1) and (self.arr[triple[1]] > 22)):
                ugly = True

        if not ugly:
            self.pretty_count += 1

            print(f"new solution: {self.pretty_count}")
            for triple in triples:
                base = 10

                a = change_base(self.arr[triple[0]], base)
                b = change_base(self.arr[triple[1]], base)
                c = change_base(self.arr[triple[2]], base)

                print(f"{a} + {b} = {c}")



def foo(arr, max_time=None):
    """Try to partition arr into difference triples."""
    if len(arr) % 3 != 0:
        # no.
        raise ValueError("Invalid array length")
    
    model = cp_model.CpModel()

    index_vars = [model.new_int_var(0, len(arr) - 1, f"index_var_{i}") for i in range(len(arr))]
    value_vars = [model.new_int_var(min(arr), max(arr), f"value_var_{i}") for i in range(len(arr))]
    for value_var, index_var in zip(value_vars, index_vars):
        model.add_element(index_var, arr, value_var)

    model.add_all_different(index_vars)


    for i in range(0, len(arr), 3):
        a = value_vars[i]
        b = value_vars[i + 1]
        c = value_vars[i + 2]

        model.add(a + b == c)

        # these constraints are temporary for testing
        model.add(a < arr[len(arr) // 3])
        #model.add_implication(a == 1, b == 30)
        model.add(c != arr[-2])
        #model.add_modulo_equality(0,a,2)

        # force a nice ordering
        model.add(index_vars[i] < index_vars[i + 1])
        if i > 0:
            model.add(index_vars[i - 3] < index_vars[i])
            


    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    if max_time is not None:
        solver.parameters.max_time_in_seconds = max_time
    callback = Callback(arr, index_vars)
    solver.solve(model, callback)
    return callback

x = 5
arr = None
if x % 2 == 1:
    arr = list([1]) + list(range(3, (6 * x + 1) + 1))
else:
    arr = list(range(2, (6 * x + 1) + 1))

callback_obj = foo(arr)
#print(callback_obj.solution_count)
