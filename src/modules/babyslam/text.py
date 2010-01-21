from pygame.locals import *

import const

def drawText(text, font, surface, x, y, color = const.TEXTCOLOR, center = False):
    textobj = font.render(text, 1, color)
    if center:
      x,y = x-textobj.width/2,y-textobj.height/2
    surface.blit(textobj, (x, y))

# cheap but effective way to render 1-pixel outlines
def drawTextOutline(text, font, surface, x, y, color = const.TEXTCOLOR, outline_color = const.OUTLINECOLOR, center = False):
    base_out = font.render(text, 0, outline_color)
    base_in = font.render(text, 0, color)
    if center:
      x,y = x-textobj.width/2,y-textobj.height/2
    surface.blit(base_out, (x-1,y-1))
    surface.blit(base_out, (x-1,y+1))
    surface.blit(base_out, (x+1,y-1))
    surface.blit(base_out, (x+1,y+1))
    surface.blit(base_in, (x,y))

def createText(text, font, color = const.TEXTCOLOR):
    return font.render(text, 0, color)

