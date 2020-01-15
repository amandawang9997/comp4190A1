#run this file to test
from read import read
import rule as rl,backtracking as bt
state=read()['puzzle']
arr=rl.goodCells(state)
print(arr)
print(rl.solutionCheck(state))
