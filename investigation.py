# use normal forward checking
from forward_checking import arc_consistent as ah0
# use forward checking with heuristic 1
from forward_checking_h1 import arc_consistent as ah1
# use forward checking with heuristic 2
from forward_checking_h2 import arc_consistent as ah2
# use forward checking with heuristic 3
from forward_checking_h3 import arc_consistent as ah3
from backtrack import backtracking as bh0  # use normal backtracking
# use backtracking with heuristic 1
from backtrack_h1 import backtracking as bh1
# use backtracking with heuristic 2
from backtrack_h2 import backtracking as bh2
# use backtracking with heuristic 3
from backtrack_h3 import backtracking as bh3
from read import read, printPuzzle
import timeit

# this method initialize everything and return a list of dictionaries.
# Each dictionray corresponds to an algorithm as described above


def initialize():
    list1 = [{'name': None, 'function': None, 'time': 0, 'numVisited': 0}
             for y in range(8)]
    names = ['normal forward checking', 'forward checking with heuristic 1',
             'forward checking with heuristic 2', 'forward checking with heuristic 3',
             'normal backtracking', 'backtracking with heuristic 1',
             'backtracking with heuristic 2', 'backtracking with heuristic 3']
    functions = [ah0, ah1, ah2, ah3, bh0, bh1, bh2, bh3]
    for i in range(len(list1)):
        list1[i]['name'], list1[i]['function'] = names[i], functions[i]
    return list1


# this method takes in a 2d array and solves it using different algorithms.
# it will also print out the time it spends and node visited
def investigate():
    puzzle = read()['puzzle']
    list1 = initialize()
    for i in range(len(list1)):
        t_initial = timeit.default_timer()
        solution, list1[i]['numVisited'] = list1[i]['function'](puzzle)
        list1[i]['time'] = timeit.default_timer() - t_initial
        print('{} solves the puzzle'.format(list1[i]['name']))
        print('{} nodes visited'.format(list1[i]['numVisited']))
        print('the answer is:')
        printPuzzle(solution)
    for dict1 in list1:
        time = dict1['time']
        name = dict1['name']
        num = dict1['numVisited']
        print('{} solved the puzzle in {} s. {} nodes were visited'.format(
            name, time, num))
