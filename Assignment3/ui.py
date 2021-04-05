# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from domain import *
import matplotlib.pyplot as plot


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes through walls

class UI:
    def __init__(self):
        self.__controller = controller()
        self.__bestIndividuals = []
        #popSize=50, indSize=30, genCount=20, nrIterations=100
        self.__popSize = 50
        self.__indSize = 30
        self.__genCount = 20
        self.__nrIterations = 100

    def __printMenu(self):
        print("\n1. Map options")
        print("2. EA options")
        print("0. Exit")

    def __printMenuMap(self):
        print("\nMap options:")
        print("1. Generate random map")
        print("2. Load map")
        print("3. Save map")
        print("4. Visualize map")
        print("0. Exit")

    def __printMenuEA(self):
        print("\nEA options:")
        print("1. Parameters setup")
        print("2. Run the solver")
        print("3. View the drone moving on a path")
        print("0. Exit")

    def plotGraph(self, solutionAverages):
        plot.plot(solutionAverages)
        plot.savefig("solutionAverageFitness.png")

    def logToFile(self, solutionAverages, lastSeed=30, populationSize=50, individualSize=30, generationCount=30,
                  numberIterations=50):
        logFile = open("results.txt", "a")
        logFile.write("Seeds = [%d, %d]; " % (1, lastSeed))
        logFile.write(
            "Pop.size = %d; Ind.size = %d; Generations = %d; " % (populationSize, individualSize, generationCount))
        logFile.write(
            "Iterations/gen = %d; Mutation prob = %.2f; Crossover prob = %.2f\n" % (numberIterations, 0.04, 0.8))
        logFile.write("Average of averages: %.3f\n" % np.average(solutionAverages))
        logFile.write("Stdev of averages: %.3f\n" % np.std(solutionAverages))
        logFile.write("\n")
        logFile.close()

    def runMap(self):
        newMap = Map()
        while True:
            self.__printMenuMap()
            mapOption = input("Your option: ")

            if mapOption == "1":
                newMap.randomMap()
                print("Map successfully generated!\n")

            elif mapOption == "2":
                mapName = input("Enter the map filename: ")
                newMap.loadMap(mapName)
                print("Map successfully loaded!\n")

            elif mapOption == "3":
                mapName = input("Enter the map filename: ")
                newMap.saveMap(mapName)
                print("Map successfully saved!\n")

            elif mapOption == "4":
                print(newMap)

            elif mapOption == "0":
                break

            else:
                print("Invalid command.\n")

        self.__controller.setMap(newMap)

    def runEA(self):
        while True:
            self.__printMenuEA()
            eaOption = input("Your option: ")

            if eaOption == "1":
                self.__popSize = input("Population size: ")
                self.__indSize = input("Number of individuals: ")
                self.__genCount = input("Number of generations: ")
                self.__nrIterations = input("Number of iterations: ")

            elif eaOption == "2":
                bestIndividuals, averages = self.__controller.solver(self.__popSize, self.__indSize, self.__genCount, self.__nrIterations)
                bestIndividuals.sort(key=lambda e: e.getFitness(), reverse=True)
                self.__bestIndividuals = bestIndividuals[:3]
                self.plotGraph(averages)
                self.logToFile(averages)

            elif eaOption == "3":
                screen = initPyGame((400, 400))
                movingDrone(screen, self.__controller, self.__bestIndividuals)
                closePyGame()

            elif eaOption == "0":
                break

            else:
                print("Invalid command.\n")

    def run(self):
        while True:
            self.__printMenu()
            option = input("Your option: ")

            if option == "1":
                self.runMap()
            elif option == "2":
                self.runEA()
            elif option == "0":
                break
            else:
                print("Invalid command.\n")
