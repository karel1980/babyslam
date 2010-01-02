import pygame, random, sys
from pygame.locals import *

TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
LETTERMINSIZE = 10
LETTERMAXSIZE = 40
IMAGEMINSIZE = 1
IMAGEMAXSIZE = 8
PLAYERMOVERATE = 5
ESCAPE_CLAUSE = "babydodo"
MAXOBJECTS = 15
SPECIAL_RATE = 1.0/10 # frequency of 'specials'

NICECOLORS = [( 255, 255, 0 ), ( 255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255)]
LETTER_MAP = 'qazwsxedcrfvtgbyhnujmikolp'

class Special:
  def __init__(self, img, sound):
    self.img = pygame.image.load(img)
    self.sound = pygame.mixer.Sound(sound)

class SpecialObj:
  def __init__(self, char, special):
    print '!!! ', special.img
    self.special = special
    self.rect = special.img.get_rect()
    self.rect.topleft = ((WINDOWWIDTH*.8)*LETTER_MAP.index(char)/len(LETTER_MAP), WINDOWHEIGHT / 2) #TODO: subtract half of special img height, add rnd factor

  def draw(self):
    windowSurface.blit(self.special.img, self.rect)

class Letter:
  def __init__(self, char):
    fi = random.randint(0, len(fonts)-1)
    # FIXME: improve formula to determine max 'left' value
    self.text = char
    self.font = fonts[fi]
    self.left = (WINDOWWIDTH*.8)*LETTER_MAP.index(char)/len(LETTER_MAP)
    self.top = random.randint(0, WINDOWHEIGHT - fheights[fi])
    self.color = random.choice(NICECOLORS)

  def draw(self):
    drawText(l.text, l.font, windowSurface, l.left, l.top, l.color)


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def drawText(text, font, surface, x, y, color = TEXTCOLOR):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
# todo: full screen
pygame.init()
mainClock = pygame.time.Clock()
firstmode = pygame.display.list_modes()[0]
WINDOWWIDTH, WINDOWHEIGHT = firstmode
windowSurface = pygame.display.set_mode(firstmode, pygame.FULLSCREEN)
pygame.display.set_caption('Babyslam')
#pygame.mouse.set_visible(False)

# set up fonts
fheights = [ 80, 160, 240 ]
fonts = [ pygame.font.SysFont(None, x) for x in fheights ]
sysfont = pygame.font.SysFont(None, 15)

# set up images
#playerImage = pygame.image.load('player.png')
#playerRect = playerImage.get_rect()
#baddieImage = pygame.image.load('baddie.png')

def addObject(obj, ary):
  if len(ary) >= MAXOBJECTS:
      ary[0:1] = []
  ary.append(obj)

#print [ x.strip() for x in open('specials').readlines() ]
# TODO: load specials from specials file
SPECIALS = [ Special('mama.png', 'mama.ogg') ]

while True:
    letters = []
    escapecnt = 0
    # set up the start of the game

    while True: # the game loop runs while the game part is playing

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key >= ord('a') and event.key <= ord('z') and ESCAPE_CLAUSE[escapecnt] != chr(event.key):
                    escapecnt = 0
                if event.key >= ord('a') and event.key <= ord('z') and ESCAPE_CLAUSE[escapecnt] == chr(event.key):
                    escapecnt += 1

                if event.key >= ord('a') and event.key <= ord('z'):
                    if random.random() < SPECIAL_RATE:
                        addObject(SpecialObj(chr(event.key), random.choice(SPECIALS)), letters)
                    else:
                        addObject(Letter(chr(event.key)), letters)

            if event.type == KEYUP:
                None

            if event.type == MOUSEMOTION:
                None

        if escapecnt == len(ESCAPE_CLAUSE):
            terminate()
        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        drawText('type %s to quit'%ESCAPE_CLAUSE, sysfont, windowSurface, 0, 0)
        # Draw the letters
        for l in letters:
            l.draw()

        pygame.display.update()

        mainClock.tick(FPS)

    # Stop the game
