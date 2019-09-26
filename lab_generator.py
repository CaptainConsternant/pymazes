#!/usr/bin/env python
import random
import pygame
from pygame import gfxdraw, Rect
from pygame.locals import HWSURFACE, DOUBLEBUF, K_SPACE
import math
from outils import random_color, random_rgb, random_vector
from laby_objects import Cell
from params import GX, GY, CSIZE, CELL_COLOR, HCELL_COLOR




flags=  HWSURFACE | DOUBLEBUF #| FULLSCREEN

pygame.init()
screen = pygame.display.set_mode((GX, GY), flags)
clock = pygame.time.Clock()
# print(pygame.font.get_fonts())


tab_cell = [[Cell(screen, x*CSIZE,y*CSIZE) for y in range(int(GY/CSIZE))] for x in range(int(GX/CSIZE))]
cell_list = [item for subl in tab_cell for item in subl]
completed_cells = []
#import ipdb; ipdb.set_trace()

def random_merge_process_cell(selected_cell, selected_wall, cell_list) :
    for cell in cell_list_potentielles :
        if selected_wall in cell.walls_pos and cell != selected_cell :
            print(f"{selected_cell.cid} and {cell.cid} are neighbour")
            if selected_cell.cid != cell.cid :
                # print('ok removing walls')
                colors = list(set([selected_cell.color, cell.color]).difference([HCELL_COLOR, CELL_COLOR]))
                if colors :
                    col = colors[0]
                else :
                    col = random_color()
                cell.walls_pos.remove(selected_wall)
                selected_cell.walls_pos.remove(selected_wall)
                selected_cell.show()
                id_to_remove = cell.cid
                for c in cell_list :
                    if c.cid in [id_to_remove, selected_cell.cid] :
                        c.cid=selected_cell.cid
                        c.color = col
                        # c.show()

                return True
            else :
                # print('Wall inside a common zone')
                return False


run=True
freeze = False
while run:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        run = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE:
            freeze = not freeze


    if not freeze:
        screen.fill(CELL_COLOR)
        for cols in tab_cell :
            for cell in cols :
                cell.show()
        cell_list_potentielles = [x for x in cell_list if x not in completed_cells]
        if cell_list_potentielles :
            selected_cell=random.choice(cell_list_potentielles)
            # print(f"cell choisie {selected_cell.cid}")
            selected_cell.highlight()
            deleted_wall = False
            processable_walls = selected_cell.walls_pos[:]
            random.shuffle(processable_walls)
            # print('ordre des murs', processable_walls)
            for selected_wall in processable_walls :
                # print('process mur', selected_wall)
                deleted_wall = random_merge_process_cell(selected_cell, selected_wall, cell_list)
                if deleted_wall :
                    break
            
            if not deleted_wall :
                completed_cells.append(selected_cell)
                print(f'cellule {selected_cell.x} {selected_cell.y} écartée')
            else :
                print('dernier mur cassé')

        pygame.event.poll()
        pygame.display.flip()
        # clock.tick(10) # max x fps

