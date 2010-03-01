import pygame, random, sys, os, re, time, getopt
from pygame.locals import *

import shared, text


# put sound playback here?
class BaseEffect(object):
    pass

class BaseEffectInstance(object):
    def __init__(self, steps, sound=None):
        self.t = 0
        self.increase = 1.0 / steps
        if sound != None:
          sound.play()

    def update(self):
        if self.t < 1:
            self.t += self.increase
            if self.t >= 1:
                self.t = 1
            self.do_update()

    def do_update(self):
        pass;


class RotateEffect(BaseEffect):
    def __init__(self, images, sound):
        super(RotateEffect, self).__init__()
        self.images = [ pygame.image.load(img) for img in images ]
        self.sound = sound
        
    def create_instance(self, char):
        return RotateEffectInstance(40, self.images, self.sound)

class RotateEffectInstance(BaseEffectInstance):
    def __init__(self, steps, images, sound):
        super(RotateEffectInstance, self).__init__(steps, sound)
        self.images = images
        self.current = -1 

        self.base_angle = random.randint(-20, 20)
        self.base_dir = -1 if random.random() < 0.5 else 1

        w,h = self.images[0].get_rect().size
        #should be different with every instance
        self.center = random.randint(w/2, shared.WINDOWWIDTH - w/2), random.randint(h/2, shared.WINDOWHEIGHT - h/2)

    def draw(self):
        shared.windowSurface.blit(self.current_image, self.rect)

    def do_update(self):
        self.current = ( self.current + 1 ) % len(self.images)
        self.current_image = self.images[self.current];

        t2 = 1 - (1 - self.t)**2 # self.t = linear 0..1, self.t2 = ease-out 0..1

        self.angle = int(1.0 * self.base_angle + t2 * 10 * self.base_dir)
        self.current_image = pygame.transform.rotozoom(self.current_image, self.angle, 1)
        self.rect = self.current_image.get_rect()
        self.rect.center = self.center
        self.t += self.increase
       
class FlipEffect(BaseEffect):
    def __init__(self, images, sound):
        super(FlipEffect, self).__init__()
        self.images = [ pygame.image.load(img) for img in images ]
        self.sound = sound
        
    def create_instance(self, char):
        return FlipEffectInstance(20, self.images, self.sound)

class FlipEffectInstance(BaseEffectInstance):
    def __init__(self, steps, images, sound):
        super(FlipEffectInstance, self).__init__(steps, sound)
        self.images = images

        self.base_angle = random.randint(-20, 20)
        self.base_dir = -1 if random.random() < 0.5 else 1

        self.flipstart = 0
        self.halfway = 0.5
        self.flipend = 1

        size = self.images[0].get_rect().size
        # make a 3:2 rect:
        border = 20
        rect = pygame.Rect(0, 0, int(max(size[1] * 3 / 2, size[0])), int(max(size[0] * 2 / 3, size[1]))).inflate(border, border)
        bordercolor = random.choice(shared.NICECOLORS)
        bgcolor = random.choice(shared.NICECOLORS)

        self.back = pygame.Surface(rect.size)
        self.back.fill(bordercolor)
        self.back.fill(bgcolor, self.back.get_rect().inflate(-border,-border))

        self.front = pygame.Surface(rect.size)
        self.front.set_colorkey((0,0,0))
        self.front.fill(bordercolor)
        self.front.fill(bgcolor, self.back.get_rect().inflate(-border,-border))
        imgrect = self.images[0].get_rect()
        imgrect.center = rect.center
        self.front.blit(self.images[0], imgrect.topleft)
        w,h = self.front.get_rect().size
        self.center = random.randint(w/2, shared.WINDOWWIDTH - w/2), random.randint(h/2, shared.WINDOWHEIGHT - h/2)

    def draw(self):
        rect = self.image.get_rect()
        rect.center = self.center
        self.image.set_colorkey((0,0,0))
        shared.windowSurface.blit(self.image, rect)

    def do_update(self):
        if self.t < self.flipstart:
          self.image = pygame.transform.rotozoom(self.back, self.base_angle, 1)
        elif self.t < self.halfway:
          t2 = 1 - (self.t-self.flipstart)/(self.halfway - self.flipstart) # linear from [1, 0[ between t=0.2 and t=0.5
          width = int(self.back.get_rect().width * t2)
          width = width if width > 0 else 1
          height = self.back.get_rect().height
          self.image = pygame.transform.scale(self.back, (width, height))
          self.image = pygame.transform.rotozoom(self.image, self.base_angle, 1)
        elif self.t < self.flipend:
          t2 = (self.t-self.halfway)/(self.flipend - self.halfway) # linear from 0 to 1 between t=0.5 and t=0.8
          width = int(self.front.get_rect().width * t2)
          width = width if width > 0 else 1
          height = self.front.get_rect().height
          self.image = pygame.transform.scale(self.front, (width, height))
          self.image = pygame.transform.rotozoom(self.image, self.base_angle, 1)
        else:
          self.image = pygame.transform.rotozoom(self.front, self.base_angle, 1)

class LetterEffect(BaseEffect):
    def __init__(self):
        super(LetterEffect, self).__init__() 

    def create_instance(self, char):
        return LetterEffectInstance(10, char)

class LetterEffectInstance(BaseEffectInstance):
    def __init__(self, steps, char):
        super(LetterEffectInstance, self).__init__(steps) 

        self.char = char
        self.base_size = random.randint(100, 200)
        # FIXME: improve formula to determine max 'left' value
        self.color = random.choice(shared.NICECOLORS)

        base_surface = text.createText(self.char, shared.font_cache[int(self.base_size)])
        base_rect = base_surface.get_rect()

        w,h = base_rect.width, base_rect.height
        self.center = random.randint(w/2, shared.WINDOWWIDTH - w/2), random.randint(h/2, shared.WINDOWHEIGHT - h/2)

    def draw(self):
        #TODO: text.drawTextCenter(text, font, surf, pos, color)
        mytext = text.createText(self.char, self.font, self.color)
        outline = text.createText(self.char, self.font, shared.OUTLINECOLOR)
        r = mytext.get_rect()
        r.center = self.center
        x,y = r.x, r.y
        shared.windowSurface.blit(outline, (x-1,y-1))
        shared.windowSurface.blit(outline, (x-1,y+1))
        shared.windowSurface.blit(outline, (x+1,y-1))
        shared.windowSurface.blit(outline, (x+1,y+1))
        shared.windowSurface.blit(mytext, (x,y))

    def do_update(self):
        t2 = 1.25 - 0.25 * (2*(self.t - 0.5)) # 0...1...0 parabolic
        font_size = 1.0 * self.base_size * t2
        self.font = shared.font_cache[int(font_size)]
