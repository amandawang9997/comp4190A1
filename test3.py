# run this file to test
from read import read, printPuzzle
import mostConstraining as mc
import rule as rl

# the following code solves puzzle one at a time
puzzle = read()['puzzle']
# print(mc.mostConstrainingCell(puzzle, rl.getUnassigned(puzzle)))
mc.mainLoopmC()
# print(rl.getUnassigned(puzzle))
