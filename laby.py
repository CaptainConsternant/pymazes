#!/usr/bin/env python
import random
import pygame
from pygame import gfxdraw, Rect
from pygame.locals import *
import math
from outils import *


ck = (0, 0, 0)
csize = 20
wall_color = (125,125,125)
cell_color = (80,80,80)
cell_current_color = (150,60,100)
gx = 600
gy = 400
gcols= int(gx/csize)
glines= int(gy/csize)
flags=  HWSURFACE | DOUBLEBUF #| FULLSCREEN

pygame.init()
screen = pygame.display.set_mode((gx, gy), flags)

def wall_idx_to_pos(arg):
    return ((arg[0][0] *csize, arg[0][1] *csize), (arg[1][0] *csize, arg[1][1] *csize))

class Cell():
    """Cellule de labyrinthe"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = cell_color
        self.index_x = int(x/csize)
        self.index_y = int(y/csize)
        self.in_lab = False

        self.walls_idx = [
            ((self.index_x, self.index_y), (self.index_x + 1, self.index_y)), #H
            ((self.index_x + 1, self.index_y), (self.index_x + 1, self.index_y + 1)),#d
            ((self.index_x , self.index_y+ 1), (self.index_x + 1, self.index_y + 1)),#b
            ((self.index_x, self.index_y ), (self.index_x, self.index_y + 1)),#g
        ]
        self.walls_pos = [ wall_idx_to_pos(wall) for wall in self.walls_idx  ]

    def neigh(self):
        self.index_x
        pass

    def show(self):
        pygame.draw.rect(screen,self.color, Rect((self.x,self.y),(csize,csize)), )
        for wall in self.walls_pos :
            if wall :
                pygame.draw.line(screen, wall_color, wall[0], wall[1])






tab_cell = [[Cell(x*csize,y*csize) for y in range(int(gy/csize))] for x in range(int(gx/csize))]
#import ipdb; ipdb.set_trace()

randx=int(random.randrange(0,gx/csize))
randy=int(random.randrange(0,gy/csize))
current_cell = tab_cell[randx][randy]
print(current_cell.index_x, current_cell.index_y)
current_cell.color = cell_current_color
current_cell.in_lab = True
lab_walls = current_cell.walls_idx

# import ipdb; ipdb.set_trace()

run=True
freeze = False
while run:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        run = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE:
            freeze = not freeze

    # debut algo :
    # as long as ther are walls_idx
    if lab_walls:
        # pick random wall
        idx = random.randrange(0,len(lab_walls))
        wall = lab_walls[idx]
        print('walls %s' % str(lab_walls))
        if wall[0][0] == wall[1][0] : # wall is vert (x stays the same)
            cell1=tab_cell[wall[0][0]][wall[0][1]]
            cell2=tab_cell[wall[0][0]-1][wall[0][1]]
        else :
            cell1=tab_cell[wall[0][0]][wall[0][1]]
            cell2=tab_cell[wall[0][0]][wall[0][1]-1]
            cell1.color = cell_current_color
            cell2.color = cell_current_color


        if cell1.in_lab != cell2.in_lab : # only one cell in_lab
            # delete wall
            # cell1.walls_idx.remove(wall)
            # cell2.walls_idx.remove(wall)
            # cell1.walls_pos.remove(wall_idx_to_pos(wall))
            # cell2.walls_pos.remove(wall_idx_to_pos(wall))
            # del lab_walls[idx]
            wall_pos=wall_idx_to_pos(wall)
            lab_walls = [x for x in lab_walls if x != wall]
            cell1.walls_idx = [x for x in cell1.walls_idx if x != wall]
            cell2.walls_idx = [x for x in cell2.walls_idx if x != wall]
            cell1.walls_pos = [x for x in cell1.walls_pos if x != wall_pos]
            cell2.walls_pos = [x for x in cell2.walls_pos if x != wall_pos]

            # add neighbouring walls to list
            lab_walls = list(set(lab_walls + cell1.walls_idx + cell2.walls_idx))
        else :
            print('pb tous_visités')
    else :
        print('plus de mur, terminé')




    if not freeze:
        # pygame.draw.rect(screen, random_color(), Rect((200,200),(50,50)), )
        for cols in tab_cell :
            for cell in cols :
                cell.show()
        # for wall in lab_walls :
        #     pygame.draw.line(screen, wall_color, wall[0], wall[1])
        pygame.event.poll()
        pygame.display.flip()
        screen.fill((60,60,60))
