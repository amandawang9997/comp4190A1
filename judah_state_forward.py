def parse_puzzle(puzzle):
    A = {}
    U = {}
    lc = {}
    wc = {}
    Nodes= 0
    W = len(puzzle[0])
    H = len(puzzle)
    Solved = False
    Max_Depth = False
    None_empty = True
    
    #If wall, add to A
    for i in range(H):
        for j in range(W):
            if puzzle[i][j] == 0: A[(i,j)] = 0
            if puzzle[i][j] == 1: A[(i,j)] = 1
            if puzzle[i][j] == 2: A[(i,j)] = 2
            if puzzle[i][j] == 3: A[(i,j)] = 3
            if puzzle[i][j] == 4: A[(i,j)] = 4
        
    #If wall, add constraints to wc
    for wall in A:
        if A[wall] == 0:
            wc[wall] = {}
            wc[wall]['Num'] = 0
            wc[wall]['Neighbors'] = {(wall[0]-1,wall[1]):None,
                                    (wall[0]+1,wall[1]):None,
                                    (wall[0],wall[1]-1):None,
                                    (wall[0],wall[1]+1):None}
            
            wc[wall]['Neighbors'] ={ x : k for x,k in wc[wall]['Neighbors'].items() if not (x[0]<0 or x[1]<0 or x[0] >= W or x[1]>= H or x in A)}
            
        if A[wall] == 1:
            wc[wall] = {}
            wc[wall]['Num'] = 1
            wc[wall]['Neighbors'] = {(wall[0]-1,wall[1]):None,
                                (wall[0]+1,wall[1]):None,
                                (wall[0],wall[1]-1):None,
                                (wall[0],wall[1]+1):None}
            
            wc[wall]['Neighbors'] ={  x : k for x,k in wc[wall]['Neighbors'].items() if not (x[0]<0 or x[1]<0 or x[0] >= W or x[1]>= H or x in A)}
            
        if A[wall] == 2:
            wc[wall] = {}
            wc[wall]['Num'] = 2
            wc[wall]['Neighbors'] = {(wall[0]-1,wall[1]):None,
                                    (wall[0]+1,wall[1]):None,
                                    (wall[0],wall[1]-1):None,
                                    (wall[0],wall[1]+1):None}
            
            wc[wall]['Neighbors'] ={  x : k for x,k in wc[wall]['Neighbors'].items() if not (x[0]<0 or x[1]<0 or x[0] >= W or x[1]>= H or x in A)}
            
        if A[wall] == 3:
            wc[wall] = {}
            wc[wall]['Num'] = 3
            wc[wall]['Neighbors'] = {(wall[0]-1,wall[1]):None,
                                    (wall[0]+1,wall[1]):None,
                                    (wall[0],wall[1]-1):None,
                                    (wall[0],wall[1]+1):None}
            
            wc[wall]['Neighbors'] ={  x : k for x,k in wc[wall]['Neighbors'].items() if not (x[0]<0 or x[1]<0 or x[0] >= W or x[1]>= H or x in A)}
            
        if A[wall] == 4:
            wc[wall] = {}
            wc[wall]['Num'] = 4
            wc[wall]['Neighbors'] = {(wall[0]-1,wall[1]):None,
                                    (wall[0]+1,wall[1]):None,
                                    (wall[0],wall[1]-1):None,
                                    (wall[0],wall[1]+1):None}
            
            wc[wall]['Neighbors'] ={  x : k for x,k in wc[wall]['Neighbors'].items() if not (x[0]<0 or x[1]<0 or x[0] >= W or x[1]>= H or x in A)}
                    
    
            
    #If not wall, add to U
    for i in range(H):
        for j in range(W):
            if (i,j) not in A:
                U[(i,j)] = ['_']
                if wall_constraint_check(wc,(i,j),'b'):
                    U[(i,j)].insert(0,'b')
            j = j + 1
        i = i + 1
    
    #if empty space add constraints to light constraints
    for x in U:
        lc[x] = {}
        lc[x]['Value'] = None
        lc[x]['Connected'] = []
        
        i = 1
        while True:
            if (x[0]-i,x[1]) in U:
                lc[x]['Connected'].append((x[0]-i,x[1]))
                i = i + 1
            else:
                break
                
        i = 1
        while True:
            if (x[0]+i,x[1]) in U:
                lc[x]['Connected'].append((x[0]+i,x[1]))
                i = i + 1
            else:
                break
                
        i = 1
        while True:
            if (x[0],x[1]-i) in U:
                lc[x]['Connected'].append((x[0],x[1]-i))
                i  = i + 1
            else:
                break
                
        i = 1
        while True:
            if (x[0],x[1]+i) in U:
                lc[x]['Connected'].append((x[0],x[1]+i))
                i = i + 1
            else:
                break
        

    
    state = {'A':A,
            'U':U,
            'LC':lc,
            'WC':wc,
            'Nodes': Nodes,
            'W':W,
            'H':H,
            'Solved': Solved,
            'Max_depth':Max_Depth,
            'None_empty':None_empty}
       
    return state

