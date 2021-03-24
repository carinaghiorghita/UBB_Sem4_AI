import pygame,time
from pygame.locals import *
from random import randint

from Domain.Constants import *
from Controller import Controller

class GUI:
    def __init__(self):
        # we position the drone somewhere in the area
        self.__initialX = randint(STARTAREA, ENDAREA)
        self.__initialY = randint(STARTAREA, ENDAREA)
        # get final coordinates for the drone
        self.__finalX = randint(STARTAREA, ENDAREA)
        self.__finalY = randint(STARTAREA, ENDAREA)
        self.__controller = Controller(self.__initialX, self.__initialY)

    def start(self):

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((1200, 400))
        screen.fill(WHITE)

        #check whether the end point is a wall
        while self.__controller.getMap().surface[self.__finalX][self.__finalY]==1:
            self.__finalX = randint(STARTAREA, ENDAREA)
            self.__finalY = randint(STARTAREA, ENDAREA)

        print('Start: ('+str(self.__initialX)+', '+str(self.__initialY)+')')
        print('End: ('+str(self.__finalX)+', '+str(self.__finalY)+')')

        # define a variable to control the main loop
        running = True

        #variable for printing path
        printedTime = False
        printedG = False
        printedA = False
        printedU = False

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            startG = time.time()
            pathG = self.__controller.searchGreedy(self.__initialX,self.__initialY,self.__finalX,self.__finalY)
            endG = time.time()
            if len(pathG) == 0:
                print('Path does not exist.')
                return
            
            if not printedG:
                print('Greedy Path: ')
                print(pathG)
                printedG = True
            screen.blit(self.__controller.displayWithPath(self.__controller.getMap().image(BLUE), pathG, PALEBLUE), (0, 0))

            startA = time.time()
            pathA = self.__controller.searchAStar(self.__initialX,self.__initialY,self.__finalX,self.__finalY)
            endA = time.time()
            if not printedA:
                print('A* Path: ')
                print(pathA)
                printedA = True
            screen.blit(self.__controller.displayWithPath(self.__controller.getMap().image(RED), pathA, PALEORANGE), (400, 0))

            startU = time.time()
            pathU = self.__controller.searchUniformCost(self.__initialX,self.__initialY,self.__finalX,self.__finalY)
            endU = time.time()
            if not printedU:
                print('Uniform Cost Path: ')
                print(pathU)
                printedU = True
            screen.blit(self.__controller.displayWithPath(self.__controller.getMap().image(DARKGREEN), pathU, PALEGREEN), (800, 0))

            if not printedTime:
                print('\nExecution time for Greedy: '+str(endG-startG))
                print('Execution time for A*: '+str(endA-startA))
                print('Execution time for Uniform Cost Search: '+str(endU-startU))
                printedTime = True
            pygame.display.flip()
        pygame.quit()
