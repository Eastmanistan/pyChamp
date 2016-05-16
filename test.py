background_image_filename = 'Assets/night1.jpg'
mouse_image_filename = 'Assets/rocky_run_1.png'
import pygame
from pygame.locals import *
from sys import exit
import sys
import datetime
import math
import time
FPS = 30
frameDelay = (float(1)/FPS)
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Hello, World!")
background = pygame.image.load(background_image_filename).convert()
mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()
startTime = datetime.datetime.now()
frame = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))
    print screen
    currentTime = datetime.datetime.now()
    deltaTime = (startTime - currentTime)
    currentFrame = ((deltaTime.total_seconds()) % 10) + 1
    mouse_cursor = pygame.image.load('Assets/rocky_run_' + str((frame % 10) + 1) + '.png').convert_alpha()
    x = (frame * 3) % 640
    screen.blit(mouse_cursor, (x, 300))
    pygame.display.update()
    time.sleep(frameDelay)
    frame += 1



