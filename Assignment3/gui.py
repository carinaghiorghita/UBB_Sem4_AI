# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from pygame.locals import *
import pygame, time
from utils import *
from domain import *

def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()
    

def movingDrone(screen, controller, bestIndividuals, speed = 1,  markSeen = True):
    # animation of a drone on a path

    for individual in bestIndividuals:
        imagee = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        pathTile = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagee.fill(WHITE)
        pathTile.fill(GREEN)

        mapSurface = controller.getMap().surface
        for i in range(20):
            for j in range(20):
                if mapSurface[i][j] == 1:
                    imagee.blit(brick, (j * 20, i * 20))

        drona = pygame.image.load("drona.png")
        imagee.blit(drona, (controller.getDrone().getY() * 20, controller.getDrone().getX() * 20))

        crtPosition = (controller.getDrone().getX(), controller.getDrone().getY())

        path = individual.getChromosome()
        for directionCode in path:
            imagee.blit(pathTile, (crtPosition[1] * 20, crtPosition[0] * 20))
            pathImageCopy = imagee.copy()
            pathImageCopy.blit(drona, (crtPosition[1] * 20, crtPosition[0] * 20))
            screen.blit(pathImageCopy, (0, 0))
            pygame.display.update()
            pygame.time.wait(5)
            direction = v[directionCode]
            crtPosition = (crtPosition[0] + direction[0], crtPosition[1] + direction[1])


def image(currentMap, colour = BLUE, background = WHITE):
    # creates the image of a map
    
    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20,20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, ( j * 20, i * 20))
                
    return imagine        
