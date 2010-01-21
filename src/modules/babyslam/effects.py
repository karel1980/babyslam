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

