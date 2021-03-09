import pygame
from Domain.Constants import *
from Controller import *
from random import randint
import time


class GUI:
    def __init__(self):
        # we position the drone somewhere in the area
        x = randint(STARTAREA, ENDAREA)
        y = randint(STARTAREA, ENDAREA)
        self.__controller = Controller(x, y)

    def __initializeGame(self):
        # initialize the pygame module
        pygame.init()

        # load and set the logo
        logo = pygame.image.load("pirate.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Pirates of the Caribbean")

        #add music
        pygame.mixer.init()
        pygame.mixer.music.load("theme.mp3")
        pygame.mixer.music.play(PLAYLOOP,PLAYSTART)

    def __setInitialScreen(self):
        screen = pygame.display.set_mode(STARTWINDOW)
        screen.fill(PALEBLUE)
        #add font
        pygame.font.init()
        font = pygame.font.SysFont('calibri.ttf', STARTFONT)
        img = font.render('Let\'s explore!', True, DARKBLUE)
        #draw the button
        pygame.draw.rect(screen, WHITE, BUTTONPOSITION, border_radius=BORDER)
        pygame.draw.rect(screen, BLACK, BUTTONPOSITION, BUTTONWIDTH, border_radius=BORDER)
        screen.blit(img, STARTFONTBLIT)
        pygame.display.flip()
        return screen


    def __setMainScreen(self):
        #initialize the main screen
        screen = pygame.display.set_mode(MAINWINDOW)
        screen.fill(WHITE)
        screen.blit(self.__controller.getEnvironment().image(), FULLBLIT)
        pygame.display.flip()
        return screen

    def __setEndScreen(self):
        screen = pygame.display.set_mode(MAINWINDOW)
        screen.fill(WHITE)
        #add background image
        bg = pygame.image.load("final.jpg")
        screen.blit(bg,FULLBLIT)
        #add font
        font = pygame.font.SysFont("calibri.ttf",ENDFONT)
        img = font.render('Congratulations, pirate!', True, DARKBLUE)
        screen.blit(img,ENDFONTBLIT)
        pygame.display.flip()
        return screen


    def start(self):
        self.__initializeGame()
        screen = self.__setInitialScreen()
        # define variables to control each window loop
        start = True
        running = False
        endscreen = False

        # initial screen
        while start:
            for event in pygame.event.get():
                # handle quit event
                if event.type == pygame.QUIT:
                    # exit game
                    start = False
                # handle button pressed event
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if STARTBUTTON <= pygame.mouse.get_pos()[WIDTH] <= ENDBUTTONWIDTH:
                        if STARTBUTTON <= pygame.mouse.get_pos()[HEIGHT] <= ENDBUTTONHEIGHT:
                            # set main screen, exit this loop and enter main loop
                            screen = self.__setMainScreen()
                            running = True
                            start = False


        # main loop
        while running:
            for event in pygame.event.get():
                # handle quit event
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            # move one step using DFS
            self.__controller.moveDFS()
            time.sleep(SLEEP)

            # stop main window execution when the stack is empty and enter the end screen
            if self.__controller.getDroneX() is None:
                running = False
                endscreen = True
            else:
                self.__controller.markDetectedWalls()
                screen.blit(self.__controller.getMapImage(), MAPBLIT)
                pygame.display.flip()

        # enter end screen
        while endscreen:
            screen = self.__setEndScreen()
            for event in pygame.event.get():
                # handle quit event
                if event.type == pygame.QUIT:
                    endscreen = False

        pygame.quit()
