# this is the implementation of forwardChecking with backtracking
import rule
from read import printPuzzle

# this method receives a 2d-list state and outputs an assignment for all the cells


def forwardChecking(state):
    A, D = [], []
    U = rule.getUnassigned(state)
    forwardCheckingHelper(A, U, D)


def forwardCheckingHelper(A, U, D):
    current = assignAll(A, state)
    printPuzzle(current)
    if rule.solutionCheck(current):  # all unassigned cell have been assigned
        return A
