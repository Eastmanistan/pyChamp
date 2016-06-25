import pygame
import stepCounter
from pygame.locals import *
from sys import exit
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
import engine

x, y = 0, 0
move_x, move_y = 0, 0
gameEngine = engine.Engine(screen)
player = engine.Runner({'default': ('Assets/rocky_run_.png', 10) })
player2 = engine.Runner({'default': ('Assets/rocky_run_.png', 10) })
#background = engine.GameSprite({'default': ('Assets/night.jpg', 1)})
firstScene = engine.Scene(False, {player2:(100,400), player: (0,300)})
pygame.event.clear()
gameEngine.run(firstScene)





