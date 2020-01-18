
import rule
import mostConstraining as mc


# this method takes an original state and returns a dictionary whose keys are all the unassigned
# coordinates and values are number of constraints each coordinate has

def getConstrains(stateOriginal):
    unassigned = rule.getUnassigned(stateOriginal)
    result = {(i, j): 0 for (i, j) in unassigned}
    for (i, j) in rule.getUnassigned(stateOriginal):

        # sameRowCol is num of strains caused by 2 coordinates being in the same row or col
        sameRowCol = mc.numlitCells(stateOriginal, (i, j))
        neighborsToNumber = getNumAffected((i, j), stateOriginal)
        result[(i, j)] = sameRowCol + neighborsToNumber
    return {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}


# given a coordinate (m,n) and a state, if (m,n) is adjacent to a numbered cell,
# then all the unassigned cells adjacent to that numbered cell will be add to a set
# this method returns the length of set


def getNumAffected(coord, stateOriginal):
    (m, n) = coord
    result = []

    unassigned = rule.getUnassigned(stateOriginal)
    row, col = len(stateOriginal), len(stateOriginal[0])
    for (i, j) in rule.getNumbers(stateOriginal):
        if isAdjacent(coord, (i, j), stateOriginal):

            if i + 1 <= row - 1 and (i + 1, j) in unassigned:
                result.append((i + 1, j))
            if i - 1 >= 0 and (i - 1, j) in unassigned:
                result.append((i - 1, j))
            if j + 1 <= col - 1 and (i, j + 1) in unassigned:
                result.append((i, j + 1))
            if j - 1 >= 0 and (i, j - 1) in unassigned:
                result.append((i, j - 1))
            result.remove(coord)

    return len(set(result))

# detects 2 coords are adjacent


def isAdjacent(coord1, coord2, state):
    (i, j) = coord1
    (m, n) = coord2
    row = len(state)
    col = len(state[0])
    if j is n:
        if i + 1 <= row - 1 and i + 1 is m:
            return True
        if i - 1 >= 0 and i - 1 is m:
            return True
    if i is m:
        if j + 1 <= col - 1 and j + 1 is n:
            return True
        if j - 1 >= 0 and j - 1 is n:
            return True
    return False
