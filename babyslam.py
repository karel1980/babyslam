import pygame, random, sys, os, re
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
SPECIAL_RATE = 1.0/5 # frequency of 'specials'
RATE_LIMIT = 100 # number of milliseconds between hits
now = 0
last_hit = 0

NICECOLORS = [( 255, 255, 0 ), ( 255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255)]
LETTER_MAP = '1qa2zws3xed4crf5vtg6byh7nuj8mik9ol0p'

class Special:
    def __init__(self, img, sound):
        self.img = pygame.image.load(img)
        self.sound = None
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
    def playSound(self):
        if self.sound != None: self.sound.play()

class SpecialObj:
    def __init__(self, char, special):
        self.special = special
        self.image = pygame.transform.rotozoom(special.img, random.randint(-30, 30), 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WINDOWWIDTH*.8)*LETTER_MAP.index(char)/len(LETTER_MAP), random.randint(0, WINDOWHEIGHT - self.rect.height)
        self.special.playSound()
    def draw(self):
        windowSurface.blit(self.image, self.rect)

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

def loadSpecials():
    result = []
    media = [ 'media/' + x for x in os.listdir('media') ]
    pattern = re.compile('\.png$')
    for png in filter(lambda x: pattern.search(x), media):
        ogg = "%s.wav"%png[0:png.rindex('.')]
        wav = "%s.wav"%png[0:png.rindex('.')]
        if ogg in media:
            result.append(Special(png, ogg))
        elif wav in media:
            result.append(Special(png, wav))
        else: result.append(Special(png, None))
    return result

SPECIALS = loadSpecials()

while True:
    letters = []
    escapecnt = 0
    # set up the start of the game

    while True: # the game loop runs while the game part is playing

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if chr(event.key) in LETTER_MAP and ESCAPE_CLAUSE[escapecnt] != chr(event.key):
                    escapecnt = 0
                if chr(event.key) in LETTER_MAP and ESCAPE_CLAUSE[escapecnt] == chr(event.key):
                    escapecnt += 1

                if chr(event.key) in LETTER_MAP:
                    if (now - last_hit) > RATE_LIMIT:
                        continue
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
