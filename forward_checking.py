#  this is the implementation of forwardChecking with backtracking

import rule
from read import printPuzzle
from backtracking import assignAll

# this method receives a 2d-list state and outputs an assignment for all the cells


def forwardChecking(state):
    A = []
    # D is a list of mappings: (i,j)->[possible values for (i, j)]
    D = {(i, j): ['b', '_'] for (i, j) in rule.getUnassigned()}
    U = rule.getUnassigned(state)
    return forwardCheckingHelper(A, U, D)


def forwardCheckingHelper(A, U, D, state):
    current = assignAll(A, state)
    printPuzzle(current)
    if rule.solutionCheck(current):  # check if current is a solution
        return A
    (i, j) = A.pop()
    for option in D[(i, j)]:
        if option == 'b' and (i, j) not in rule.goodCells():  # the first constraint
            continue
        B = A.copy()  # make a copy of A, then append a new assignment
        B[(i, j)] = option
        # create a new state with new assignments B
        new_state = assignAll(B, state)
        if not rule.numberConstrain(assignAll(B, state)):    # the second constraint
            continue
        D_copy = D  # save the original D
        conflicts = findConflicts(new_state)
        commonCells = set(U).intersection(set(conflicts))
        for (m, n) in commonCells:  # remove 'b' if we have conflicts
            D_copy[(m, n)].remove('b')
        # if for any variable(coordinates), there exists at least one value('b'or '_') for that, then:
        if all(len(D_copy[(i, j)]) > 0 for (i, j) in commonCells):
            # recursive call with new assignments&unassigned variables and D
            result = forwardCheckingHelper(B, U.copy(), D_copy)
            if result is not None:
                return result
    return None

# this method receives a coordinate and a current state(2d-list) and returns all the cells which are inconsistent with coord's existence


def findConflicts(state):
    return rule.findLit()
