import copy


def parse_puzzle(puzzle):
    A = {}
    U = {}
    lc = {}
    wc = {}
    Nodes = 0
    W = len(puzzle[0])
    H = len(puzzle)
    Solved = False
    Max_Depth = False
    None_empty = True

    # If wall, add to A
    for i in range(H):
        for j in range(W):
            if puzzle[i][j] == 0:
                A[(i, j)] = 0
            if puzzle[i][j] == 1:
                A[(i, j)] = 1
            if puzzle[i][j] == 2:
                A[(i, j)] = 2
            if puzzle[i][j] == 3:
                A[(i, j)] = 3
            if puzzle[i][j] == 4:
                A[(i, j)] = 4

    # If wall, add constraints to wc
    for wall in A:
        if A[wall] == 0:
            wc[wall] = {}
            wc[wall]['Num'] = 0
            wc[wall]['Neighbors'] = {(wall[0] - 1, wall[1]): None,
                                     (wall[0] + 1, wall[1]): None,
                                     (wall[0], wall[1] - 1): None,
                                     (wall[0], wall[1] + 1): None}

            wc[wall]['Neighbors'] = {x: k for x, k in wc[wall]['Neighbors'].items(
            ) if not (x[0] < 0 or x[1] < 0 or x[0] >= W or x[1] >= H or x in A)}

        if A[wall] == 1:
            wc[wall] = {}
            wc[wall]['Num'] = 1
            wc[wall]['Neighbors'] = {(wall[0] - 1, wall[1]): None,
                                     (wall[0] + 1, wall[1]): None,
                                     (wall[0], wall[1] - 1): None,
                                     (wall[0], wall[1] + 1): None}

            wc[wall]['Neighbors'] = {x: k for x, k in wc[wall]['Neighbors'].items(
            ) if not (x[0] < 0 or x[1] < 0 or x[0] >= W or x[1] >= H or x in A)}

        if A[wall] == 2:
            wc[wall] = {}
            wc[wall]['Num'] = 2
            wc[wall]['Neighbors'] = {(wall[0] - 1, wall[1]): None,
                                     (wall[0] + 1, wall[1]): None,
                                     (wall[0], wall[1] - 1): None,
                                     (wall[0], wall[1] + 1): None}

            wc[wall]['Neighbors'] = {x: k for x, k in wc[wall]['Neighbors'].items(
            ) if not (x[0] < 0 or x[1] < 0 or x[0] >= W or x[1] >= H or x in A)}

        if A[wall] == 3:
            wc[wall] = {}
            wc[wall]['Num'] = 3
            wc[wall]['Neighbors'] = {(wall[0] - 1, wall[1]): None,
                                     (wall[0] + 1, wall[1]): None,
                                     (wall[0], wall[1] - 1): None,
                                     (wall[0], wall[1] + 1): None}

            wc[wall]['Neighbors'] = {x: k for x, k in wc[wall]['Neighbors'].items(
            ) if not (x[0] < 0 or x[1] < 0 or x[0] >= W or x[1] >= H or x in A)}

        if A[wall] == 4:
            wc[wall] = {}
            wc[wall]['Num'] = 4
            wc[wall]['Neighbors'] = {(wall[0] - 1, wall[1]): None,
                                     (wall[0] + 1, wall[1]): None,
                                     (wall[0], wall[1] - 1): None,
                                     (wall[0], wall[1] + 1): None}

            wc[wall]['Neighbors'] = {x: k for x, k in wc[wall]['Neighbors'].items(
            ) if not (x[0] < 0 or x[1] < 0 or x[0] >= W or x[1] >= H or x in A)}

    # If not wall, add to U
    for i in range(H):
        for j in range(W):
            if (i, j) not in A:
                U[(i, j)] = ['_']
                if wall_constraint_check(wc, (i, j), 'b'):
                    U[(i, j)].insert(0, 'b')
            j = j + 1
        i = i + 1

    # if empty space add constraints to light constraints
    for x in U:
        lc[x] = {}
        lc[x]['Value'] = None
        lc[x]['Connected'] = []

        i = 1
        while True:
            if (x[0] - i, x[1]) in U:
                lc[x]['Connected'].append((x[0] - i, x[1]))
                i = i + 1
            else:
                break

        i = 1
        while True:
            if (x[0] + i, x[1]) in U:
                lc[x]['Connected'].append((x[0] + i, x[1]))
                i = i + 1
            else:
                break

        i = 1
        while True:
            if (x[0], x[1] - i) in U:
                lc[x]['Connected'].append((x[0], x[1] - i))
                i = i + 1
            else:
                break

        i = 1
        while True:
            if (x[0], x[1] + i) in U:
                lc[x]['Connected'].append((x[0], x[1] + i))
                i = i + 1
            else:
                break

    state = {'A': A,
             'U': U,
             'LC': lc,
             'WC': wc,
             'Nodes': Nodes,
             'W': W,
             'H': H,
             'Solved': Solved,
             'Max_depth': Max_Depth,
             'None_empty': None_empty}

    return state


def unparse_puzzle(state):
    puzzle = []
    for i in range(state['W']):
        row = []
        for j in range(state['H']):
            row.append(state['A'][(i, j)])
        puzzle.append(row)
    return puzzle


