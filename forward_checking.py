from judah_state_forward import parse_puzzle,unparse_puzzle, update_state_arc_consistent, check_constraints
from read import read,printPuzzle
import copy


#Takes a 2d array puzzle
#retuns a 2d array solution 
#OR None if no solution was found
def arc_consistent(puzzle):    
    state = parse_puzzle(puzzle)
    result,num_nodes = arc_consistent_helper(state)
    if result['Max_depth']:
        return unparse_puzzle(result),num_nodes
    else:
        None
        
def arc_consistent_helper(state):

    num_nodes = 1
    
    # if all the nodes are in A, that is, the puzzle is at max depth
    if state['Max_depth'] or not state['None_empty']:
        return state,num_nodes
    for x in range(2):
        state_copy = copy.deepcopy(state)
        curr,value = state_copy['U'].popitem()
        if(x < len(value)):
            update_state_arc_consistent(state_copy,curr,value[x])
            
            result,num_nodes_child = arc_consistent_helper(state_copy)
            
            num_nodes = num_nodes + num_nodes_child
            if(result['Max_depth'] or not state['None_empty']):
                return result,num_nodes

    return state,num_nodes

def solve_puzzle():
    while True:
        puzzle=read()['puzzle']
        result,num_nodes=arc_consistent(puzzle)
        print()
        if result == None:
            print('no solution found')
        else:
            print('the answer is:')
            printPuzzle(result)
            print('Number of Nodes Visited: ' + str(num_nodes))
