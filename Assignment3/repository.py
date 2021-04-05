# -*- coding: utf-8 -*-

import pickle
from domain import *


class repository():
    def __init__(self):
        self.__populations = []
        self.__dmap = Map()
        self.__drone = Drone(rand.randint(0,19), rand.randint(0,19))
        #self.createPopulation()
        
    def createPopulation(self):
        # args = [populationSize, individualSize] -- you can add more args    
        self.__populations.append(Population(self.__drone, self.__dmap))

    def getPopulations(self):
        return self.__populations

    def setLastPopulation(self, population):
        self.__populations[-1]=population

    def addPopulation(self, population):
        self.__populations.append(population)
        
    def load_random_map(self):
        self.__dmap.randomMap()

    def getMap(self):
        return self.__dmap

    def getDrone(self):
        return self.__drone

    def setMap(self,newMap):
        self.__dmap = newMap