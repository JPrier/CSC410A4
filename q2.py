#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file
from z3 import *
from itertools import combinations

def solve(grid):
    """
    This function solves the Hidato puzzle with the initial configuration stored in grid.
    You should ouput a grid in the same format, but where all the '-' have been replaced by numbers.
    """
    # TODO : solve the Hidato puzzle using Z3. gird[i][j] is either "-", "*" or an integer.
    clauses = []

    # Set up variables
    v = []
    max_value = 1
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if not (value == "*"):
                if value == "-":
                    v += [(Int("t_%i_%i" % (i,j)), (i,j))]
                else:
                    v += [(Int("t_%i_%i" % (i,j)), (i,j))]
                    clauses += [v[-1][0] == value]
                    if value > max_value:
                        max_value = value

    # Set up clauses
    ## all variables are >= 1
    clauses += [And([And([value[0] >= 1, value[0] <= max_value]) for value in v])]
    ## no two variables are equivalent
    for pairs in combinations(v, 2):
        clauses += [pairs[0][0] != pairs[1][0]]
    ## Any pair of sequential variables need to be touching (including diagonals)
    for value in v:
        neighbours = []
        i, j = value[1][0], value[1][1]

        if i > 0:
            # i-1, j-1
            if j > 0 and grid[i-1][j-1] != "*":
                neighbours += [Or(neighbour(i-1, j-1, value[0]))]
            # i-1, j
            if grid[i-1][j] != "*":
                neighbours += [Or(neighbour(i-1, j, value[0]))]
            # i-1, j+1
            if j+1 < len(grid[i-1]) and grid[i-1][j+1] != "*":
                neighbours += [Or(neighbour(i-1, j+1, value[0]))]

        # i, j-1
        if j > 0  and grid[i][j-1] != "*":
            neighbours += [Or(neighbour(i, j-1, value[0]))]

        # i, j+1
        if j+1 < len(grid[i]) and grid[i][j+1] != "*":
            neighbours += [Or(neighbour(i, j+1, value[0]))]

        if i+1 < len(grid):
            # i+1, j-1
            if j > 0 and grid[i+1][j-1] != "*":
                neighbours += [Or(neighbour(i+1, j-1, value[0]))]
            # i+1, j
            if grid[i+1][j] != "*":
                neighbours += [Or(neighbour(i+1, j, value[0]))]
            # i+1, j+1
            if j+1 < len(grid[i+1]) and grid[i+1][j+1] != "*":
                neighbours += [Or(neighbour(i+1, j+1, value[0]))]

        clauses += [Or(neighbours)]  # TODO: make this exactly one

    # Solve
    s = Solver()

    for clause in clauses:
        s.add(clause)

    if str(s.check()) == 'sat':
        model = s.model()

        for value in v:
            #set grid[value[1]] to eval of value[0]
            i, j = value[1][0], value[1][1]
            grid[i][j] = model.evaluate(value[0])

        print("sat")
    else:
        print("unsat")

    return grid


def neighbour(i, j, value):
    return [Int("t_%i_%i" % (i,j)) - 1 == value,
            Int("t_%i_%i" % (i,j)) + 1 == value]


# ================================================================================
#  Do not modify below!
# ================================================================================
def check(raw_grid):
    """
    Check that the grid is well defined.
    """
    n = len(raw_grid)
    assert n > 1
    m = len(raw_grid[0])
    assert m > 1

    grid = []
    for i in range(n):
        grid.append([])
        assert len(raw_grid[i]) == m

        for elt in raw_grid[i]:
            if elt == '*':
                grid[i].append(elt)
            elif elt == '-':
                grid[i].append(elt)
            else:
                try:
                    grid[i].append(int(elt))
                except:
                    return None

    return grid

def print_solution(grid):
    for line in grid:
        if '-' not in line:
            print(" ".join([str(x) for x in line]))
        else:
            print("Solution incomplete!")
            return


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python q2.py INPUT_FILE")
        print("\tHint: test_input contains valid input files for Hidato.")
        exit(1)

    raw_grid = []
    with open(sys.argv[1], 'r') as input_grid:
        for line in input_grid.readlines():
            raw_grid.append(line.strip().split())


        grid = check(raw_grid)
        if grid:
            # Call the encoding function on the input.
            print_solution(solve(grid))
            exit(0)
        else:
            print("The input file does not define a valid problem.")
            exit(1)
