#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file
from z3 import *
from itertools import combinations

def abs(x):
    return If(x >= 0,x,-x)
def check_preference (var, L):
    for match in L:
        if var == match:
            return var + L.index(match)
    return var + len(L)

def solve(A, B):
    """
    This function should solve the stable marriages problem, with inputs A and B:
    - A lists the preferences of elements from 1 to len(A).
    - B lists the preferences of elements from len(A) + 1 to 2 * len(A).
      This means that B[i] is the preferences of element (i + 1 + len(A))!
    Returns a list of pairs of integers, such that the lists represents a stable
    matching for A, B. The first element of each pair is an element of [1, len(A)]
    and the second element of each pair is an element of [len(A) + 1, 2 * len(A)]
    """
    n = len(A)
    constraints_matching = []
    minimization_objectives = []
    # In this problem, you have to express matching constraints, that ensure the result is a correct
    # matching. You can reuse the constraints of q1a, but do not reuse the constraints_stability!
    # Instead, create a list of minimization objectives that have to be minimized (the list can
    # have a single element).
    # REMARK: to add a maximixation objective, just add its opposite:
    # Maximize Q <-> Minimize - Q
    # TODO add the matching constraints and the optimization objectives.
    v = [Int('v{}'.format(i)) for i in range(1, (n * 2  ) + 1)]

    constraints_matching += [And([(v[i] > n) for i in range(0, n)])]
    constraints_matching += [And([(v[i] <= ((n * 2) + (n - 1) * (n * 2 * n * 2))) for i in range(0, n)])]
    constraints_matching += [And([(v[i] > 0) for i in range(n, n * 2)])]
    constraints_matching += [And([(v[i] <= (n + (n - 1) * (n * 2 * n * 2))) for i in range(n, n * 2)])]
    for i, j in combinations(v, 2):
        if ((i in v[0:n]) and (j in v[0:n])) or ((i in v[n:(n * 2)]) and (j in v[n:(n * 2)])):
            constraints_matching += [And((i != j))]

    for i in v[0:n]:
        tmp = []
        a = A[v.index(i)]
        for j in v[n:(n * 2)]:
            b = B[v.index(j) - n]
            num_i = int(str(i)[1])
            num_i += (n * 2 * n * 2) * (b.index(num_i))
            num_j = int(str(j)[1])
            num_j += (n * 2 * n * 2) * (a.index(num_j))
            tmp += [And([(i == num_j), (j == num_i)])]
        constraints_matching += [Or(tmp)]

    s = 0
    for k in v:
        s += k
    minimization_objectives += [s]

    # ==============================================================================================
    # DO NOT MODIFY.
    # This code adds the matching constraints to the solver, and the minimization objectives.
    s = Optimize()
    for cstr in constraints_matching:
        s.add(cstr)
    for opt in minimization_objectives:
        s.minimize(opt)
    assert str(s.check()) == 'sat'
    model = s.model()
    # ==============================================================================================

    # TODO : Add code here to interpret the model and return the matching.
    result = []
    model_list = sorted([(d, model[d]) for d in model], key=lambda x: str(x[0]))
    for m in model_list:
        value = int(str(m[1]))
        while value > n * 2 * n * 2:
            value -= n * 2 * n * 2
        result.append((model_list.index(m) + 1, value))
    return result[0:n]

# ================================================================================
#  Do not modify below!
# ================================================================================
def well_ranked(pref, imin, imax):
    for pid in pref:
        if pid > imax or pid < imin:
            return False
    return True


def well_formed_problem(prefs):
    """
    Check that everyone has ranked all the other persons.
    """
    n2 = len(prefs)
    A, B = prefs[: int(n2 / 2)], prefs[int(n2 / 2):]
    n = len(A)
    assert len(B) == n
    for pref in A:
        assert well_ranked(pref, n, 2 * n)
    for pref in B:
        assert well_ranked(pref, 1, n)
    return True


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python q1b.py INPUT_FILE\n\tHint: test_input contains two valid input files.")
        exit(1)

    prefs = []
    with open(sys.argv[1], 'r') as input_grid:
        for line in input_grid.readlines():
            prefs.append([int(x) for x in   line.strip().split()])

        if well_formed_problem(prefs):
            n2 = len(prefs)
            A, B = prefs[: int(n2 / 2)], prefs[int(n2 / 2):]
            print(solve(A, B))
            exit(0)
        else:
            print("The input file does not define a valid problem.")
            exit(1)
