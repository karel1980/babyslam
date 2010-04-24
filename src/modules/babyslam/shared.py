
import os, sys, pygame

TEXTCOLOR = (255, 255, 255)
OUTLINECOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)

FPS = 40
LETTERMINSIZE = 10
LETTERMAXSIZE = 40
IMAGEMINSIZE = 1
IMAGEMAXSIZE = 8
PLAYERMOVERATE = 5
MAXOBJECTS = 15
SPECIAL_RATE = 1.0/5 # frequency of 'specials'
RATE_LIMIT = 0 # minimum number of milliseconds between hits
NICECOLORS = [( 255, 255, 0 ), ( 255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255)]

WINDOWWIDTH, WINDOWHEIGHT = 0, 0
windowSurface = None
font_cache = None
cursor_image = None

def init(mode_res, mode_flags = 0):
    global WINDOWWIDTH, WINDOWHEIGHT, windowSurface, font_cache, cursor_image

    pygame.init()
    mainClock = pygame.time.Clock()

    mode_res = pygame.display.list_modes()[0] if mode_res is None else mode_res
    WINDOWWIDTH, WINDOWHEIGHT = mode_res
    windowSurface = pygame.display.set_mode(mode_res, mode_flags)

    pygame.display.set_caption('Babyslam')
    pygame.mouse.set_visible(False)

    # create font cache (sizes 100 to 300)
    font_cache = dict( (x, pygame.font.SysFont(None, x)) for x in range(100, 301) )

    prefix = __file__
    for a in range(5):
      prefix = os.path.split(prefix)[0]
    media_dir = os.path.join(prefix, 'share', 'babyslam', 'media')
    cursor_image = pygame.image.load(os.path.join(media_dir, 'mouse.png'))
    
    return mainClock     

