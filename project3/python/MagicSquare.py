def isMagic(square): # this will check if the givien is a Magic or not by the square

    result = isMatrix(square) # the result of the matrix will be checked here 

    if result:
        sums = []
        # diagonal (of a straight line)\
        sum = 0
        for x in range(len(square)):
            sum += square[x][x]
        
        sums.append(sum)

        # diagonal /
        sum = 0
        y = len(square) - 1
        for x in range(len(square)):
            sum += square[x][y]
            y -= 1
        
        sums.append(sum)

        # for the rows _
        sum = 0
        for x in range(len(square)):
            for y in range(len(square)):
                sum += square[x][y]
            sums.append(sum)
            sum = 0
        
        # for the columns |
        sum = 0
        for x in range(len(square)):
            for y in range(len(square)):
                sum += square[y][x]
            sums.append(sum)
            sum = 0        
        
        # check if all are similar
        value = sums[0]
        for i in range(1, len(sums)):
            if sums[i] != value:
                result = False
                break
    #end of our if
    return result

# This will check if is a list is of n x n 
def isMatrix(m):
    result = True

    size = len(m)

    for row in m:
        if len(row) != size:
            result = False
            break
    
    return result

def printMatrix(matrix):
	for subList in matrix:
		print(subList)

square = [  #example
    [ 2, 7, 6 ],
    [ 9, 5, 1 ],
    [ 4, 3, 8 ]
]

print("Our Square:")
printMatrix(square)
print("")
print("Is It magic square?")
print ({isMagic(square)})