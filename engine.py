import pygame
import sys
import time
from pygame.locals import *
background_image_filename = 'Assets/night1.jpg'
mouse_image_filename = 'Assets/rocky_run_1.png'
background = pygame.image.load(background_image_filename).convert()
mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()

FPS = 30

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, aniStatesDict):  #aniStatesDict is a dicionary of animation states to base filenames
        pygame.sprite.Sprite.__init__(self)
        self.currentFrame = 0
        self.aniState = 'default'
        self.aniDict = buildAniDict(aniStatesDict)
        self.velocity = {'x': 0 , 'y': 0}
       # self.colliderDict = buildColliderDict(self.aniDict)  #dunno if actually need this?  probably now
        self.zIndex = 0
        self.finished = False
        self.image = self.aniDict[self.aniState][self.currentFrame]
        self.rect = self.image.get_rect()
        self.gravity = False






    def setAniState(self, newState):
        self.aniState = newState
        self.currentFrame = 0

    def setLocation(self, loc):
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def getLoc(self):
        return (self.rect.x, self.rect.y)

    def move(self):
        self.rect.x += self.getVelocity()['x']
        self.rect.y += self.getVelocity()['y']

    def nextFrame(self):
        self.currentFrame += 1
        if self.currentFrame >= len(self.aniDict[self.aniState]):
            self.currentFrame = 0
        self.image = self.aniDict[self.aniState][self.currentFrame]

    def update(self):
        self.nextFrame()
        self.move()

    def setVelocity(self, vel):
        self.velocity['x'] = vel[0]
        self.velocity['y'] = vel[1]

    def getVelocity(self):
        return self.velocity




class SpritePool(object):  #for obstacles
    def __init__(self, *sprites):
        self.sprites = [sprites[x] for x in range(len(sprites))]


class Runner(GameSprite):
    def __init__(self, imgDict):
        GameSprite.__init__(self, imgDict)
        self.setVelocity((1,0))

    def jump(self):

        self.setVelocity((1, -10))
        self.gravity = True
        #self.setAniState('jump')


    def update(self):
        if self.gravity:
            y = self.getVelocity()['y']
            self.setVelocity((1, y+1))
            if self.rect.top >= 300:
                self.gravity = False
                self.rect.top = 300
                self.setVelocity((1,0))
        else:
            for event in pygame.event.get(KEYDOWN):
                if event.key == K_SPACE:
                    self.jump()
        self.nextFrame()
        self.move()



class TextBubble(pygame.sprite.Sprite):
    def __init__(self, text):
        self.text = text
        self.size = 0 # build size function based on length of text

class Pushup(GameSprite):
    def __init__(self, imgDict):
        GameSprite.__init__(self, imgDict)

    def update(self):
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_SPACE:
                self.setAniState('pushUp')



class Trainer(GameSprite):
    def __init__(self, imgDict):
        GameSprite.__init__(self, imgDict)

    def talk(self,text):
        pass


"""
Background may not need their own class
class Background(pygame.sprite.Sprite):
    def __init__(self, surface, parallax):
        self.image = surface
        self.parallax = parallax
"""

"""
spriteLocationDict example
{GameSprite(anidict: (0,0)}
"""
class Scene(object):
    def __init__(self, next, spriteLocationDict):
        self.sprites = buildGroup(*spriteLocationDict.keys())
        self.nextScene = next
        self.startingLocations = spriteLocationDict
        self.done = False

    # moves each sprite to the correct starting position
    def setup(self):
        for sprite in self.sprites:
            sprite.setLocation(self.startingLocations[sprite])

    def addSprite(self, sprite):
        self.sprites.add(sprite)

    def deleteSprite(self, sprite):
        self.sprites.remove(sprite)

    def checkFinished(self):
        for sprite in self.sprites:
            if sprite.finished:
                self.done = True

    def draw(self, screen):
        for sprite in self.sprites:
            screen.blit(sprite.image, sprite.getLoc())



class Engine(object):
    def __init__(self, screen):
        self.currentScene = False
        self.screen = screen


    def newScene(self, scene): #resets with new scene
        self.currentScene = scene

    def checkCollision(self, sprite1, sprite2):
        pass

    def run(self, scene):
        self.currentScene = scene
        scene.setup()
        while not scene.done:

            for sprite in scene.sprites:
                sprite.update() #this is where unique sprite behavior goes
            scene.draw(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            time.sleep((float(1) / FPS))

            scene.checkFinished()
        if bool(scene.nextScene):
            self.run(scene.nextScene)
        exit()



def buildGroup(*sprites):
    spriteList = list(sprites)
    group = pygame.sprite.OrderedUpdates()
    spriteList.sort(key=lambda x: x.zIndex)
    for index in range(len(spriteList)):
        group.add(spriteList[index])
    return group

def buildImgAnimation(fileLengthTuple):
    aniList = []
    for i in range(fileLengthTuple[1]):
        aniList.append(pygame.image.load(fileLengthTuple[0][0:-4] + str(i + 1)+fileLengthTuple[0][-4:]).convert_alpha())
    return aniList

"""
sample animationStateDict:
dict = {'default': ('Assets/runnerIdle', 4)}
default is the name of the state,
Assets/runnerIdle is the base file name
4 is the number of frames in the animation
"""
def buildAniDict(animationStatesDict):
    aniDict = {}
    for key in animationStatesDict:
        aniDict[key] = buildImgAnimation(animationStatesDict[key])
    return aniDict


def buildColliderDict(aniDict):
    colliderDict = {}
    for key in aniDict:
        colliderDict[key] = []
        for i in xrange(len(aniDict[key])):
            colliderDict[key].append(aniDict[key][i].getSize())
    return colliderDict