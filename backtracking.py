
import rule
from read import printPuzzle, read
import random

# the main loop so that it will always ask an input then solve the puzzle


def mainLoop():

    while True:
        state = None

        state = read()['puzzle']
        assignment, num = backtracking(state)
        temp = assignAll(assignment, state)  # the final solution as a 2d list
        print('the answer is:')
        printPuzzle(temp)
        print('numVisited=')
        print(num)


def backtracking(state):  # state is the initial state immediately after reading from stdin
    U = rule.getUnassigned(state)  # a list of all unassigned variables
    A = {}  # a dictionary that maps: unassigned coordinate-->None
    return countHelper(A, U.copy(), state)


# this method receives assignments(A,dictionary), a list of unassigned coordinates(U), an initial state
# it returns a new assignment to solve the puzzle with initial state "state"
def countHelper(A, U, state):
    count = 0

    def backtrackingHelper(A, U, state):
        nonlocal count
        count += 1
        current = assignAll(A, state)
        printPuzzle(current)
        if rule.solutionCheck(current):  # all unassigned cell have been assigned
            return A  # and the number constraint is satisfied
        elif len(U) > 0:
            (i, j) = U.pop(random.randint(0, len(U) - 1))
            for option in ['b', '_']:  # one coordinate has 2 possible assignment
                B = A.copy()
                B[(i, j)] = option
                if ((i, j) not in rule.goodCells(current)) and option == 'b':
                    continue
                temp = assignAll(B, state)
                if not rule.numberConstrain(temp):
                    continue
                # recursive call with new assignments B
                result = backtrackingHelper(B, U.copy(), state)
                if result is not None:                  # WE HAVE no solution in this case
                    return result

        return None
    return backtrackingHelper(A, U, state), count


# this method receives an initial state and apply assignment A to it then return its copy
def assignAll(A, state):
    result = state.copy()
    for (i, j), option in A.items():
        result[i][j] = option
    return result
