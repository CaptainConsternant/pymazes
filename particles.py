#!/usr/bin/env python
import random
import pygame
from pygame import gfxdraw
from pygame.locals import *
import math
from outils import *


ck = (0, 0, 0)
size = 5
g_x = 600
g_y = 400
nb_parts = 100
flags=  HWSURFACE | DOUBLEBUF #| FULLSCREEN

pygame.init()
screen = pygame.display.set_mode((g_x, g_y), flags)


class Particle():
    """docstring for Particle."""
    def __init__(self, x = 0, y = 0):
        super(Particle, self).__init__()
        self.surf = pygame.Surface((size*2+2, size*2+2))
        self.surf.fill(ck)
        self.surf.set_colorkey(ck)
        self.color = random_color()
        # pygame.draw.circle(self.surf, self.color, (size, size), size)
        self.surf.set_alpha(175)
        pygame.gfxdraw.filled_circle(self.surf, size-1, size-1, size-1, self.color)
        pygame.gfxdraw.aacircle(self.surf, size-1, size-1, size-1, self.color)
        self.pos = [x-size,y-size]
        self.speed=random_vector(0.1)
        # print(self.speed)

    def update_pos(self):
        new_x = self.pos[0] + self.speed[0]
        new_y = self.pos[1] + self.speed[1]

        if new_x <= 0 or new_x >= g_x:
            self.speed[0] *= -1
        if new_y <= 0 or new_y >= g_y:
            self.speed[1] *= -1

        self.pos = [
            new_x,
            new_y
        ]

    def get_pos(self):
        """
        Position en int pour placement sur la grille
        """
        return [
            int(self.pos[0]),
            int(self.pos[1]),
        ]


run=True
freeze = False
particles=[Particle(300,200) for x in ['']*nb_parts]
while run:
    event = pygame.event.poll()
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        p = Particle(x=x, y=y)
        screen.blit(p.surf, p.get_pos())
        # pygame.draw.circle(screen, p.color, p.get_pos(), size)

        particles.append(p)

    elif event.type == pygame.QUIT:
        run = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE:
            freeze = not freeze

    if not freeze:
        for p in particles :
            p.update_pos()
            screen.blit(p.surf, p.get_pos())
            # pygame.draw.circle(screen, p.color, p.get_pos(), size)

        pygame.event.poll()
        pygame.display.flip()
        screen.fill((30,30,30))
