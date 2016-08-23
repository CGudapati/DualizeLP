import pprint
from collections import OrderedDict
import json
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

# Line Number where Bounds section start in MPS file
if "BOUNDS\n" in mpsContents:
    boundsLNo = mpsContents.index("BOUNDS\n")
else:
    boundsLNo = endLNo

# Get the objective Name:
objName = ''
for i in range(rowsLNo + 1, colsLNo):
    print(mpsContents[i][1:3].strip())
    if mpsContents[i][1:3].strip() == 'N':
        objName = mpsContents[i][4:12].strip()
        break

print("The objective name is:", objName)

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
print("Primal Name:", primalName)

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

print("Row names before removing objective: ", rowNames)

if objName in rowNames:
    rowNames.remove(objName)
print("Row names after removing objective: ", rowNames)

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

firstRHSName = mpsContents[rhsLNo + 1][4:12].strip()
if not firstRHSName:
    firstRHSName = "RHS"

for i in range(rhsLNo + 1, boundsLNo):
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
            upVariableBounds[varName_1] = mpsContents[i][24:36].strip()
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'LO':
            varName_2 = mpsContents[i][14:22].strip()
            loVariableBounds[varName_2] = mpsContents[i][24:36].strip()
    for i in range(boundsLNo + 1, endLNo):
        if mpsContents[i][1:3] == 'MI':
            varName_2 = mpsContents[i][14:22].strip()
            miVariableBounds.append(varName_2)
    for varName in listOfVars:
        print("Test var name being tested for PL:", varName)
        if (varName not in miVariableBounds) and (varName not in loVariableBounds.keys()) \
                and (varName not in upVariableBounds.keys()) and (varName not in frVariableBounds):
            plVariableBounds.append(varName)

if boundsLNo != endLNo:
    firstBoundName = mpsContents[boundsLNo + 1][4:12].strip()
# Getting the type of Rows


pp = pprint.PrettyPrinter(indent=4, depth=3)



print("Amatrix: ")

# since pretty printing the default dictionary is not working
print(json.dumps(AMatrix, indent=4))

print("Nrows", Nrows)
print("Lrows", Lrows)
print("Grows", Grows)
print("Erows", Erows)
print("List Of Vars", listOfVars)

print("RHS names:")
print(firstRHSName)

print("RHS values:")
pp.pprint(rhsValues)
print("PL variables")
print(plVariableBounds)
print("FR variables", frVariableBounds)
print("MI variables", miVariableBounds)
print("UP variables")
pp.pprint(upVariableBounds)
print("LO variables")
pp.pprint(plVariableBounds)

# Analysis of Bound Variables
for variable in listOfVars:
    # if variable in upVariableBounds and variable in loVariableBounds:

    if variable in upVariableBounds and variable not in loVariableBounds:
        tempRowName = variable[:4]+"BC"
        rowNames.append(tempRowName)
        Lrows.append(tempRowName)
        AMatrix[tempRowName][variable] = 1
        plVariableBounds.append(variable)
        rhsValues[tempRowName] = upVariableBounds[variable]
        actualRowNames.append(tempRowName)
    if variable not in upVariableBounds and variable in loVariableBounds:
        tempRowName = variable[:4]+"BC"
        rowNames.append(tempRowName)
        Grows.append(tempRowName)
        AMatrix[tempRowName][variable] = 1
        frVariableBounds.append(variable)
        rhsValues[tempRowName] = loVariableBounds[variable]
        actualRowNames.append(tempRowName)

# for row in Lrows:
#     if row not in AMatrix:

# writing the Dual String
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

print('keys of Amatrix:', AMatrix.keys())

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
print("Printing RHS:")
for i in listOfVars:
    if AMatrix[objName].get(i):
        s += 4 * ' ' + objName + + (10 - len(objName)) * ' ' + i + (10 - len(i)) * ' ' + str(AMatrix[objName][i]) + '\n'

defaultBndName = 'B1'


if Lrows or Erows:
    s += "BOUNDS\n"
    for name in actualRowNames:
        print("row name being bounded", name)
        if name in Lrows:
            s += " " + "MI" + " " + defaultBndName + (10 - len(defaultBndName)) * ' ' + name + '\n'
            s += " " + "UP" + " " + defaultBndName + (10 - len(defaultBndName)) * ' ' + name + (10 - len(
                name)) * ' ' + '0' + '\n'
        if name in Erows:
            s += " " + "FR" + " " + defaultBndName + (10 - len(defaultBndName)) * ' ' + name + '\n'

s += "ENDATA\n"
fileNameOut = os.path.splitext(file_name)[0] + "Dual.mps"
print(fileNameOut)
with open(fileNameOut, "w") as text_file:
    text_file.write(s)
