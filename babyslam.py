import pygame, random, sys, os, re
from pygame.locals import *

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
now = 0
last_hit = 0

NICECOLORS = [( 255, 255, 0 ), ( 255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255)]
LETTER_MAP = '1qa2zws3xed4crf5vtg6byh7nuj8mik9ol0p'

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
        self.base_dir = -1 if random.random() > 0.5 else 1

        self.special = special
        self.special.playSound()
        w,h = special.image_cache[0].get_rect().size
        self.center = w/2 + (WINDOWWIDTH - w)*LETTER_MAP.index(char)/len(LETTER_MAP), random.randint(h/2, WINDOWHEIGHT - h)

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
        left = (WINDOWWIDTH*.8)*LETTER_MAP.index(char)/len(LETTER_MAP)
        top = random.randint(0, WINDOWHEIGHT - self.base_size)
        self.base_pos = (left, top)

    def draw(self):
        #TODO: drawTextCenter(text, font, surf, pos, color)
        drawTextOutline(self.char, self.font, windowSurface, self.pos[0], self.pos[1], self.color)

    def update(self):
        if self.t > 1.0:
            return
        t2 = 1.25 - 0.25 * (2*(self.t - 0.5)) # 0...1...0 parabolic
        font_size = 1.0 * self.base_size * t2
        self.font = font_cache[int(font_size)]
        self.pos = self.base_pos
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

def drawText(text, font, surface, x, y, color = TEXTCOLOR):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# cheap but reasonaly effective way to render 1-pixel outlines
def drawTextOutline(text, font, surface, x, y, color = TEXTCOLOR, outline_color = OUTLINECOLOR):
    base_out = font.render(text, 0, outline_color)
    base_in = font.render(text, 0, color)
    surface.blit(base_out, (x-1,y-1))
    surface.blit(base_out, (x-1,y+1))
    surface.blit(base_out, (x+1,y-1))
    surface.blit(base_out, (x+1,y+1))
    surface.blit(base_in, (x,y))

# set up pygame, the window, and the mouse cursor
# todo: full screen
pygame.init()
mainClock = pygame.time.Clock()
firstmode = pygame.display.list_modes()[0]
WINDOWWIDTH, WINDOWHEIGHT = firstmode
windowSurface = pygame.display.set_mode(firstmode, pygame.FULLSCREEN)
pygame.display.set_caption('Babyslam')
#pygame.mouse.set_visible(False)

# create font cache (sizes 100 to 300)
font_cache = dict( (x, pygame.font.SysFont(None, x)) for x in range(100, 300) )
#print font_cache.keys()
sysfont = pygame.font.SysFont(None, 15)

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
                if event.key in range(256) and chr(event.key) in LETTER_MAP and ESCAPE_CLAUSE[escapecnt] != chr(event.key):
                    escapecnt = 0
                if event.key in range(256) and chr(event.key) in LETTER_MAP and ESCAPE_CLAUSE[escapecnt] == chr(event.key):
                    escapecnt += 1

                if event.key in range(256) and chr(event.key) in LETTER_MAP:
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
            l.update()
            l.draw()

        pygame.display.update()

        mainClock.tick(FPS)

    # Stop the game
