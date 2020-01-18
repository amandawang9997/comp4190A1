# run this file to test
from read import read, printPuzzle
import mostConstraining as mc
import rule as rl
import howmanyconstrains as hc
# the following code solves puzzle one at a time

# print(mc.mostConstrainingCell(puzzle, rl.getUnassigned(puzzle)))

# print(rl.getUnassigned(puzzle))

puzzle = read()['puzzle']
print(hc.getConstrains(puzzle))
