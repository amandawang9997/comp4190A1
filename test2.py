import read
import forward_checking as fc
state = read.read()['puzzle']
print(fc.getArcsRowCol(state))
