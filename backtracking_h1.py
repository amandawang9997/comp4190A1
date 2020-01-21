from read import printPuzzle,read
from judah_state_forward import (parse_puzzle,unparse_puzzle,get_next_u_h1,
        check_constraints,update_state_backtracking)
import copy

#the main loop so that it will always ask an input then solve the puzzle
def solve_puzzle():
    
        while True:
            puzzle=read()['puzzle']
            result,num_nodes = backtracking(puzzle)
            
            print()
            if result == None:
                print('no solution found')
            else:
                print('the answer is:')
                printPuzzle(result)
                print('Number of Nodes Visited: ' + str(num_nodes))

def backtracking(puzzle):
    state = parse_puzzle(puzzle)
    
    result,num_nodes = backtrackingHelper(state)
    if result['Solved']:
        return unparse_puzzle(result),num_nodes
    else:
        return None,None

def backtrackingHelper(state):
    num_nodes = 1

    if state['Solved']:
        return state,num_nodes
    
    for x in range(2):
        state_copy = copy.deepcopy(state)
        curr,value = get_next_u_h1(state_copy) 
        if(x < len(value)):
            if(check_constraints(state_copy,curr,value[x])):
                update_state_backtracking(state_copy,curr,value[x])

                result, num_nodes_child = backtrackingHelper(state_copy)

                num_nodes = num_nodes  + num_nodes_child

                if result['Solved']:
                    return result,num_nodes

    return state, num_nodes

