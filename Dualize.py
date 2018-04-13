#Run by typing python Dualize.py MPSfilename

import pprint
from collections import OrderedDict
from collections import defaultdict
import sys
import os

file_name = sys.argv[1]

with open(file_name) as file:
    mpsContents = file.readlines()


class DefaultOrderedDict(OrderedDict):
    def __missing__(self, key):
        val = self[key] = type(self)()
        return val


# Line Number where ROWS section starts in MPS file
rowsLNo = mpsContents.index("ROWS\n")

# Line Number where COLUMNS section start in MPS file
colsLNo = mpsContents.index("COLUMNS\n")

# Line Number where RHS section start in MPS file
rhsLNo = mpsContents.index("RHS\n")

# Line Number where ENDATA section starts in MPS file
endLNo = mpsContents.index("ENDATA\n")


rangesLno = 0



# Line Number where Bounds section start in MPS file
if "BOUNDS\n" in mpsContents:
    boundsLNo = mpsContents.index("BOUNDS\n")
else:
    boundsLNo = endLNo

# Line Number where RANGES begin

if "RANGES\n" in mpsContents and "BOUNDS\n" in mpsContents:
    rangesLno = mpsContents.index("RANGES\n")
elif "RANGES\n" in mpsContents and "BOUNDS\n" not in mpsContents:
    rangesLno = mpsContents.index("RANGES\n")
elif "RANGES\n" not in mpsContents and "BOUNDS\n" in mpsContents:
    rangesLno = boundsLNo
elif "RANGES\n" not in mpsContents and "BOUNDS\n" not in mpsContents:
    rangesLno = endLNo

# Get the objective Name:
objName = ''
for i in range(rowsLNo + 1, colsLNo):
    #print(mpsContents[i][1:3].strip())
    if mpsContents[i][1:3].strip() == 'N':
        objName = mpsContents[i][4:12].strip()
        break

#print("The objective name is:", objName)

# Get different kind of rows:

Nrows = []
Lrows = []
Grows = []
Erows = []
rowNames = []  # list of all the row names that appear the order of the mps file

rhsValues = DefaultOrderedDict()

primalName = ''
for i in range(0, rowsLNo):
    if mpsContents[i][:4].lower() == "name":
        primalName = mpsContents[i][14:]
#print("Primal Name:", primalName)

for i in range(rowsLNo + 1, colsLNo):
    if mpsContents[i][1:3].strip() == 'N':
        Nrows.append(mpsContents[i][4:12].strip())

    if mpsContents[i][1:3].strip() == 'L':
        Lrows.append(mpsContents[i][4:12].strip())

    if mpsContents[i][1:3].strip() == 'E':
        Erows.append(mpsContents[i][4:12].strip())

    if mpsContents[i][1:3].strip() == 'G':
        Grows.append(mpsContents[i][4:12].strip())

# add all the row names
for i in range(rowsLNo + 1, colsLNo):
    if mpsContents[i][4:12].strip() != '':
        rowNames.append(mpsContents[i][4:12].strip())

# remove the Cost Row

#print("Row names before removing objective: ", rowNames)

if objName in rowNames:
    rowNames.remove(objName)
#print("Row names after removing objective: ", rowNames)

listOfVars = []

# Get list of vars
for i in range(colsLNo + 1, rhsLNo):
    varName = mpsContents[i][4:12].strip()
    if not (varName in listOfVars):
        listOfVars.append(varName)
    varName = mpsContents[i][4:12].strip()
    if not (varName in listOfVars):
        listOfVars.append(varName)

# Another list of row names to get a list of redundant rows
actualRowNames = []

print("Number of EQ rows: ", str(len(Erows)))
print("Number of LE+GE rows: ", str(len(Lrows)+len(Grows)))

# create an empty A array
AMatrix = DefaultOrderedDict()

