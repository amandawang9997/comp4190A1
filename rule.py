#Note:state is always a 2d list


#this method find all unassigned cells in the initial state and return a list containing coordinates(e.g (3,4))
def getUnassigned(state):
    result=[]
    for i in range(len(state)):
        for j in range(len(state[0])):
            if not isinstance(state[i][j],int):
                result.append((i, j))
    return result

##this method find all bulbs and return a list containing coordinates(e.g (3,4))
def getBulbs(state):
    result = []
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j]=='b':
                result.append((i, j))
    return result

#this method find all  numbered cells and return a list containing their coordinates(e.g (3,4))
def getNumbers(state):
    result = []
    for i in range(len(state)):
        for j in range(len(state[0])):
            if  isinstance(state[i][j],int):
                result.append((i, j))
    return result

#when searching, the number of bulbs around a numbered cell should be at most that number
#this method receives a state and returns boolean variable indicating the state is ok?
def numberConstrain(state):
    row,col=len(state),len(state[1])
    for (i,j) in getNumbers(state):
        count=0
        if i+1<=row-1 and  state[i+1][j]=='b':count+=1
        if i-1>=0 and  state[i-1][j]=='b':count+=1
        if j+1<=col-1 and state[i][j+1]=='b':count+=1
        if j-1>=0 and state[i][j-1]=='b':count+=1
        if count>state[i][j]:
            return False
    return True

#this method is used to check whether the number of bulbs around a numbered cell is exactly the same? should use this method
#when all empty cells have been assigned a value
def numberCheck(state):
    row,col=len(state),len(state[1])
    for (i,j) in getNumbers(state):
        count=0
        if(i+1<=row-1 and state[i+1][j]=='b'):count+=1
        if(i-1>=0 and  state[i-1][j]=='b'):count+=1
        if(j+1<=col-1 and state[i][j+1]=='b'):count+=1
        if(j-1>=0 and state[i][j-1]=='b'):count+=1
        if(count!=state[i][j]):
            return False
    return True

#this method returns a set containing coordinates which are lit(the bulbs' coordinates are also included)
def findLit(state):
    bulbs=getBulbs(state)
    result=[]
    if(len(bulbs)>0):
        for(i,j) in bulbs:  #for each bulb the first 2 while loops find cells which are lit horizontally by that bulb(i is fixed)
            k=0             #the last 2 find cells which are lit vertically(j is fixed) (till the light hits a number cell)
            while j+k<len(state[1]) and (not isinstance(state[i][j+k],int)):
                result.append((i,j+k))
                k+=1

            k=0
            while j-k>=0 and (not isinstance(state[i][j-k],int)):
                result.append((i,j-k))
                k+=1
            k=0
            while i+k<len(state) and (not isinstance(state[i+k][j],int)):
                result.append((i+k,j))
                k+=1
            k=0
            while i-k>=0 and (not isinstance(state[i-k][j],int)):
                result.append((i-k,j))
                k+=1
            result.append((i,j))
    return set(result)

#this is one of the constrains
#this method returns a list containing cells that are neither lit (note that we assume the bulbs' cells are lit) nor numbered
def goodCells(state):
    row,col=len(state),len(state[0])
    result=[]
    lit=findLit(state)                  #note that lit and numbers are both list
    numbers=getNumbers(state)
    for i in range(row):
        for j in range (col):
            if (i,j) not in lit and (i,j) not in numbers:
                result.append((i,j))
    return result

#this method checks whether a solution is valid(i.e. every cell is lit and the number condition is satisfied)
#only use this method when every empty cell has been  assigned a value(either '_' or 'b')
def solutionCheck(state):
    return len(goodCells(state))==0 and numberCheck(state)

#when #bulbs around the numbered cell is greater, we should exit the current loop and do backtracking
#use this method when the searching has not been done(there is still some empty cell)
#when searching, if we always choose the next cell from goodCells(), then we are guaranteed that the light
#from two bulbs will not overlap
#another constrain
def constraintsCheck(state):
    return numberConstrain(state)