def unparse_puzzle(state):
    puzzle = []
    for i in range(state['W']):
        row = []
        for j in range(state['H']):
            row.append(state['A'][(i,j)])
        puzzle.append(row)
    return puzzle



# Checks if a change is valid with the light constraints
# lc is the dictionary of current light constraints
# key is the cooridinates of the var you are trying to change
# lit is true if you are adding a bulb and false if not
def light_constraint_check(lc,key,value):
    ret = True
    if(value == '_'):
        return True
    else:
        for x in lc[key]['Connected']:
            if lc[x]['Value'] == 'b':
                ret = False
                break
    return ret

#simply updates the light_constraints with a change
# lc is the dictionary of current light constraints
# key is the cooridinates of the var you are trying to change
# lit is true if you are adding a bulb and false if not
def light_constraint_update(lc,key,value):
    lc[key]['Value'] = value

#checks if the light constraints have been satysfied
def solved_light(lc):
    for key in lc:
        if(lc[key]['Value'] == None):
            return False
        if(lc[key]['Value'] == '_'):
            connected_lit = False
            for connected in lc[key]['Connected']:
                if lc[connected]['Value'] == 'b':
                    connected_lit = True
            if not connected_lit:
                return False
    return True


#Checks if the suggested change is valid under the wall constraints
def wall_constraint_check(wc,key,value):
    if(value == '_'):
        return True
    for wall in wc:
        if key in wc[wall]['Neighbors']:
            num_lit = 1
            for x in wc[wall]['Neighbors']:
                if wc[wall]['Neighbors'][x] == 'b':
                    num_lit = num_lit + 1
            if num_lit > wc[wall]['Num']:
                return False
    return True



#Updates wall constraint to new value
def wall_constraint_update(wc,key,value):
    for wall in wc:
        if key in wc[wall]['Neighbors']:
            wc[wall]['Neighbors'][key] = value


# checks if the wall constraints have been satysfied
def solved_wall(wc):
    for wall in wc:
        num_lit = 0
        for x in wc[wall]['Neighbors']:
            if wc[wall]['Neighbors'][x] == 'b':
                num_lit = num_lit + 1
        if num_lit != wc[wall]['Num']:
            return False
            
    return True


def check_solved(state):
    if  not check_max_depth(state):
        return False
    else: 
        return solved_light(state['LC']) and solved_wall(state['WC'])

def check_max_depth(state):
    return len(state['A']) == state['W']*state['H']

def check_constraints(state,key,value):
    if value == '_':
        return True
    else:
        return light_constraint_check(state['LC'],key,value) and wall_constraint_check(state['WC'],key,value)

def u_update(state,key,value):
    if value == 'b':
        for connected in state['LC'][key]['Connected']:
            if connected in state['U']:
                if 'b' in state['U'][connected]:
                    state['U'][connected].remove('b')
        
        for wall in state['WC']:
            if key in state['WC'][wall]['Neighbors']:
                
                num_lit = 0
                for neighbor in state['WC'][wall]['Neighbors']:
                    if state['WC'][wall]['Neighbors'][neighbor] == 'b':
                        num_lit = num_lit + 1
                        
                if state['WC'][wall]['Num'] == num_lit:
                    for neighbor in state['WC'][wall]['Neighbors']:
                        if neighbor in state['U']:
                            if 'b' in state['U'][neighbor]:
                                state['U'][neighbor].remove('b')
                        
                        
def update_state(state,key,value):
    state['A'][key] = value
    light_constraint_update(state['LC'],key,value)
    wall_constraint_update(state['WC'],key,value)
    u_update(state,key,value)
        
    
    state['Solved'] = check_solved(state)
    state['Max_depth'] = check_max_depth(state)
    # False is never droped so this will alway be true
    state['None_empty'] = True
    
    #update possible values for adjacent nodes