for i in range(colsLNo + 1, rhsLNo):
    varName = mpsContents[i][4:12].strip()
    rowName1 = mpsContents[i][14:22].strip()
    if rowName1 not in actualRowNames:
        actualRowNames.append(rowName1)
    rowName2 = mpsContents[i][39:47].strip()
    if rowName2 not in actualRowNames:
        actualRowNames.append(rowName2)

    if (varName in listOfVars) and (rowName1 in Grows):
        AMatrix[rowName1][varName] = float(mpsContents[i][24:36].strip())
    if (varName in listOfVars) and (rowName1 in Erows):
        AMatrix[rowName1][varName] = float(mpsContents[i][24:36].strip())
    if (varName in listOfVars) and (rowName1 in Lrows):
        AMatrix[rowName1][varName] = float(mpsContents[i][24:36].strip())
    if (varName in listOfVars) and (rowName1 in Nrows):
        AMatrix[rowName1][varName] = float(mpsContents[i][24:36].strip())

    if (varName in listOfVars) and (rowName2 in Grows):
        AMatrix[rowName2][varName] = float(mpsContents[i][49:61].strip())
    if (varName in listOfVars) and (rowName2 in Erows):
        AMatrix[rowName2][varName] = float(mpsContents[i][49:61].strip())
    if (varName in listOfVars) and (rowName2 in Lrows):
        AMatrix[rowName2][varName] = float(mpsContents[i][49:61].strip())
    if (varName in listOfVars) and (rowName2 in Nrows):
        AMatrix[rowName2][varName] = float(mpsContents[i][49:61].strip())

# Getting first RHS names

if rhsLNo+1 != rangesLno:
    firstRHSName = mpsContents[rhsLNo + 1][4:12].strip()
    if not firstRHSName:
        firstRHSName = "RHSdft"
else:
    firstRHSName = "RHSdft"
if rhsLNo+1 != rangesLno:
    for i in range(rhsLNo + 1, rangesLno):
        if not mpsContents[i][4:12].strip() and (mpsContents[i][4:12].strip() == firstRHSName):
            rowName1 = mpsContents[i][14:22].strip()
            rowName2 = mpsContents[i][39:47].strip()
            if rowName1 in Grows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())
            if rowName1 in Erows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())
            if rowName1 in Lrows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())
            if rowName1 in Nrows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())

            if rowName2 in Grows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
            if rowName2 in Erows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
            if rowName2 in Lrows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
            if rowName2 in Nrows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
        else:  # when there is not RHS name
            rowName1 = mpsContents[i][14:22].strip()
            rowName2 = mpsContents[i][39:47].strip()
            if rowName1 in Grows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())
            if rowName1 in Erows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())
            if rowName1 in Lrows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())
            if rowName1 in Nrows:
                rhsValues[rowName1] = float(mpsContents[i][24:36].strip())

            if rowName2 in Grows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
            if rowName2 in Erows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
            if rowName2 in Lrows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())
            if rowName2 in Nrows:
                rhsValues[rowName2] = float(mpsContents[i][49:61].strip())


plVariableBounds = []
frVariableBounds = []
upVariableBounds = DefaultOrderedDict()
loVariableBounds = DefaultOrderedDict()
miVariableBounds = []
fxVariableBounds = DefaultOrderedDict()

'''*******************************Begin RANGES Analysis*************************************************'''

rangedRows = DefaultOrderedDict()


#print("Debug:  Ranges number" ,rangesLno, boundsLNo)
if rangesLno + 1 != boundsLNo and rangesLno != boundsLNo:
    firstRangeName = mpsContents[rangesLno+1].split()[0]
    if not firstRangeName:
        firstRangeName = "DefRng"
else:
    firstRangeName = "DefRang"

if rangesLno + 1 != boundsLNo and rangesLno != boundsLNo:
    tempRowName = ''
    for i in range(rangesLno+1, boundsLNo):
        listedRange = mpsContents[i].split()
        if listedRange[0] == firstRangeName:
            tempRowName = listedRange[1]
            r = listedRange[2]
        else:
            tempRowName = listedRange[0]
            r = listedRange[1]
    rangedRows[tempRowName] = float(r)

