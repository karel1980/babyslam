import pygame, random, sys, os, re, time, getopt

import shared, text

class Special:
    def __init__(self, img, sounds):
        base_image = pygame.image.load(img)
        self.image_cache = dict( (x, pygame.transform.rotozoom(base_image, x, 1)) for x in range(-30, 31) )
        self.sound_cache = [ pygame.mixer.Sound(sound) for sound in sounds ]

    def playSound(self):
        if len(self.sound_cache) > 0: random.choice(self.sound_cache).play()

class SpecialObj:
    def __init__(self, char, special):
        self.t = 0.0
        self.step = 1.0 / 10 # 10 steps, 1/4 second animation
        self.base_angle = random.randint(-20, 20)
        self.base_dir = -1 if random.random() < 0.5 else 1

        self.special = special
        self.special.playSound()
        w,h = special.image_cache[0].get_rect().size
        self.center = random.randint(w/2, shared.WINDOWWIDTH - w/2), random.randint(h/2, shared.WINDOWHEIGHT - h/2)

    def draw(self):
        shared.windowSurface.blit(self.image, self.rect)

    def update(self):
        if self.t > 1:
            return

        t2 = 1 - (1 - self.t)**2 # self.t = linear 0..1, self.t2 = ease-out 0..1
        self.angle = int(1.0 * self.base_angle + t2 * 10 * self.base_dir)
        self.image = self.special.image_cache[self.angle]
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.t += self.step

class Flip:
    def __init__(self, char, special):
        self.t = 0.0
        self.step = 1.0 / 40 # 1 second animation
        self.base_angle = random.randint(-20, 20)
        self.base_dir = -1 if random.random() < 0.5 else 1

        self.special = special
        self.special.playSound()

        size = special.image_cache[0].get_rect().size
        # make a 3:2 rect:
        border = 20
        rect = pygame.Rect(0, 0, int(max(size[1] * 3 / 2, size[0])), int(max(size[0] * 2 / 3, size[1]))).inflate(border, border)
        self.back = pygame.Surface(rect.size)
        self.back.fill(random.choice(shared.NICECOLORS))
        self.back.fill(random.choice(shared.NICECOLORS), self.back.get_rect().inflate(-border,-border))

        self.front = special.image_cache[0] # replace with solid fill (add 0.2 border, superimpose image)
        w,h = self.front.get_rect().size
        self.center = random.randint(w/2, shared.WINDOWWIDTH - w/2), random.randint(h/2, shared.WINDOWHEIGHT - h/2)

    def draw(self):
        rect = self.image.get_rect()
        rect.center = self.center
        shared.windowSurface.blit(self.image, rect)

    def update(self):
        if self.t > 1:
            return

        if self.t < 0.2:
          self.image = pygame.transform.rotozoom(self.back, self.base_angle, 1)
        elif self.t < 0.5:
          t2 = 1 - (self.t-0.2)/0.3 # linear from [1, 0[ between t=0.2 and t=0.5
          width = int(self.back.get_rect().width * t2)
          width = width if width > 0 else 1
          height = self.back.get_rect().height
          self.image = pygame.transform.scale(self.back, (width, height))
          self.image = pygame.transform.rotozoom(self.image, self.base_angle, 1)
        elif self.t < 0.8:
          t2 = (self.t-0.5)/0.3 # linear from 0 to 1 between t=0.5 and t=0.8
          width = int(self.front.get_rect().width * t2)
          width = width if width > 0 else 1
          height = self.front.get_rect().height
          self.image = pygame.transform.scale(self.front, (width, height))
          self.image = pygame.transform.rotozoom(self.image, self.base_angle, 1)
        else:
          self.image = pygame.transform.rotozoom(self.front, self.base_angle, 1)

        self.t += self.step

class Letter:
    def __init__(self, char):
        self.t = 0.0
        self.step = 1.0 / 10 # 10 steps, 1/4 second animation

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

    def update(self):
        if self.t > 1.0:
            return
        t2 = 1.25 - 0.25 * (2*(self.t - 0.5)) # 0...1...0 parabolic
        font_size = 1.0 * self.base_size * t2
        self.font = shared.font_cache[int(font_size)]
        self.t += self.step

