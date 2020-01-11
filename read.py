
import sys
row=0  #the number of rows
col=0  #the number of cols
puzzle=[] #a 2d-array
data={'row':0,'col':0,'puzzle':puzzle} #this is the dictionary, row&col are integer and puzzle is a 2-d array

#use the format provided in the assignment(i.e. the first 2 lines must specify the start and the dimension)
def read():         #this method reads from stdin and returns a dictionary containing a 2d-array
    print("plz enter your puzzle")
    linesArr = sys.stdin.read().splitlines()
    temp=[int(s) for s in linesArr[1].split() if s.isdigit()]   #temp stores number of rows and cols
    row, col=temp[0], temp[1]
    puzzle1=[[0 for x in range(col)]for y in range(row)]    #first initialize this 2d-array with 0's
    linesArr=linesArr[2:len(linesArr)-1]
    for i in range(row):        #iterate thru linesArr(a String array), if integer is found, convert it into integer
        for j in range(col):
            if(linesArr[i][j].isdigit()):puzzle1[i][j]=int(linesArr[i][j])
            else:puzzle1[i][j]=linesArr[i][j]
    data['row'], data['col'], data['puzzle']=row,col,puzzle1    #assign new values to the dictionary
    return data


