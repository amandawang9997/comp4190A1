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

# this method receives a 2d list and returns {(c_i, c_j)} [c_i is a coordinate] where c_i affects c_j because of the number constraints


def getArcsNum(state):
    row, col = len(state), len(state[0])
    result = []
    unAssigned = rule.getUnassigned()
    for (i, j) in rule.getNumbers(state):
        if i + 1 <= row - 1 and (i + 1, j) in unAssigned:
            result.append((i + 1, j))
        if i - 1 >= 0 and (i - 1, j) in unAssigned:
            result.append((i - 1, j))
        if j + 1 <= col - 1 and (i, j + 1) in unAssigned:
            result.append((i, j + 1))
        if j - 1 >= 0 and (i, j - 1) in unAssigned:
            result.append((i, j - 1))
    temp = [(x, y) for x in result for y in result if x is not y]
    return set(temp)

# this method receives a 2d list and returns {(c_i,c_j)} where c_i affects c_j because they are on the same row or col


def getArcsRowCol(state):
    result = []
    for (i, j) in rule.getUnassigned():
        state1 = state.copy()
        # in order the use the findLit method, we have to assign b to (i,j) in the initial state
        state1[i][j] = 'b'
        result.append([((i, j), (m, n)) for (m, n) in rule.findLit(state1)])
    return set(result)

#   this method receives a state and calculate a possible assignment by elimating impossible values in the domain for each variable


def constraintPropagation(state):
    # initialize the domain with all possible values. Agian the the domain is a dictionary
    domain = {(i, j): ['b', '_'] for (i, j) in rule.getUnassigned()}
    # we first add all arcs, Q is a list of all arcs(directed)
    Q = []
    Q.extend(getArcsNum(state))
    Q.extend(getArcsRowCol(state))
    Q = list(set(Q))
    #  iterate until there is no arc left
    while len(Q) > 0:
        ((i, j), (u, v)) = Q.pop(0)
        if removeInconsistency((i, j), (u, v), domain):
            for (m, n) in rule.getUnassigned(state):
                #  new neighbors of  (i, j) in the set of arcs
                newNeighbors = {(x, y)
                                for (x, y) in Q if ((x, y), (i, j)) in Q}
                if (m, n) is not (u, v) and (m, n) in newNeighbors and ((m, n), (i, j)) not in Q:
                    Q.append(((m, n), (i, j)))
    return domain


#   this method receives 2 tuples(coordinate) and removes the impossible value in the domain of tup1 because of the inconsistency caused by the arc between tup1,2
def removeInconsistency(tup1, tup2, domain, state):
    for option1 in domain[tup1]:
        # have we found a value (option 2) such that for any option 1 in domain1, there exists a value(option 2) in domain2 such that they are consistent
        exist = False
        for option2 in domain[tup2]:
            if rule.numberConstrain(assignAll({tup1: domain[tup1], tup2: domain[tup2]}, state)):
                if len(domain[tup2]) > 1:
                    exist = True
                    break
                if option1 == 'b' and option2 == 'b' and tup2 not in rule.findLit(assignAll({tup1: 'b'}, state)):
                    exist = True
                    break
                if option1 == 'b' and option2 == '_' or option1 == '_' and option2 == 'b':
                    exist = True
                    break
        if not exist:
            domain[tup1].pop(option1)
            return True
    return False


def findConflicts(state):
    return rule.findLit()
