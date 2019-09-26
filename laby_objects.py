#!/usr/bin/env python
from params import CELL_COLOR, HCELL_COLOR, CSIZE, WALL_COLOR
import pygame
from pygame import Rect
from itertools import count


class Cell():
    """Cellule de labyrinthe"""
    global_cell_counter = count(0)
    def __init__(self, screen, x, y, print_ids=False):
        self.cid = next(self.global_cell_counter) # cell id
        self.screen = screen
        self.x = x
        self.y = y
        self.color = CELL_COLOR
        self.index_x = int(x/CSIZE)
        self.index_y = int(y/CSIZE)
        self.in_lab = False
        self.print_ids = print_ids 
        if self.print_ids :
            self.font = pygame.font.SysFont('dejavusans', 8, bold=True)

        self.walls_idx = [
            ((self.index_x, self.index_y), (self.index_x + 1, self.index_y)), #top
            ((self.index_x + 1, self.index_y), (self.index_x + 1, self.index_y + 1)),#right
            ((self.index_x , self.index_y+ 1), (self.index_x + 1, self.index_y + 1)),#bottom
            ((self.index_x, self.index_y ), (self.index_x, self.index_y + 1)),#left
        ]
        self.walls_pos = [ self.wall_idx_to_pos(wall) for wall in self.walls_idx  ]
        # print(self.cid, self.walls_pos)

    def neigh(self):
        self.index_x
        pass

    def show(self):
        pygame.draw.rect(self.screen,self.color, Rect((self.x,self.y),(CSIZE,CSIZE)), )
        for wall in self.walls_pos :
            if wall :
                pygame.draw.line(self.screen, WALL_COLOR, wall[0], wall[1], width=2)
        
        if self.print_ids :
            textsurface = self.font.render(str(self.cid), False, (150, 150, 255))
            self.screen.blit(textsurface,(self.x+CSIZE/4,self.y+CSIZE/3))

    def highlight(self):
        col = self.color
        self.color = HCELL_COLOR
        self.show()
        self.color = col

    def wall_idx_to_pos(self, arg):
        return ((arg[0][0] *CSIZE, arg[0][1] *CSIZE), (arg[1][0] *CSIZE, arg[1][1] *CSIZE))


