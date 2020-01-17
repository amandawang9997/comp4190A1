import rule
from read import printPuzzle, read
from backtracking import assignAll


# the main loop so that it will always ask an input then solve the puzzle
def mainLoop():

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
        currentState = assignAll({(i, j): 'b'}, state)
        # since numLit must exclude the bulb itself
        # calculate how many cells have been lit if (i,j) has a bulb
        numLit = len(rule.findLit(currentState)) - len(rule.findLit(state))
        # calculate the number of cells which are affected because of the number constraint
        affectedList = []
        for (m, n), arr in affectedDict.items():
            if (i, j) in arr:  # if  (i,j) is adjacent to some numbered Cell (m, n)then add all the cells that are adjacent to (m,n) into the list
                affectedList.extend(arr)
        affectedList = set(affectedList)
        temp[(i, j)] = len(affectedList) - 1 + numLit
    return max(temp, key=temp.get)


# given a current state, find a dictionary such that {(i, j):[(x1,y1),(x2,y2),...],......} where (i, j) is numbered and (xi, yi)'s' are adjacent to it and unassigned
def getAffected(state):
    result = {}
    unassigned = rule.getUnassigned()
    row, col = len(state), len(state[0])
    for (i, j) in rule.getNumbers(state):
        result[(i, j)] = []
        if i + 1 <= row - 1 and state[i + 1][j] in unassigned:
            result[(i, j)].append((i + 1, j))
        if i - 1 >= 0 and state[i - 1][j] in unassigned:
            result[(i, j)].append((i - 1, j))
        if j + 1 <= col - 1 and state[i][j + 1] in unassigned:
            result[(i, j)].append((i, j + 1))
        if j - 1 >= 0 and state[i][j - 1] in unassigned:
            result[(i, j)].append((i, j - 1))
    return result


# state is the initial state immediately after reading from stdin
def mostConstrainingSearch(state):
    U = rule.getUnassigned(state)  # a list of all unassigned variables
    A = {}  # a dictionary that maps: unassigned coordinate-->None
    return mostConstrainingSearchHelper(A, U.copy(), state)


# this method receives assignments(A,dictionary), a list of unassigned coordinates(U), an initial state
# it returns a new assignment to solve the puzzle with initial state "state"
def mostConstrainingSearchHelper(A, U, state):
    current = assignAll(A, state)  # the current state
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
            temp = assignAll(B, state)
            if not rule.numberConstrain(temp):
                continue
            # recursive call with new assignments B
            result = mostConstrainingSearchHelper(B, U.copy(), state)
            if result is not None:                  # WE HAVE no solution in this case
                return result

    return None
