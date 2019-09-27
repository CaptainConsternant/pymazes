#!/usr/bin/env python
import random
import pygame
from pygame import gfxdraw, Rect
from pygame.locals import K_SPACE
import math
from outils import random_color, random_rgb, random_vector
from cell import Cell
from params import GX, GY, CSIZE, CELL_COLOR, HCELL_COLOR, FLAGS



class Maze(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GX, GY), FLAGS)
        self.clock = pygame.time.Clock()
        self.reset_grid()
        self.show_grid()
        pygame.display.flip()

        self.run = True
        self.pause = False

        self.is_generated = False
        self.is_solved = False

        self.main_menu()

    def reset_grid(self):
        self.tab_cell = [[Cell(self.screen, x*CSIZE,y*CSIZE) for y in range(int(GY/CSIZE))] for x in range(int(GX/CSIZE))]
        self.cell_list = [item for subl in self.tab_cell for item in subl]
        self.is_generated = False
        self.is_solved = False

    def show_grid(self):
        # self.screen.fill(CELL_COLOR)
        for cols in self.tab_cell :
            for cell in cols :
                cell.show()
    
    def update_screen(self):
        self.show_grid()
        pygame.display.flip()
        # self.clock.tick(10) # max x fps

    def poll(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False
            print('Quitting...')
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                self.pause = not self.pause
                print("(Un)Pause")


    def generate_by_random_merge(self):
        def random_merge_process_cell(selected_cell, selected_wall) :
            for cell in self.cell_list_potentielles :
                if selected_wall in cell.walls_pos and cell != selected_cell :
                    # print(f"{selected_cell.cid} and {cell.cid} are neighbour")
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
                        for c in self.cell_list :
                            if c.cid in [id_to_remove, selected_cell.cid] :
                                c.cid=selected_cell.cid
                                c.color = col
                                # c.show()

                        return True
                    else :
                        # print('Wall inside a common zone')
                        return False
        completed_cells = []
        while self.run:
            self.poll()
            if not self.pause:
                # self.screen.fill(CELL_COLOR)
                self.cell_list_potentielles = [x for x in self.cell_list if x not in completed_cells]
                if self.cell_list_potentielles :
                    selected_cell=random.choice(self.cell_list_potentielles)
                    # print(f"cell choisie {selected_cell.cid}")
                    selected_cell.highlight()
                    deleted_wall = False
                    processable_walls = selected_cell.walls_pos[:]
                    random.shuffle(processable_walls)
                    # print('ordre des murs', processable_walls)
                    for selected_wall in processable_walls :
                        # print('process mur', selected_wall)
                        deleted_wall = random_merge_process_cell(selected_cell, selected_wall)
                        if deleted_wall :
                            break
                    
                    if not deleted_wall :
                        completed_cells.append(selected_cell)
                        # print(f'cellule {selected_cell.x} {selected_cell.y} écartée')
                    else :
                        # print('dernier mur cassé')
                        pass
                else :
                    self.run = False
                    print('end')
                    self.main_menu()

                self.update_screen()

    def main_menu(self):
        print(f"{' MAIN MENU ':_^30}")
        print("1. Generate by random merge")
        print('q. Quit')
        print()
        resp=None
        while resp not in ['1', 'Q']:
            resp = str(input("Please enter a number")).upper().strip()

        if resp == "Q":
            print("Bye. Comme back soon !")
            return
        elif resp == '1' :
            self.generate_by_random_merge()

    
#import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    a=Maze()

