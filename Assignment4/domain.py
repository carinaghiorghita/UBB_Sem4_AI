import random
from const import *

import numpy as np

class Drone:
    def __init__(self,x ,y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setCoords(self, x, y):
        self.__x = x
        self.__y = y


class Map:
    def __init__(self):
        self.surface = np.zeros((MAP_HEIGHT, MAP_WIDTH))
        self.randomMap()

    def randomMap(self, fill=0.2):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if random.random() <= fill:
                    self.surface[i][j] = 1

    def setValueOnPos(self, x, y, val):
        self.surface[x][y] = val

    def __str__(self):
        string = ""
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def getSurface(self):
        return self.surface


class Sensor:
    def __init__(self, x, y, dmap):
        #self.__x = randint(0,MAP_HEIGHT)
        #self.__y = randint(0,MAP_WIDTH)
        self.__x = x
        self.__y = y
        self.__accPositions = [0 for _ in range(6)]
        self.__map = dmap
        self.__maxEnergyLevel = 0

    def validCoord(self, x, y):
        return -1 < x < MAP_HEIGHT and -1 < y < MAP_WIDTH and self.__map.getSurface()[x][y] != 1

    def detectMaxEnergy(self):
        blocked = [False for _ in range(4)]

        # energy value between 1-5
        for i in range(1, 6):
            self.__accPositions[i] = self.__accPositions[i-1]
            for d in range(4):
                if not blocked[d]:
                    newX = self.__x + dir[d][0]*i
                    newY = self.__y + dir[d][1]*i
                    if self.validCoord(newX, newY):
                        self.__accPositions[i] += 1
                    else:
                        blocked[d] = True

    def computeMaxEnergyLevel(self):
        for energy in range(5):
            if self.__accPositions[energy] == self.__accPositions[energy + 1]:
                self.__maxEnergyLevel = energy
                return
        self.__maxEnergyLevel = 5

    def getMaxEnergy(self):
        return self.__maxEnergyLevel

    def getAccessiblePositions(self):
        return self.__accPositions

    def getCoords(self):
        coord = (self.__x, self.__y)
        return coord

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

class Ant:
    def __init__(self):
        self.__size = SENSOR_COUNT
        self.__path = [random.randint(0, SENSOR_COUNT - 1)]
        self.__fitness = 0
        self.__battery = BATTERY


    def __getPossibleMoves(self, distances):
        #distances is a table containing distances from one sensor to another
        moves = []
        #for sensors, we will work with indexes
        currentSensor = self.__path[-1]

        for nextSensor in range(SENSOR_COUNT):
            if nextSensor != currentSensor and distances[currentSensor][nextSensor] != INFINITY and\
                    nextSensor not in self.__path and self.__battery >= distances[currentSensor][nextSensor]:
                moves.append(nextSensor)
        return moves

    def __computeProbabilityOfChoosingNextSensor(self, moves, alpha, beta, distances, pheromones):
        currentSensor = self.__path[-1]
        nextSensorProb = [0 for _ in range(SENSOR_COUNT)]

        for i in moves:
            distanceNextSensor = distances[currentSensor][i]
            pheromoneNextSensor = pheromones[currentSensor][i]
            prob = (distanceNextSensor ** beta) * (pheromoneNextSensor ** alpha)
            nextSensorProb[i] = prob

        return nextSensorProb

    def nextMove(self, distances, pheromones, q0, alpha, beta):
        # q0 = probability that the ant chooses the best possible move
        moves = self.__getPossibleMoves(distances)
        if not moves:
            return False  # the move wasn't completed successfully

        nextNodeProb = self.__computeProbabilityOfChoosingNextSensor(moves, alpha, beta, distances, pheromones)
        if random.random() < q0:
            bestProb = max(nextNodeProb)
            selectedNode = nextNodeProb.index(bestProb)
        else:
            selectedNode = self.__roulette(nextNodeProb)

        self.__battery -= distances[self.__path[-1]][selectedNode]
        self.__path.append(selectedNode)

        return True

    def __roulette(self, nextNodeProb):
        probSum = sum(nextNodeProb)

        if probSum == 0:
            return random.randint(0, len(nextNodeProb) - 1)

        pSum = [nextNodeProb[0] / probSum]
        for i in range(1, len(nextNodeProb)):
            pSum.append(pSum[i - 1] + nextNodeProb[i] / probSum)

        r = random.random()
        position = 0
        while r > pSum[position]:
            position += 1
        return position

    def computeFitness(self, distances):
        length = 0
        for i in range(1, len(self.__path)):
            length += distances[self.__path[i-1]][self.__path[i]]

        self.__fitness = length

    def getFitness(self):
        return self.__fitness

    def getPath(self):
        return self.__path

    def getBattery(self):
        return self.__battery