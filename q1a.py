#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file
from z3 import *
from itertools import combinations


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
    constraints_stability = []

    # In this problem, you have to express matching constraints, that ensure the result is a correct
    # matching, and stability constraints, which ensure the matching is stable.
    # TODO add the required constraints, separated in two sets.
    # TODO add the required constraints, separated in two sets.
    print('A', A)
    print('B', B)
    # TODO: Declare the variables
    v = [Int('v{}'.format(i)) for i in range(1, (n * 2) + 1)]
    print('v', v)
    # constraints_matching
    # Element from A must be paired with an element in the range [n+1, 2n]
    constraints_matching += [And([(v[i] > n) for i in range(0, n)])]
    constraints_matching += [And([(v[i] <= (n * 2)) for i in range(0, n)])]
    # Element from B must be paired with an element [1, n]
    constraints_matching += [And([(v[i] > 0) for i in range(n, n * 2)])]
    constraints_matching += [And([(v[i] <= n) for i in range(n, n * 2)])]
    # Loop through combinations and add constraints
    # tmp = []
    for i, j in combinations(v, 2):
        # tmp2 = []
        # Every element in the matching must appear exactly once
        if ((i in v[0:n]) and (j in v[0:n])) or ((i in v[n:(n * 2)]) and (j in v[n:(n * 2)])):
            constraints_matching += [And((i != j))]
        # Every element must match with their match
        # if (i in v[0:n]) and (j in v[n:(n * 2)]):
        #     num_i = int(str(i)[1])
        #     num_j = int(str(j)[1])
        #     tmp += [And([(i == num_j), (j == num_i)])]
    # constraints_matching += [Or(tmp)]
    for i in v[0:n]:
        tmp = []
        for j in v[n:(n * 2)]:
            num_i = int(str(i)[1])
            num_j = int(str(j)[1])
            tmp += [And([(i == num_j), (j == num_i)])]
        constraints_matching += [Or(tmp)]

    print('constraints_matching', constraints_matching)

    # TODO: constraints_stability
    # def prefers(i, j):
    #     """
    #     Returns True iff v prefers alt over curr and False otherwise.
    #     """
    #     num_i = int(str(i)[1])
    #     num_j = int(str(j)[1])
    #     index_i = num_i - 1
    #     index_i = num_j - 1
    #     return A[index_i].index(alt)

    # Loop through combinations and add constraints
    tmp = []
    for i, j in combinations(v, 2):
        # The match must be stable
        # The following cannot be true:
        # vi != j and
        # vi prefers j and
        # vj prefers i
        tmp2 = []
        if (i in v[0:n]) and (j in v[n:(n * 2)]):
            num_i = int(str(i)[1])
            num_j = int(str(j)[1])
            print(('{} == {}'.format(i, num_j)))
            # vi != j
            tmp2 += [(i == num_j)]
            # vi prefers j
            for k in range(n + 1, (n * 2) + 1):
                if k != num_j:
                    print(('{}.index({}) < {}'.format(i, num_j, k)))
                    tmp2 += [A[num_i - 1].index(num_j) < A[num_i - 1].index(k)]
            # print(prefers(i,j))
            # vj prefers i
            for k in range(1, n + 1):
                if k != num_i:
                    print(('{}.index({}) < {}'.format(j, num_i, k)))
                    tmp2 += [B[num_j - 1 - n].index(num_i) < B[num_j - 1 - n].index(k)]
            # print(('{} prefers {}'.format(j, num_i)))
            constraints_stability += [Not(And(tmp2))]
    # print(tmp)
    # constraints_stability += tmp

    print('constraints_stability', constraints_stability)

    # ==============================================================================================
    # DO NOT MODIFY.
    # This code adds the two sets of constraints to the solver, and calls the solver.
    s = Solver()
    for cstr in constraints_matching + constraints_stability:
        s.add(cstr)
    assert str(s.check()) == 'sat'
    model = s.model()
    # ==============================================================================================

    # TODO : Add code here to interpret the model and return the matching.

    return []


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
        print("Usage: python q1a.py INPUT_FILE\n\tHint: test_input contains two valid input files.")
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