#print(rangedRows)
varCounter = 0
for row in rangedRows:
    if row in Grows:
        lRange = rhsValues[row]
        uRange = rhsValues[row] + abs(rangedRows[row])
        newVar = 'Rv' + str(varCounter)
        AMatrix[row][newVar] = -1
        listOfVars.append(newVar)
        rhsValues[row] = lRange
        Erows.append(row)
        newRow = 'Rr' + str(varCounter)
        AMatrix[newRow][newVar] = 1
        Lrows.append(newRow)
        rowNames.append(newRow)
        plVariableBounds.append(newVar)
        rhsValues[newRow] = uRange-lRange
        if newRow not in actualRowNames:
            actualRowNames.append(newRow)
    if row in Grows:
        Grows.remove(row)
    varCounter += 1
    if row in Lrows:
        lRange = rhsValues[row] - abs(rangedRows[row])
        uRange = rhsValues[row]
        newVar = 'Rv' + str(varCounter)
        AMatrix[row][newVar] = -1
        listOfVars.append(newVar)
        rhsValues[row] = lRange
        Erows.append(row)
        newRow = 'Rr' + str(varCounter)
        AMatrix[newRow][newVar] = 1
        Lrows.append(newRow)
        rowNames.append(newRow)
        plVariableBounds.append(newVar)
        rhsValues[newRow] = uRange-lRange
        if newRow not in actualRowNames:
            actualRowNames.append(newRow)
    if row in Lrows:
        Lrows.remove(row)
    varCounter += 1
    if row in Erows:
        if float(r) > 0:
            lRange = rhsValues[row]
            uRange = rhsValues[row] + abs(rangedRows[row])
        else:
            lRange = rhsValues[row] - abs(rangedRows[row])
            uRange = rhsValues[row]
        newVar = 'Rv' + str(varCounter)
        AMatrix[row][newVar] = -1
        listOfVars.append(newVar)
        rhsValues[row] = lRange
        Erows.append(row)
        newRow = 'Rr' + str(varCounter)
        AMatrix[newRow][newVar] = 1
        Lrows.append(newRow)
        rowNames.append(newRow)
        plVariableBounds.append(newVar)
        rhsValues[newRow] = uRange - lRange
        if newRow not in actualRowNames:
            actualRowNames.append(newRow)
    if row in Erows:
        Erows.remove(row)




'''********************************End RANGES Analysis**************************************************'''

if boundsLNo == endLNo:  # All the variables are set to Positive
    for i in listOfVars:
        plVariableBounds.append(i)

if boundsLNo != endLNo:
    # adding the free variables
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'FR':
            frVariableBounds.append(mpsContents[i][14:22].strip())
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'UP':
            varName_1 = mpsContents[i][14:22].strip()
            upVariableBounds[varName_1] = float(mpsContents[i][24:36].strip())
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'LO':
            varName_2 = mpsContents[i][14:22].strip()
            loVariableBounds[varName_2] = float(mpsContents[i][24:36].strip())
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'FX':
            varName_3 = mpsContents[i][14:22].strip()
            fxVariableBounds[varName_3] = float(mpsContents[i][24:36].strip())
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'MI':
            varName_2 = mpsContents[i][14:22].strip()
            miVariableBounds.append(varName_2)

    for varName in listOfVars:
        if (varName not in miVariableBounds) and (varName not in loVariableBounds.keys()) and (
                    varName not in upVariableBounds.keys()) and (varName not in frVariableBounds) and (
                    varName not in fxVariableBounds):
            plVariableBounds.append(varName)

if boundsLNo != endLNo:
    firstBoundName = mpsContents[boundsLNo + 1][4:12].strip()
# Getting the type of Rows


pp = pprint.PrettyPrinter(indent=4, depth=4)

listOfVarsObj = list(listOfVars)
listOfVarsObj.append(objName)

for variable in listOfVarsObj:
    if variable in upVariableBounds or variable in loVariableBounds or variable in fxVariableBounds:
        for row in AMatrix:
            for col in AMatrix[row]:
                if not rhsValues[row]:
                    rhsValues[row] = 0



NoOfRangeVariables = len(list(set(upVariableBounds.keys())&set(loVariableBounds.keys())));

