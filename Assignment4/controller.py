from sensorList import *
from domain import *

class Controller:
    def __init__(self):
        self.__map = Map()
        self.__drone = Drone(0, 0)

        self.__placeDroneOnEmptyPos()

        self.__sensors = SensorList(self.__map)
        self.__pheromones = [[1.0 for _ in range(SENSOR_COUNT)] for _ in range(SENSOR_COUNT)]
        self.__distances = self.__sensors.getDistBetweenSensors()

    def __placeDroneOnEmptyPos(self):
        crtX, crtY = random.randint(0, MAP_HEIGHT), random.randint(0, MAP_WIDTH)
        while self.__map.getSurface()[crtX][crtY] == 1:
            crtX, crtY = random.randint(0, MAP_HEIGHT), random.randint(0, MAP_WIDTH)
        self.__drone.setCoords(crtX, crtY)

    def __moveAnts(self, ants, alpha, beta, q0):
        antLives = [True for _ in ants]
        for i in range(len(ants)):
            ant = ants[i]
            for step in range(SENSOR_COUNT-1):
                found = ant.nextMove(self.__distances, self.__pheromones, q0, alpha, beta)
                if not found:
                    antLives[i] = False
                    break

        aliveAnts=[]
        for i in range(len(ants)):
            if antLives[i]:
                ants[i].computeFitness(self.__distances)
                aliveAnts.append(ants[i])
        return aliveAnts

    def __selectBestAnt(self, ants):
        bestAnt = None
        bestFitness = INFINITY

        for ant in ants:
            if bestFitness > ant.getFitness():
                bestFitness = ant.getFitness()
                bestAnt = ant
        return bestAnt

    def __simulateEpoch(self, nrAnts, alpha, beta, q0, rho):
        ants = [Ant() for _ in range(nrAnts)]

        ants = self.__moveAnts(ants, alpha, beta, q0)

        for i in range(SENSOR_COUNT):
            for j in range(SENSOR_COUNT):
                self.__pheromones[i][j] = (1-rho)*self.__pheromones[i][j]

        if not ants:
            return None

        newPheromones = [1.0 / ant.getFitness() for ant in ants]
        for i in range(len(ants)):
            current = ants[i].getPath()
            for j in range(len(current)-1):
                currentSensor = current[j]
                nextSensor = current[j+1]
                self.__pheromones[currentSensor][nextSensor] += newPheromones[i]

        return self.__selectBestAnt(ants)

    def __chargeSensors(self, remainingBattery, accessibleSensors):
        sensors = []
        for i in range(len(self.__sensors.getSensorList())):
            if i in accessibleSensors:
                sensors.append(self.__sensors.getSensorList()[i])

        energyLevels = [0 for _ in sensors]
        if remainingBattery <= 0:
            return energyLevels

        sensors.sort(key=lambda s: (s.getAccessiblePositions()[-1] / s.getMaxEnergy()))
        i = 0
        while i < len(sensors) and remainingBattery > 0:
            currentSensorMaxEnergy = sensors[i].getMaxEnergy()
            if remainingBattery > currentSensorMaxEnergy:
                remainingBattery -= currentSensorMaxEnergy
                energyLevels[i] = currentSensorMaxEnergy
            else:
                energyLevels[i] = remainingBattery
                remainingBattery = 0
            i += 1
        return energyLevels

    def __updateBestSolution(self, bestSolution):
        currentSolution = self.__simulateEpoch(ANT_COUNT, ALPHA, BETA, Q0, RHO)
        if currentSolution is None:
            return bestSolution

        currentSolutionPathLength = len(currentSolution.getPath())
        if bestSolution is None or currentSolutionPathLength > len(bestSolution.getPath()) \
                or (currentSolutionPathLength == len(bestSolution.getPath()) and currentSolution.getFitness() < bestSolution.getFitness()):
            return currentSolution  # new best solution
        return bestSolution

    def run(self):
        bestSolution = None  # will be the one with the lowest cost path

        print("Starting")
        for epoch in range(EPOCH_COUNT):
            bestSolution = self.__updateBestSolution(bestSolution)

        energyLevels = self.__chargeSensors(BATTERY - bestSolution.getFitness(),bestSolution.getPath())
        print("Best path: ")
        for indices in bestSolution.getPath():
            print(self.__sensors.getSensorList()[indices].getCoords(), end=" ")
        print("\nEnergy in each sensor: ", energyLevels)

    def getMap(self):
        return self.__map

    def setMap(self, dmap):
        self.__map = dmap

    def getMapSurface(self):
        return self.__map.getSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()