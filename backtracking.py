import rule
def backtracking(state): #state is the initial state immediately after read from stdin
    U=rule.getUnassigned(state) #a list of all unassigned variables
    A = {} #a dictionary that maps: unassigned coordinate-->None
    return backtrackingHelper(A,U,state)




#this method receives assignments(A,dictionary), a list of unassigned coordinates(U), an initial state
#it returns a new assignment to solve the puzzle with initial state "state"
def backtrackingHelper(A,U,state):
    current = assignAll(A, state)
    if len(A)==len(state)*len(state[0])-rule.getNumbers(state) and rule.solutionCheck(current):#all unassigned cell have been assigned
        return A                                                                             #and the number constraint is satisfied
    (i,j)=U.pop(0)
    for option in ['_','b']:    #one coordinate has 2 possible assignment
        if option=='b' and ((i,j) not in rule.goodCells(current)):
            break
        B=A.copy()
        B[(i,j)]=option         #add one more assignment to list A
        temp=assignAll(B,state) #apply assignments to original state
        if option=='b' and not rule.numberConstrain(temp):
            break
        result=backtrackingHelper(B,U.copy(),state) #recursive call with new assignments B
        if result is not None:                  # WE HAVE not solution in this case
            return result
    return None







#this method receives an initial state and apply assignment A to it then return its copy
def assignAll(A,state):
    result=state.clone()
    for (i,j),option in A.items():
        result[i][j]=option
    return result


#