print('UP Variables are: ', len(upVariableBounds)-NoOfRangeVariables);
print('LO Variables are: ', len(loVariableBounds)-NoOfRangeVariables);
print('range variables are: ', NoOfRangeVariables)
print('FR Variable Bounds are: ', len(frVariableBounds))
print('FX variable bounds are: ', len(fxVariableBounds))




tempRowsAndVars = {}
tempRowsAndVarsFX = defaultdict(list)   # for fixed variables

for variable in listOfVarsObj:

    if variable in fxVariableBounds:

        for row in AMatrix:
            for col in AMatrix[row]:
                if col == variable:
                    if row in rhsValues:
                        rhsValues[row] = rhsValues[row] - AMatrix[row][col]*(fxVariableBounds[variable])
                    else:
                        rhsValues[row] = rhsValues[row] - AMatrix[row][col]*(fxVariableBounds[variable])
                    #print(row, variable)
                    tempRowsAndVarsFX[row].append(variable)

    if variable not in upVariableBounds and variable in loVariableBounds:
        for row in AMatrix:
            for col in AMatrix[row]:
                if col == variable:
                    if row in rhsValues:
                        rhsValues[row] = rhsValues[row] - AMatrix[row][col] * (loVariableBounds[variable])
                    else:
                        #print("Row being iterated:", row)
                        rhsValues[row] = rhsValues[row] - AMatrix[row][col] * loVariableBounds[variable]

                    plVariableBounds.append(variable)
        del loVariableBounds[variable]

    if variable in upVariableBounds and variable not in loVariableBounds:
        tempRowName = "R" + str(listOfVarsObj.index(variable))
        rowNames.append(tempRowName)
        Lrows.append(tempRowName)
        tempRowsAndVars[tempRowName] = variable
        plVariableBounds.append(variable)
        rhsValues[tempRowName] = upVariableBounds[variable]
        actualRowNames.append(tempRowName)
        del upVariableBounds[variable]

    if variable in upVariableBounds and variable in loVariableBounds:
        for row in AMatrix:
            for col in AMatrix[row]:
                if col == variable:
                    if row in rhsValues:
                        rhsValues[row] = rhsValues[row] - AMatrix[row][col] * (loVariableBounds[variable])
                    else:
                        rhsValues[row] = rhsValues[row] - AMatrix[row][col] * loVariableBounds[variable]
        upVariableBounds[variable] -= loVariableBounds[variable]
        tempRowName = "R" + str(listOfVarsObj.index(variable))
        rowNames.append(tempRowName)
        Lrows.append(tempRowName)
        tempRowsAndVars[tempRowName] = variable
        plVariableBounds.append(variable)
        rhsValues[tempRowName] = upVariableBounds[variable]
        actualRowNames.append(tempRowName)
        del loVariableBounds[variable]

for row in tempRowsAndVars:
    AMatrix[row][tempRowsAndVars[row]] = 1


for row in tempRowsAndVarsFX:
    for col in tempRowsAndVarsFX[row]:
        AMatrix[row][col] = 0
        if col in listOfVars:
            listOfVars.remove(col)
        if col is listOfVarsObj:
            listOfVarsObj.remove(col)

#print("The AMatrix is given by:")
#print(AMatrix)

# Writing the Primal String
s = "NAME" + 10*" "
s += primalName
s += "ROWS\n"
s += " N " + " "
s += objName+"\n"
for i in Lrows:
    s += " L " + " " + i + '\n'
for j in Grows:
    s += " G " + " " + j + '\n'
for k in Erows:
    s += " E " + " " + k + '\n'

s += "COLUMNS\n"
# for var in actualRowNames:
#     if var in AMatrix.keys():
#         for col in listOfVars:
#             if AMatrix[var].get(col):
#                 s += ' '*4 + col
#                 s += (10-len(col))*' ' + var + (10-len(var))* ' ' + str(AMatrix[var][col]) + '\n'

