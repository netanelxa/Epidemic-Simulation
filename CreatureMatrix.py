import numpy as np
import random
from itertools import product, starmap


class MyPosition:
    # exact values for position in Matrix
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Creatures:
    def __init__(self, position, health, ID):
        self.position = position
        self.health = health
        self.ID = ID


# constructor - dim is the matrix size
# numofHealthy - number of healthy creatures
# numofInfected - number of infected creatures
# randomly fix on matrix
class matrixHandler:
    def __init__(self, dim, numofHealthy, numofInfected, probToInfect, k,theNewk ,ChangeKAfter):
        self.stepsCounter = 0
        self.k = k
        self.theNewk = theNewk
        self.ChangeKAfter = ChangeKAfter
        self.dim = dim
        self.creaturesTable = {}
        self.probToInfect = probToInfect
        self.matrix = np.zeros((dim, dim), "uint8")
        for i in range(numofHealthy):
            newPoint = MyPosition(random.randint(0, dim - 1), random.randint(0, dim - 1))
            self.creaturesTable[i] = Creatures(newPoint, 2, i)
            self.matrix[newPoint.x, newPoint.y] = 2
        for i in range(numofInfected):
            newPoint = MyPosition(random.randint(0, dim - 1), random.randint(0, dim - 1))
            self.creaturesTable[i + numofHealthy] = Creatures(newPoint, 3, i)
            self.matrix[newPoint.x, newPoint.y] = 3
        print("Creatures Created")

    # Checking if the new position is empty
    # if the new position is out of the border - continue in the other side
    def isEmpty(self, matrix, position):
        if position.x < 0:
            position.x = matrix.shape[1] - 1
        if position.y < 0:
            position.y = matrix.shape[0] - 1
        if position.x == matrix.shape[0]:
            position.x = 0
        if position.y == matrix.shape[1]:
            position.y = 0
        if matrix[position.x, position.y] == 0:
            return True

    # updating the matrix after movement
    def updateMatrix(self, positionsMatrix, oldPosition, newPosition, HealthStatus):
        positionsMatrix[oldPosition.x, oldPosition.y] = 0
        positionsMatrix[newPosition.x, newPosition.y] = HealthStatus

    def updateDict(self, ID, newPosition):
        self.creaturesTable[ID].position = newPosition

    # if the new position is empty - randomly moving one step
    def moveOneStep(self, ID, cell, healthStatus):
        counter = 0
        while True:
            randNum = random.randint(1, 9)
            cell = MyPosition(cell.x, cell.y)
            if randNum == 1:
                newPosition = MyPosition(cell.x - 1, cell.y - 1)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 2:
                newPosition = MyPosition(cell.x, cell.y - 1)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 3:
                newPosition = MyPosition(cell.x + 1, cell.y - 1)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 4:
                newPosition = MyPosition(cell.x - 1, cell.y)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 5:
                newPosition = MyPosition(cell.x, cell.y)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 6:
                newPosition = MyPosition(cell.x + 1, cell.y)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 7:
                newPosition = MyPosition(cell.x - 1, cell.y + 1)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    #    self.updatePositionsToIDdict(cell, newPosition,randNum)
                    break
            elif randNum == 8:
                newPosition = MyPosition(cell.x, cell.y + 1)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break
            elif randNum == 9:
                newPosition = MyPosition(cell.x + 1, cell.y + 1)
                if self.isEmpty(self.matrix, newPosition):
                    self.updateMatrix(self.matrix, cell, newPosition, healthStatus)
                    self.updateDict(ID, newPosition)
                    break

            counter += 1
            if counter > 20:
                # print("cant move")
                break

    def setK(self, newK):
        print("K has change from " + str(self.k) + " To " + str(newK))
        self.k = newK

    # activate moveOneStep function for each living creature
    def moveAllOneStep(self):
        self.stepsCounter += 1
        if self.stepsCounter == self.ChangeKAfter:
            self.setK(self.theNewk)
        for x in self.creaturesTable:
            self.moveOneStep(x, self.creaturesTable[x].position, self.creaturesTable[x].health)
        self.Infect()
        x = []
        y = []
        for c in self.creaturesTable:
            if self.creaturesTable[c].health == 2:
                x.append([self.creaturesTable[c].position.x, self.creaturesTable[c].position.y])
            elif self.creaturesTable[c].health == 3:
                y.append([self.creaturesTable[c].position.x, self.creaturesTable[c].position.y])
        return x, y

    # returning list with the active neighbors
    def getNeighbors(self, positionsMatrix, currentPosition):
        a = currentPosition
        cells = starmap(lambda a, b: (currentPosition.x + a, currentPosition.y + b), product((0, -1, +1), (0, -1, +1)))
        nlist = []
        NeighborsList = list(cells)
        NeighborsList.remove(NeighborsList[0])
        for x in NeighborsList:
            a = list(x)
            if a[0] < 0:
                a[0] = self.matrix.shape[1] - 1
                x = tuple(a)
            if a[1] < 0:
                a[1] = self.matrix.shape[0] - 1
                x = tuple(a)
            if a[0] == self.matrix.shape[0]:
                a[0] = 0
                x = tuple(a)
            if a[1] == self.matrix.shape[1]:
                a[1] = 0
                x = tuple(a)
            if positionsMatrix[x] != 0:
                nlist.append(x)
        return nlist

    def kIsolation(self, currentposition, neighborlist, k):
        nlist = neighborlist.copy()
        a = self.matrix.shape[1] - 1
        mytupleposition = tuple((currentposition.x, currentposition.y))
        for x in neighborlist:
            if ((mytupleposition[0] - 1 == x[0] or mytupleposition[0] - 1 < 0) and (
                    mytupleposition[1] - 1 == x[1] or mytupleposition[1] - 1 < 0)) and k > 7:
                nlist.remove(x)
            elif ((mytupleposition[0] - 1 == x[0] or mytupleposition[0] - 1 < 0) and mytupleposition[1] == x[
                1]) and k > 6:
                nlist.remove(x)
            elif ((mytupleposition[0] - 1 == x[0] or mytupleposition[0] - 1 < 0) and (mytupleposition[1] + 1 == x[
                1] or mytupleposition[1] + 1 > self.matrix.shape[1] - 1)) and k > 5:
                nlist.remove(x)
            elif (mytupleposition[0] == x[0] and (
                    mytupleposition[1] + 1 == x[1] or mytupleposition[1] + 1 > self.matrix.shape[0] - 1)) and k > 4:
                nlist.remove(x)
            elif ((mytupleposition[0] + 1 == x[0] or mytupleposition[0] + 1 > self.matrix.shape[0] - 1) and (
                    mytupleposition[1] + 1 == x[1] or mytupleposition[1] + 1 > self.matrix.shape[1] - 1)) and k > 3:
                nlist.remove(x)
            elif ((mytupleposition[0] + 1 == x[0] or mytupleposition[0] + 1 > self.matrix.shape[0] - 1) and
                  mytupleposition[1] == x[1]) and k > 2:
                nlist.remove(x)
            elif ((mytupleposition[0] + 1 == x[0] or mytupleposition[0] + 1 > self.matrix.shape[0] - 1) and (
                    mytupleposition[1] - 1 == x[1] or mytupleposition[1] - 1 < 0)) and k > 1:
                nlist.remove(x)
            elif (mytupleposition[0] == x[0] and (
                    mytupleposition[1] - 1 == x[1] or mytupleposition[1] - 1 < 0)) and k > 0:
                nlist.remove(x)
        return nlist

    # returning num of infected
    def getNumOfInfected(self):
        return np.count_nonzero(self.matrix == 3)

    def getNumOfHealthy(self):
        return np.count_nonzero(self.matrix == 2)

    def getNeighborID(self, position):
        a = position
        for x in self.creaturesTable:
            b = tuple((self.creaturesTable[x].position.x, self.creaturesTable[x].position.y))
            if b == position:
                return self.creaturesTable[x].ID

    # choose one of the neighbors and infect him
    # p is the probability choosing infect
    def Infect(self):
        # vector from 1 to p
        vector = list(range(1, self.probToInfect + 1))
        # iterating over all creatures, healthy and infected
        for x in self.creaturesTable:
            # if the creature is infected - can infect
            if self.creaturesTable[x].health == 3:
                # all the living neighbors
                neighborsList = self.getNeighbors(self.matrix, self.creaturesTable[x].position)
                if self.k > 0 and len(neighborsList) > 0:
                    neighborsList = self.kIsolation(self.creaturesTable[x].position, neighborsList, self.k)
                # y= tuple of neighbor position (x,y) of neighbor in tuple
                for y in neighborsList:
                    randNum = random.randint(1, 100)
                    if randNum in vector:
                        # infect the neighbor
                        self.matrix[y] = 3
                        try:
                            NeighborID = self.getNeighborID(y)
                            if NeighborID not in self.creaturesTable.keys():
                                print("Not in keys")
                            self.creaturesTable[NeighborID].health = 3
                        except:
                            print("Not in list")
