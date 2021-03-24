import pygame

from Domain.Map import Map
from Domain.Drone import Drone
from Domain.Constants import *

class Controller:
    def __init__(self,x,y):
        self.__map=Map()
        self.__drone=Drone(x,y)

    def getMap(self):
        return self.__map

    def getDrone(self):
        return self.__drone

    def getDroneX(self):
        return self.__drone.getX()

    def getDroneY(self):
        return self.__drone.getY()

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.__drone.x > 0:
            if pressed_keys[pygame.K_UP] and self.__map.surface[self.__drone.x - 1][self.__drone.y] == 0:
                self.__drone.x = self.__drone.x - 1
        if self.__drone.x < 19:
            if pressed_keys[pygame.K_DOWN] and self.__map.surface[self.__drone.x + 1][self.__drone.y] == 0:
                self.__drone.x = self.__drone.x + 1

        if self.__drone.y > 0:
            if pressed_keys[pygame.K_LEFT] and self.__map.surface[self.__drone.x][self.__drone.y - 1] == 0:
                self.__drone.y = self.__drone.y - 1
        if self.__drone.y < 19:
            if pressed_keys[pygame.K_RIGHT] and self.__map.surface[self.__drone.x][self.__drone.y + 1] == 0:
                self.__drone.y = self.__drone.y + 1

    def heuristicManhattanDist(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def validNode(self, x, y):
        return -1 < x < 20 and -1 < y < 20 and self.__map.surface[x][y] == 0

    def buildPath(self, prev, finalX, finalY):
        path = [(finalX, finalY)]
        coord = prev[(finalX, finalY)]
        while coord != (None, None):
            path.append(coord)
            coord = prev[coord]
        path.reverse()
        return path

    def searchAStar(self, initialX, initialY, finalX, finalY):
        found = False
        visited = []
        visitQueue = [(initialX,initialY)]
        prev = dict()
        prev[(initialX,initialY)] = (None, None)
        nrSteps = dict()
        nrSteps[(initialX, initialY)] = 0

        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)

            if node==(finalX, finalY):
                found = True
            else:
                aux = []
                for d in directions:
                    newX = node[0] + d[0]
                    newY = node[1] + d[1]

                    if self.validNode(newX, newY) and (newX,newY) not in visited:
                        if (newX,newY) not in visitQueue:
                            aux.append((newX, newY))
                            prev[(newX,newY)] = node
                            nrSteps[(newX,newY)] = nrSteps[node] + 1
                        else:
                            if nrSteps[(newX, newY)] > nrSteps[node] + 1:
                                visitQueue.remove((newX,newY))
                                aux.append((newX, newY))
                                prev[(newX,newY)] = node
                                nrSteps[(newX, newY)] = nrSteps[node] + 1

                visitQueue.extend(aux)
                visitQueue.sort(key=lambda coord: self.heuristicManhattanDist(coord[0],coord[1],finalX,finalY) + nrSteps[coord])

        if found:
            return self.buildPath(prev, finalX, finalY)
        else:
            return []


    def searchGreedy(self, initialX, initialY, finalX, finalY):
        found = False
        visited = []
        prev = dict()
        prev[(initialX,initialY)] = (None, None)
        visitQueue = [(initialX,initialY)]

        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)

            if node==(finalX, finalY):
                found = True
            else:
                aux = []
                for d in directions:
                    newX = node[0]+d[0]
                    newY = node[1]+d[1]

                    if self.validNode(newX, newY) and (newX,newY) not in visited:
                        aux.append((newX, newY))
                        prev[(newX,newY)] = node
                visitQueue.extend(aux)
                visitQueue.sort(key=lambda coord: self.heuristicManhattanDist(coord[0],coord[1],finalX,finalY))

        if found:
            return self.buildPath(prev, finalX, finalY)
        else:
            return []

    def searchUniformCost(self, initialX, initialY, finalX, finalY):
        found = False
        visited = []
        prev = dict()
        prev[(initialX,initialY)] = (None, None)
        visitQueue = [(initialX,initialY)]
        cost = dict()
        cost[(initialX,initialY)] = 0

        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)

            if node==(finalX, finalY):
                found = True
            else:
                aux = []
                for d in directions:
                    newX = node[0]+d[0]
                    newY = node[1]+d[1]

                    if self.validNode(newX, newY) and (newX, newY) not in visited:
                        aux.append((newX, newY))
                        prev[(newX, newY)] = node
                        cost[(newX, newY)] = cost[node] + 1
                visitQueue.extend(aux)
                visitQueue.sort(key=lambda coord: cost[coord])

        if found:
            return self.buildPath(prev, finalX, finalY)
        else:
            return []

    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]

    def displayWithPath(self, imagee, path, color):
        mark = pygame.Surface((20, 20))
        mark.fill(color)
        for move in path:
            imagee.blit(mark, (move[1] * 20, move[0] * 20))

        return imagee

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.getDroneY() * 20, self.getDroneX() * 20))

        return mapImage

