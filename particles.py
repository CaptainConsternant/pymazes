#!/usr/bin/env python
import random
import pygame
from pygame import gfxdraw
from pygame.locals import *
import math


ck = (0, 0, 0)
size = 10
g_x = 600
g_y = 400
nb_parts = 1000

pygame.init()
screen = pygame.display.set_mode((g_x, g_y), HWSURFACE | FULLSCREEN |  DOUBLEBUF)

def rand_col():
    return (
        int(random.random()*256),
        int(random.random()*256),
        int(random.random()*256)
        )

class Particle():
    """docstring for Particle."""
    def __init__(self, x = 0, y = 0):
        super(Particle, self).__init__()
        self.surf = pygame.Surface((size*2, size*2))
        self.surf.fill(ck)
        self.surf.set_colorkey(ck)
        self.color = rand_col()
        pygame.draw.circle(self.surf, self.color, (size, size), size)
        # pygame.gfxdraw.aacircle(self.surf, size-2, size-2, size-2, self.color)
        # pygame.gfxdraw.filled_circle(self.surf, size-2, size-2, size-2, self.color)
        self.surf.set_alpha(150)
        self.pos = [x-size,y-size]

        rand_angle=random.random()*math.pi*2
        rand_mag = random.random()
        self.speed=[math.cos(rand_angle)*rand_mag,math.sin(rand_angle)*rand_mag]
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
particles=[Particle(300,200) for x in ['']*nb_parts]
while run:
    screen.fill((30,30,30))
    event = pygame.event.poll()
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        p = Particle(x=x, y=y)
        screen.blit(p.surf, p.get_pos())
        # pygame.draw.circle(screen, p.color, p.get_pos(), size)

        particles.append(p)

    elif event.type == pygame.QUIT:
        run = 0

    for p in particles :
        p.update_pos()
        screen.blit(p.surf, p.get_pos())
        # pygame.draw.circle(screen, p.color, p.get_pos(), size)

    pygame.event.poll()
    pygame.display.flip()
