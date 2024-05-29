import sys
import math

############### FUNCTIONS ###############

#return the values that satisfy row constraints
def validRow(cells, rowNum):
    arr = [1,2,3,4,5,6,7,8,9]
    for val in cells[rowNum]:
        if val != 0:
            arr.remove(val)
    return arr

#return the values that satisfy column constraints
def validCol(cells, colNum):
    arr = [1,2,3,4,5,6,7,8,9]
    for i in range(len(cells)):
        if cells[i][colNum] != 0:
            arr.remove(cells[i][colNum])
    return arr

#return the values that satisfy diagonal constraints
def validDiagonal(cells, rowNum, colNum):
    arr = [1,2,3,4,5,6,7,8,9]
    if rowNum == colNum:
        for i in range(9):
            if cells[i][i] != 0:
                arr.remove(cells[i][i])
    if rowNum + colNum == 8:
        for i in range(9):
            if cells[i][8-i] != 0 and cells[i][8-i] in arr:
                arr.remove(cells[i][8-i])
    return arr

#return the values that satisfy grid constraints
def validGrid(cells, rowNum, colNum):
    arr = [1,2,3,4,5,6,7,8,9]
    for i in range(3):
        for j in range(3):
            val = cells[((rowNum//3) * 3) + i][((colNum//3) * 3) + j]
            if val != 0:
                arr.remove(val)
    return arr

#put the valid values for each blank cell to the dict, and return the MRV value
def getValidValues(validVals):
    validVals.clear()
    minCount = 9
    #for cells with a value of 0:
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            arr = []
            if cells[i][j] == 0:
                #find the valid values
                for num in range(1,10):
                    if num in validRow(cells, i) and num in validCol(cells, j) and num in validDiagonal(cells, i , j) and num in validGrid(cells, i, j):
                        arr.append(num)
                #update the lowest remaining value
                if len(arr) < minCount:
                    minCount = len(arr)
                #add the list of possible values to the dict
                validVals.update({(i,j) : arr})
    return minCount

#get list of all coords that have the MRV, represented by minCount
def getMRVlist(validVals, minCount):
    ans = []
    for key, value in validVals.items():
        if len(value) == minCount:
            ans.append(key)
    return ans

#count number of unassigned "neighbors"
def numConstraints(cells, rowNum, colNum):
    #row
    constraints = []
    for i in range(len(cells[rowNum])):
        if cells[rowNum][i] == 0:
            constraints.append((rowNum, i))
    #column
    for i in range(len(cells)):
        if cells[i][colNum] == 0:
            if ((i, colNum)) not in constraints:
                constraints.append((i, colNum))
    #grid
    for i in range(3):
        for j in range(3):
            val = cells[((rowNum//3) * 3) + i][((colNum//3) * 3) + j]
            if val == 0:
                if ((i, j)) not in constraints:
                    constraints.append((i, j))
    #diagonal
    if rowNum == colNum:
        for i in range(9):
            if cells[i][i] == 0:
                if ((i, i)) not in constraints:
                    constraints.append((i, i))
    #diagonal
    if rowNum + colNum == 8:
        for i in range(9):
            if cells[i][8-i] == 0:
                if ((i, 8-i)) not in constraints:
                    constraints.append((i, 8-i))
    return len(constraints)

#Provided a list of cells with the same MRV, use degree heuristics to pick a cell
def useDegreeHeuristics(cells, MRVlist):
    max = MRVlist[0]
    maxCount = -math.inf
    for cell in MRVlist:
        temp = numConstraints(cells, cell[0],cell[1])
        if temp > maxCount:
            maxCount = temp
            max = cell
    return max


############### SETUP ###############

filename = sys.argv[1]
input = open(filename)
lines = input.readlines()
input.close()

cells = []
for i in range(len(lines)):
    if lines[i][0] != '\n':
        line = lines[i].strip().split()
        line = [int(val) for val in line]
        cells.append(line)


############### ALGORITHM ###############

def solve(cells):
    #store the possible values for each cell, updated with every iteration
    validVals = {}     #[row, col] : [values]
    newCells = cells.copy()

    minCount = getValidValues(validVals)    #lowest mrv value of all cells

    #validVals is only empty when there are no empty cells; solution has been found
    if not validVals:
        return newCells

    MRVlist = getMRVlist(validVals, minCount)   #list of cells with the lowest MRV
    best = useDegreeHeuristics(cells, MRVlist)  #cell with highest degree

    #if the cell has no valid values, this is not the right path to the solution
    if len(validVals[best]) == 0:
        return None

    #run the algorithm on all potential values for the cell
    for val in validVals[best]:
        newCells[best[0]][best[1]] = val
        solution = solve(newCells)
        if solution is not None:
            return solution

    #reset the value of the cell to 0
    newCells[best[0]][best[1]] = 0


############### OUTPUT ###############

ans = solve(cells)

output = open('output.txt', 'w')
for i in range(len(ans)):
    for j in range(len(ans[i])):
        output.write(str(ans[i][j]))
        if j != len(ans[i]) - 1:
            output.write(' ')
    if i != len(ans) - 1:
        output.write('\n')
