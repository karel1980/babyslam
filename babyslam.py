#!/usr/bin/env python
import pygame, random, sys, os, re, time, getopt
from pygame.locals import *

dev_mode = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "d", ["dev"])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
output = None
verbose = False
for o, a in opts:
    if o == "-d":
        dev_mode = True

TEXTCOLOR = (255, 255, 255)
OUTLINECOLOR = (255, 255, 255)
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
last_hit = 0

NICECOLORS = [( 255, 255, 0 ), ( 255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255)]
symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'

class Special:
    def __init__(self, img, sound):
        base_image = pygame.image.load(img)
        self.image_cache = dict( (x, pygame.transform.rotozoom(base_image, x, 1)) for x in range(-30, 31) )
        self.sound = None
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
    def playSound(self):
        if self.sound != None: self.sound.play()

class SpecialObj:
    def __init__(self, char, special):
        self.t = 0.0
        self.step = 1.0 / 10 # 10 steps, 1/4 second animation
        self.base_angle = random.randint(10, 20)
        self.base_dir = -1 if random.random() < 0.5 else 1

        self.special = special
        self.special.playSound()
        w,h = special.image_cache[0].get_rect().size
        self.center = random.randint(w/2, WINDOWWIDTH - w/2), random.randint(h/2, WINDOWHEIGHT - h/2)

    def draw(self):
        windowSurface.blit(self.image, self.rect)

    def update(self):
        if self.t > 1:
            return

        t2 = 1 - (1 - self.t)**2 # self.t = linear 0..1, self.t2 = ease-out 0..1
        self.angle = int(1.0 * self.base_angle + t2 * 10 * self.base_dir)
        self.image = self.special.image_cache[self.angle]
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.t += self.step

class Letter:
    def __init__(self, char):
        self.t = 0.0
        self.step = 1.0 / 10 # 10 steps, 1/4 second animation

        self.char = char
        self.base_size = random.randint(100, 200)
        # FIXME: improve formula to determine max 'left' value
        self.color = random.choice(NICECOLORS)

        base_surface = createText(self.char, font_cache[int(self.base_size)])
        base_rect = base_surface.get_rect()

        w,h = base_rect.width, base_rect.height
        self.center = random.randint(w/2, WINDOWWIDTH - w/2), random.randint(h/2, WINDOWHEIGHT - h/2)

    def draw(self):
        #TODO: drawTextCenter(text, font, surf, pos, color)
        text = createText(self.char, self.font, self.color)
        outline = createText(self.char, self.font, OUTLINECOLOR)
        r = text.get_rect()
        r.center = self.center
        x,y = r.x, r.y
        windowSurface.blit(outline, (x-1,y-1))
        windowSurface.blit(outline, (x-1,y+1))
        windowSurface.blit(outline, (x+1,y-1))
        windowSurface.blit(outline, (x+1,y+1))
        windowSurface.blit(text, (x,y))

    def update(self):
        if self.t > 1.0:
            return
        t2 = 1.25 - 0.25 * (2*(self.t - 0.5)) # 0...1...0 parabolic
        font_size = 1.0 * self.base_size * t2
        self.font = font_cache[int(font_size)]
        self.t += self.step

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

def drawText(text, font, surface, x, y, color = TEXTCOLOR, center = False):
    textobj = font.render(text, 1, color)
    if center:
      x,y = x-textobj.width/2,y-textobj.height/2
    surface.blit(textobj, (x, y))

# cheap but effective way to render 1-pixel outlines
def drawTextOutline(text, font, surface, x, y, color = TEXTCOLOR, outline_color = OUTLINECOLOR, center = False):
    base_out = font.render(text, 0, outline_color)
    base_in = font.render(text, 0, color)
    if center:
      x,y = x-textobj.width/2,y-textobj.height/2
    surface.blit(base_out, (x-1,y-1))
    surface.blit(base_out, (x-1,y+1))
    surface.blit(base_out, (x+1,y-1))
    surface.blit(base_out, (x+1,y+1))
    surface.blit(base_in, (x,y))

def createText(text, font, color = TEXTCOLOR):
    return font.render(text, 0, color)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
firstmode = pygame.display.list_modes()[0]
mode = WINDOWWIDTH, WINDOWHEIGHT = firstmode
if dev_mode:
    mode = WINDOWWIDTH, WINDOWHEIGHT = 640,480
    windowSurface = pygame.display.set_mode(mode, pygame.NOFRAME)
else:
    windowSurface = pygame.display.set_mode(mode, pygame.FULLSCREEN)
  
pygame.display.set_caption('Babyslam')
pygame.mouse.set_visible(False)

# create font cache (sizes 100 to 300)
font_cache = dict( (x, pygame.font.SysFont(None, x)) for x in range(100, 301) )
#print font_cache.keys()
sysfont = pygame.font.SysFont(None, 15)

def addObject(obj, ary):
  if len(ary) >= MAXOBJECTS:
      ary[0:1] = []
  ary.append(obj)

def loadSpecials():
    result = []
    path = sys.path[0] + '/media'
    media = [ path + '/' + x for x in os.listdir(path) ]
    pattern = re.compile('\.png$')
    for png in filter(lambda x: pattern.search(x), media):
        #clumsy!
        ogg = "%s.wav"%png[0:png.rindex('.')]
        wav = "%s.wav"%png[0:png.rindex('.')]
        if ogg in media:
            result.append(Special(png, ogg))
        elif wav in media:
            result.append(Special(png, wav))
        else: result.append(Special(png, None))
    return result

SPECIALS = loadSpecials()
if len(SPECIALS)==0:
    sys.exit(0)

while True:
    letters = []
    escapecnt = 0
    # set up the start of the game

    while True: # the game loop runs while the game part is playing

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key in range(256) and chr(event.key) in symbols and ESCAPE_CLAUSE[escapecnt] != chr(event.key):
                    escapecnt = 0
                if event.key in range(256) and chr(event.key) in symbols and ESCAPE_CLAUSE[escapecnt] == chr(event.key):
                    escapecnt += 1

                now = time.time() * 1000 # time in millis
                if (now - last_hit) < RATE_LIMIT:
                    last_hit = now
                    continue

                
                char = chr(event.key) if event.key in range(256) and chr(event.key) in symbols else random.choice(symbols)
                if random.random() < SPECIAL_RATE:
                    addObject(SpecialObj(char, random.choice(SPECIALS)), letters)
                else:
                    addObject(Letter(char), letters)

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
            l.update()
            l.draw()

        pygame.display.update()

        mainClock.tick(FPS)

    # Stop the game
