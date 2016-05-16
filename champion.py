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
background = engine.GameSprite({'default': ('Assets/night.jpg', 1)})
firstScene = engine.Scene(False, {player: (0,0), background: (0,0)})
gameEngine.run(firstScene)