for col in listOfVars:
    for var in actualRowNames:
        if var in AMatrix.keys():
            if AMatrix[var].get(col):
                s += ' ' * 4 + col
                s += (10 - len(col)) * ' ' + var + (10 - len(var)) * ' ' + str(AMatrix[var][col]) + '\n'
s += "RHS\n"

for row in rhsValues:
    s += 4 * ' ' + firstRHSName + + (10 - len(firstRHSName)) * ' ' + row + (10 - len(str(i))) * ' ' + str(rhsValues[row]) + '\n'

if len(frVariableBounds) > 0:
	s += "BOUNDS\n"
	for var in frVariableBounds:
		s += ' ' + 'FR' + ' ' + firstBoundName + (10-len(firstBoundName))*' ' + var + '\n'

s += "ENDATA\n"

fileNameOut = os.path.splitext(file_name)[0] + "ModPrimal.mps"

print(fileNameOut, " has been succesfully written to the disk")
with open(fileNameOut, "w") as text_file:
    text_file.write(s)


# writing the Dual String
s = ''
s = "NAME" + 10 * " "
dualName = "TESTDUAL\n"
s += dualName
s += "OBJSENSE\n"
s += "    " + "MAX\n"
s += "ROWS\n"
s += " N " + " "
s += firstRHSName + "\n"

# sortedPLvariables = sorted(plVariableBounds.keys())
for i in listOfVars:
    if i in plVariableBounds:
        s += " L " + " " + i + '\n'
    if i in miVariableBounds:
        s += " G " + " " + i + '\n'
    if i in frVariableBounds:
        s += " E " + " " + i + '\n'

s += "COLUMNS\n"

#print('keys of Amatrix:', AMatrix.keys())
#print('RowNames', actualRowNames)

for var in rowNames:
    if var in AMatrix.keys():
        if var in rhsValues.keys():
            s += ' ' * 4 + var
            s += (10 - len(var)) * ' ' + firstRHSName + (10 - len(firstRHSName)) * ' ' + str(rhsValues[var]) + '\n'
            for col in listOfVars:
                if AMatrix[var].get(col):
                    s += ' ' * 4 + var
                    s += (10 - len(var)) * ' ' + col + (10 - len(col)) * ' ' + str(AMatrix[var][col]) + '\n'
        else:
            for col in listOfVars:
                if AMatrix[var].get(col):
                    s += ' ' * 4 + var
                    s += (10 - len(var)) * ' ' + col + (10 - len(col)) * ' ' + str(AMatrix[var][col]) + '\n'

s += "RHS\n"
#print("Printing RHS:")
for i in listOfVarsObj:
    if AMatrix[objName].get(i):
        s += 4 * ' ' + objName + + (10 - len(objName)) * ' ' + i + (10 - len(i)) * ' ' + str(AMatrix[objName][i]) + '\n'

#print("Debug: RHS values: ********************", rhsValues)

if objName in rhsValues.keys() and rhsValues[objName] != 0:
    #print("Debug: RHS: ********************", rhsValues[objName])
    s += 4 * ' ' + objName + + (10 - len(objName)) * ' ' + firstRHSName + (10 - len(objName)) * ' ' + str(
        -1 * rhsValues[objName]) + '\n'
elif objName in rhsValues.keys():
    del rhsValues[objName]

defaultBndName = 'B1'

if Lrows or Erows:
    s += "BOUNDS\n"
    for name in actualRowNames:
        #print("Debug: rowName,", name)
        if name in Lrows:
            s += " " + "MI" + " " + defaultBndName + (10 - len(defaultBndName)) * ' ' + name + '\n'
            s += " " + "UP" + " " + defaultBndName + (10 - len(defaultBndName)) * ' ' + name + (10 - len(
                name)) * ' ' + '0' + '\n'
        if name in Erows:
            s += " " + "FR" + " " + defaultBndName + (10 - len(defaultBndName)) * ' ' + name + '\n'

s += "ENDATA\n"
fileNameOut = os.path.splitext(file_name)[0] + "Dual.mps"

print(fileNameOut, " has been succesfully written to the disk")
with open(fileNameOut, "w") as text_file:
    text_file.write(s)