# Checks if a change is valid with the light constraints
# lc is the dictionary of current light constraints
# key is the cooridinates of the var you are trying to change
# lit is true if you are adding a bulb and false if not
def light_constraint_check(lc, key, value):
    # Violates constraint if there are only '_'s in key's connected nodes
    if(value == '_'):
        ret = False
        for x in lc[key]['Connected']:
            if lc[x]['Value'] == 'b' or lc[x]['Value'] == None:
                return True
        return ret
    # Violates constraint if the 'b' I am placing already has a 'b' in it connected nodes
    if(value == 'b'):
        for x in lc[key]['Connected']:
            if lc[x]['Value'] == 'b':
                return False
    return True

# simply updates the light_constraints with a change
# lc is the dictionary of current light constraints
# key is the cooridinates of the var you are trying to change
# lit is true if you are adding a bulb and false if not


def light_constraint_update(lc, key, value):
    lc[key]['Value'] = value

# Checks if the suggested change is valid under the wall constraints


def wall_constraint_check(wc, key, value):
    # Violates constraint if the number of unassigned neighbors equals the number of lights still needed
    if(value == '_'):
        for wall in wc:
            if key in wc[wall]['Neighbors']:
                num_lights = 0
                num_none = 0
                for x in wc[wall]['Neighbors']:
                    if wc[wall]['Neighbors'][x] == 'b':
                        num_lights = num_lights + 1
                    if wc[wall]['Neighbors'][x] == None:
                        num_none = num_none + 1
                # maybe a bug when num_none == 0
                if (wc[wall]['Num'] - num_lights) == num_none:
                    return False
    if(value == 'b'):
        for wall in wc:
            if key in wc[wall]['Neighbors']:
                num_lit = 1
                for x in wc[wall]['Neighbors']:
                    if wc[wall]['Neighbors'][x] == 'b':
                        num_lit = num_lit + 1
                if num_lit > wc[wall]['Num']:
                    return False
    return True


# Updates wall constraint to new value
def wall_constraint_update(wc, key, value):
    for wall in wc:
        if key in wc[wall]['Neighbors']:
            wc[wall]['Neighbors'][key] = value


def check_max_depth(state):
    return len(state['A']) == state['W'] * state['H']


def check_constraints(state, key, value):
    return light_constraint_check(state['LC'], key, value) and wall_constraint_check(state['WC'], key, value)


def u_update(state, key, value):
    # update nodes adjacent to key in the constraint graph
    for u in state['U']:
        in_lc = u in state['LC'][key]['Connected']
        in_wc = False
        for wall in state['WC']:
            if key in state['WC'][wall]['Neighbors'] and u in state['WC'][wall]['Neighbors'] and key != u:
                in_wc = True

        if in_lc or in_wc:
            for val in state['U'][u]:
                if not check_constraints(state, u, val):
                    state['U'][u].remove(val)
                    if len(state['U'][u]) == 0:
                        state['None_empty'] = False


# this function indicates that a node has been updated
# and that its adjacent node's may need to be as well
def effect_node(state, key):
    # find adjacent nodesi
    if state['None_empty'] == False:
        pass
    for u in state['U']:
        in_lc = u in state['LC'][key]['Connected']
        in_wc = False
        for wall in state['WC']:
            if key in state['WC'][wall]['Neighbors'] and u in state['WC'][wall]['Neighbors'] and key != u:
                in_wc = True

        if in_lc or in_wc:
            updated = False
            for val in state['U'][u]:
                if key in state['U']:
                    valid = False
                    for possible in state['U'][key]:

                        state_copy = copy.deepcopy(state)

                        state_copy['U'].pop(key)
                        state_copy['A'][key] = possible
                        light_constraint_update(
                            state_copy['LC'], key, possible)
                        wall_constraint_update(state_copy['WC'], key, possible)
                        if check_constraints(state_copy, u, val):
                            valid = True
                        del state_copy
                    if not valid:
                        state['U'][u].remove(val)
                        updated = True
                        if len(state['U'][u]) == 0:
                            state['None_empty'] = False
                else:
                    if not check_constraints(state, u, val):
                        state['U'][u].remove(val)
                        updated = True
                        if len(state['U'][u]) == 0:
                            state['None_empty'] = False
            #print('key' + str(key))
            #print('u' + str(u))
            #print('val' + str(state['U'][u]))
            if updated:
                effect_node(state, u)


def update_state_forward_checking(state, key, value):
    state['A'][key] = value
    light_constraint_update(state['LC'], key, value)
    wall_constraint_update(state['WC'], key, value)
    u_update(state, key, value)

    state['Max_depth'] = check_max_depth(state)


def update_state_backtracking(state, key, value):
    state['A'][key] = value
    light_constraint_update(state['LC'], key, value)
    wall_constraint_update(state['WC'], key, value)

    state['Max_depth'] = check_max_depth(state)


def update_state_arc_consistent(state, key, value):

    state['A'][key] = value
    light_constraint_update(state['LC'], key, value)
    wall_constraint_update(state['WC'], key, value)
    effect_node(state, key)

    state['Max_depth'] = check_max_depth(state)
