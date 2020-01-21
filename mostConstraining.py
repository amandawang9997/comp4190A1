import rule
from read import printPuzzle, read
from backtracking1 import assignAll
import copy
import random

# the main loop so that it will always ask an input then solve the puzzle


def mainLoopmC():

    while True:
        state = None

        state = read()['puzzle']
        assignment = mostConstrainingSearch(state)
        temp = assignAll(assignment, state)  # the final solution as a 2d list
        print('the answer is:')
        printPuzzle(temp)


#  this method receives the MOST RECENT state and a set of unassigned  variables, find the most constraining cell's coordinate from all the cells which has
#  not been assigned a char
def mostConstrainingCell(state, currentU):
    # temp is a dictionary (i,j)->numbers of cells which get affected by number constraint and non-same-row-or-column rule by(i,j)
    temp = {}
    numberedCells = set(rule.getNumbers(state))  # get all the numbered cells
    affectedDict = getAffected(state)
    for (i, j) in currentU:     # for each (i,j) which has not been assigned a value
        # currentState = assign(state, (i, j), 'b')
        # since numLit must exclude the bulb itself
        # calculate how many cells have been lit if (i,j) has a bulb

        # calculate the number of cells which are affected because of the number constraint
        # numLit = numlitCells(state, (i, j))
        numLit = 0
        affectedList = []
        for (m, n), arr in affectedDict.items():
            if (i, j) in arr:  # if  (i,j) is adjacent to some numbered Cell (m, n)then add all the cells that are adjacent to (m,n) into the list
                affectedList.extend(arr)
        affectedList = set(affectedList)
        temp[(i, j)] = len(affectedList) - 1 + numLit

        # randomly choose a kay in case of tie
        mv = max(temp.values())
        result = random.choice([k for (k, v) in temp.items() if v == mv])
    return result
    # return max(temp, key=temp.get)


# given a current state, find a dictionary such that {(i, j):[(x1,y1),(x2,y2),...],......} where (i, j) is numbered and (xi, yi)'s' are adjacent to it and unassigned
def getAffected(state):
    result = {(i, j): [] for (i, j) in rule.getNumbers(state)}
    unassigned = rule.getUnassigned(state)
    row, col = len(state), len(state[0])
    for (i, j) in rule.getNumbers(state):
        if i + 1 <= row - 1 and (i + 1, j) in unassigned:
            result[(i, j)].append((i + 1, j))
        if i - 1 >= 0 and (i - 1, j) in unassigned:
            result[(i, j)].append((i - 1, j))
        if j + 1 <= col - 1 and (i, j + 1) in unassigned:
            result[(i, j)].append((i, j + 1))
        if j - 1 >= 0 and (i, j - 1) in unassigned:
            result[(i, j)].append((i, j - 1))
    return result


def numlitCells(state, coord):
    result = []
    (i, j) = coord
    k = 0
    while j + k < len(state[1]) and (not isinstance(state[i][j + k], int)):
        result.append((i, j + k))
        k += 1

    k = 0
    while j - k >= 0 and (not isinstance(state[i][j - k], int)):
        result.append((i, j - k))
        k += 1
    k = 0
    while i + k < len(state) and (not isinstance(state[i + k][j], int)):
        result.append((i + k, j))
        k += 1
    k = 0
    while i - k >= 0 and (not isinstance(state[i - k][j], int)):
        result.append((i - k, j))
        k += 1
    return len(set(result)) - 1


# state is the initial state immediately after reading from stdin
def mostConstrainingSearch(state):
    U = rule.getUnassigned(state)  # a list of all unassigned variables
    A = {}  # a dictionary that maps: unassigned coordinate-->None
    return mostConstrainingSearchHelper(A, U.copy(), state)


def assign(state, coord, opt):
    state1 = copy.deepcopy(state)
    state1[coord[0]][coord[1]] = opt
    return state1


def assignDict(dict, state):
    result = copy.deepcopy(state)
    for (i, j), option in dict.items():
        result[i][j] = option
    return result


# this method receives assignments(A,dictionary), a list of unassigned coordinates(U), an initial state
# it returns a new assignment to solve the puzzle with initial state "state"
def mostConstrainingSearchHelper(A, U, state):
    current = assignDict(A, state)  # the current state
    printPuzzle(current)
    if rule.solutionCheck(current):  # all unassigned cell have been assigned
        return A  # and the number constraint is satisfied
    elif len(U) > 0:

        # get the most constraining coordinate
        (i, j) = mostConstrainingCell(current, U)
        U.remove((i, j))
        for option in ['b', '_']:  # one coordinate has 2 possible assignment
            B = A.copy()
            B[(i, j)] = option
            if ((i, j) not in rule.goodCells(current)) and option == 'b':
                continue
            temp = assignDict(B, state)
            if not rule.numberConstrain(temp):
                continue
            # recursive call with new assignments B
            result = mostConstrainingSearchHelper(B, U.copy(), state)
            if result is not None:                  # WE HAVE no solution in this case
                return result

    return None
