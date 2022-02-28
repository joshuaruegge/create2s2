# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import fileinput
import copy

inFile = open("in.txt", "r")

def rotate_2(a, i):
    temp = copy.deepcopy(a) #keeps lists inside main list from being linked
    for j in range(0,i):
        #pushes each value forwards a position (clockwise)
        buffer = temp[0][0]
        temp[0][0] = temp[1][0]
        temp[1][0] = temp[1][1]
        temp[1][1] = temp[0][1]
        temp[0][1] = buffer
    return temp

def rotate_3(a,i):
    temp = copy.deepcopy(a) #prevents linking between internal lists of outer list
    for j in range(0,i):
        #shuffles each outer row one position forwards (imagine turning the array like a wheel)
        buff1 = temp[0][1]
        buff2 = temp[0][2]
        temp[0][2] = temp[0][0]
        temp[0][1] = temp[1][0]
        temp[0][0] = temp[2][0]
        temp[1][0] = temp[2][1]
        temp[2][0] = temp[2][2]
        temp[2][1] = temp[1][2]
        temp[2][2] = buff2
        temp[1][2] = buff1
    return temp

#this was going to be "horizontal flip", but a vertical flip can be achieved by simply rotating twice and then horizontally flipping
def hflip_2(a):
    temp = copy.deepcopy(a)
    # essentially just mirror array
    for i in range(0,2):
        buff = temp[i][0]
        temp[i][0] = temp[i][1]
        temp[i][1] = buff
    return temp

#per above, a vertical flip is easier to implement and all possibilites are iterated over anyways
def flip_3(a):
    temp = copy.deepcopy(a)
    buff = temp[0]
    temp[0] = temp[2]
    temp[2] = buff
    return temp

def print_array(a):
    for i in range(0,len(a)):
        print(a[i])
    print()

#shortcut methods that auto-determine array size
def rotate(a,i):
    if len(a) == 2:
        return rotate_2(a,i)
    else:
        return rotate_3(a,i)

def flip(a):
    if len(a) == 2:
        return hflip_2(a)
    else:
        return flip_3(a)

#fetches all potential rotations and flips of a 2x2 or 3x3 chunk
def permutations(a):
    temp = copy.deepcopy(a)
    master = []
    #for each of the 4 potential orientations, adds both the rotation and the rotation's flipped version
    for i in range(0,4):
        rot = rotate(temp,i)
        flipped = flip(rot)
        if rot not in master:
            master.append(rot)
        if flipped not in master:
            master.append(flipped)
    return master

#converts 2d array to tuple of tuples
def tuple2d(a):
    temp = []
    for i in a:
        temp.append(tuple(i))
    return tuple(temp)

#converts 2-dimensional tuple back to 2-dimensional array
def backToArray(a):
    temp = []
    for i in a:
        tempRow = []
        for j in i:
            tempRow.append(j)
        temp.append(tempRow)
    return temp

#conversion rules dictionary
rules = {}

#input parsing for the unique way this exercise provides input
for line in inFile:
    chunks = line.split(" => ")
    chunks[1] = chunks[1][:-1]
    ruleRows = chunks[0].split("/")
    tempRule = []
    for i in range(0,len(ruleRows)):
        tempRuleRow = []
        for j in ruleRows[i]:
            if j == ".":
                tempRuleRow.append(0)
            else:
                tempRuleRow.append(1)
        tempRule.append(tempRuleRow)
    resultRows = chunks[1].split("/")
    tempResult = []
    for i in range(0,len(resultRows)):
        tempResultRow = []
        for j in resultRows[i]:
            if j == ".":
                tempResultRow.append(0)
            else:
                tempResultRow.append(1)
        tempResult.append(tempResultRow)
    tempRule = tuple2d(tempRule)
    tempResult = tuple2d(tempResult)
    rules[tempRule] = tempResult
    #rules ends up as a list of tuple keys representing the tuple they should become, allowing for easy lookup later on

#test cases:
#master = [[0,1,1,0],[1,0,0,1],[1,1,0,0],[0,0,1,1]]
#master = [[0,1,0],[0,0,1],[1,1,1]]
master = []

#obtain player input for starting condition
for x in range(0,3):
    row = input("Input row:")
    tempRow = []
    for i in row:
        if i == "#" or i == "1":
            tempRow.append(1)
        else:
            tempRow.append(0)
    master.append(tempRow)

print("Starting map:")
print_array(master)

for x in range(0,5):
    print("Iteration:", x)
    chunks = []
    #variables for determining size of array later on
    inc = 0
    rows = 0
    cols = 0
    #breaks the current map into either 2x2 or 3x3 chunks, based on whichever fits evenly
    #because initial condition should always be 3x3, array will remain square (rows = columns)
    if len(master) % 2 == 0:
        inc = 2
        rows = len(master)//2
        cols = len(master[0])//2
        for i in range(0,len(master),2):
            for j in range(0,len(master[i]),2):
                temp = []
                temp.append(master[i][j:j+2])
                temp.append(master[i+1][j:j+2])
                chunks.append(temp)
    else:
        inc = 3
        rows = len(master)//3
        cols = len(master[0])//3
        for i in range(0,len(master),3):
            for j in range(0,len(master[i]),3):
                temp = []
                temp.append(master[i][j:j+3])
                temp.append(master[i+1][j:j+3])
                temp.append(master[i+2][j:j+3])
                chunks.append(temp)
    #go through our chunks and perform the replacement rules
    for i in chunks:
        perms = permutations(i)
        for j in perms:
            if tuple2d(j) in rules.keys():
                chunks[chunks.index(i)] = backToArray(rules.get(tuple2d(j)))
                break
    #populate master with new values
    master = []
    tempArray = []
    #basically, create empty array with required number of columns, then add to master as many times as is necessary for rows
    #because 2x2 chunks result in 3x3 chunks and 3x3 chunks result in 4x4 chunks, master will always "grow" by 1 times the number of columns
    #meaning its total size is (number of columns * original size) + (number of columns) or factorized (number of columns * (original size + 1))
    for i in range(0,(cols) * (inc+1)):
        tempArray.append(0)
    for i in range(0,(rows) * (inc+1)):
        #DEEPCOPY!!!
        master.append(copy.deepcopy(tempArray))

    if inc == 2:
        curRow = 0
        curCol = 0
        #essentially iterate through master in 3x3 chunks, inserting the values of the "chunk" array in order
        while(len(chunks) > 0):
            for i in range(0,3):
                for j in range(0,3):
                    master[curRow + i][curCol + j] = chunks[0][i][j]
            curCol += 3
            #map to next row if reaching the end
            if curCol >= len(master[curRow]):
                curRow += 3
                curCol = 0
            chunks.pop(0)
    else:
        curRow = 0
        curCol = 0
        #same as above, but 4x4 chunks
        while (len(chunks) > 0):
            for i in range(0, 4):
                for j in range(0, 4):
                    master[curRow + i][curCol + j] = chunks[0][i][j]
            curCol += 4
            if curCol >= len(master[curRow]):
                curRow += 4
                curCol = 0
            chunks.pop(0)
    print("Current map:")
    print_array(master)
    count = 0
    for i in master:
        for j in i:
            count += j
    print("Number of 1s:",count)
















