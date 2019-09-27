#!/usr/bin/env python
from collections import Counter
import math
import pygame
from pygame import gfxdraw, Rect
from pygame.locals import K_SPACE
from queue import LifoQueue
import random
import sys

from outils import random_color, random_rgb, random_vector
from cell import Cell
from params import GX, GY, CSIZE, CELL_COLOR, HCELL_COLOR, VISITED_COLOR, FLAGS



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
        self.generate_by_wilson()
        self.main_menu()

    def reset_grid(self):
        self.tab_cell = [[Cell(self.screen, x*CSIZE,y*CSIZE) for y in range(int(GY/CSIZE))] for x in range(int(GX/CSIZE))]
        self.cell_list = [item for subl in self.tab_cell for item in subl]
        self.is_generated = False
        self.is_solved = False

    def show_grid(self, highlight_cells=[]):
        # self.screen.fill(CELL_COLOR)
        for cols in self.tab_cell :
            for cell in cols :
                if cell in highlight_cells :
                    col = cell.color
                    cell.color = HCELL_COLOR
                    cell.show()
                    cell.color = col
                else :
                    cell.show()
    
    def update_screen(self, highlight_cells=[] ):
        self.show_grid(highlight_cells=highlight_cells)
        pygame.display.flip()
        # self.clock.tick(4) # max x fps

    def poll(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False
            print('Quitting...')
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                self.pause = not self.pause
                print("(Un)Pause")

    def find_neighbours(self, cell):
        neighs = []
        cwalls_pos = set(cell.walls_pos)
        for c in self.cell_list :
            if c != cell and cwalls_pos.intersection(c.walls_pos) :
                neighs.append(c)
                if len(neighs) == 4 :
                    break
        # print(neighs)
        return neighs

    def find_cells_by_wall(self, wall) :
        # print(wall)
        cells = []
        for c in self.cell_list :
            if wall in c.walls_pos :
                cells.append(c)
                if len(cells) == 2 :
                    break
        return cells


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

                self.update_screen(highlight_cells=[])

    def generate_by_depth_first_search(self):
        path = LifoQueue()
        visited_cells = []
        current_cell = random.choice(self.cell_list)
        path.put(current_cell)
        while self.run:
            self.poll()
            if not self.pause:
                while path.qsize():
                    visited_cells.append(current_cell)
                    current_cell.color = VISITED_COLOR
                    neighs = self.find_neighbours(current_cell)
                    # print("neighs", neighs)

                    possible_neighs = [x for x in neighs if x not in visited_cells]
                    # print("possneigs", possible_neighs)
                    if possible_neighs :
                        neigh = random.choice(possible_neighs)
                        wall_to_remove = set(current_cell.walls_pos).intersection(neigh.walls_pos).pop()
                        # print(wall_to_remove)
                        # print(current_cell.walls_pos)
                        # print()
                        current_cell.walls_pos.remove(wall_to_remove)
                        neigh.walls_pos.remove(wall_to_remove)
                        current_cell = neigh
                        path.put(current_cell)
                    else :
                        current_cell = path.get()

                    self.update_screen(highlight_cells=list(path.queue))

                print('end')
                self.main_menu()

    def generate_by_prims(self):
        cells_in_maze = set()
        walls_list = set()
        first_cell = random.choice(self.cell_list)
        [walls_list.add(x) for x in first_cell.walls_pos]
        cells_in_maze.add(first_cell)
        while self.run:
            self.poll()
            if not self.pause:
                while walls_list :
                    wall = random.sample(walls_list,1)[0]
                    cells = self.find_cells_by_wall(wall)
                    # print("cells", cells)
                    if [x for x in cells if x not in cells_in_maze] :
                        for c in cells :
                            c.walls_pos.remove(wall)
                            [walls_list.add(w) for w in c.walls_pos]
                            cells_in_maze.add(c)
                            c.color= VISITED_COLOR

                    walls_list.remove(wall)
                    self.update_screen()
                
                print('end')
                self.main_menu()


    def generate_by_wilson(self):
        cells_not_maze = set(self.cell_list)
        cells_in_maze = set()

        cell = random.choice(self.cell_list)
        # cells_not_maze.remove(cell)
        cells_in_maze.add(cell)
        # input("cells in maze %s" % cells_in_maze )

        def cut_loops_in_path(path, large_cuts=True):
            # with large cut we cut the loop from the first occurence to the last occurence [0,1,2,3,1,2,3,1,7,4] cut 1 -> [0,1,7,4]
            # without we cut occurences in order of occurence [0,1,2,3,1,2,3,1,7,4] cut 1 -> [0,1,2,3,1,7,4]
            duplicates = True  
            while duplicates :
                duplicates = [x for x,y in Counter(path).items() if y >1]
                if duplicates :
                    elem = duplicates[0]
                    print('removing ', elem)
                    first_index = path.index(elem)
                    if large_cuts :
                        last_index = len(path)-1 - path[::-1].index(elem)
                    else :
                        last_index = path.index(elem, first_index + 1)
                    path = path[:first_index] + path[last_index:]
            return path
        
        while cells_not_maze :
            cell = random.sample(cells_not_maze,1)[0]
            #lets start a path
            path = []

            while True : 
                neighs = self.find_neighbours(cell)
                candidate = random.choice(neighs)
                print("Candidate %s" % candidate)
                # print(path)
                if candidate in cells_in_maze :
                    path = cut_loops_in_path(path)
                    for x in range(len(path)-1):
                        cell1=path[x]
                        cell2=path[x+1]
                        wall_to_remove = set(cell1.walls_pos).intersection(cell2.walls_pos).pop()
                        cell1.walls_pos.remove(wall_to_remove)
                        cell2.walls_pos.remove(wall_to_remove)
                    for c in path :
                        cells_not_maze.remove(c)
                        cells_in_maze.add(c)
                        c.color = VISITED_COLOR
                    self.update_screen()
                    break


                else :
                    path.append(candidate)
                    cell=candidate
                    print(cell)
                    self.update_screen(highlight_cells=path)





    def main_menu(self):
        print(f"{' MAIN MENU ':_^30}")
        print("1. Generate by random merge (Kruskal)")
        print("2. Generate by first depths search")
        print("3. Generate by Prim's Algorithm")
        print('q. Quit')
        print()
        resp=None
        while resp not in ['1', '2', '3', 'Q']:
            resp = str(input("Please enter a number\n")).upper().strip()

        if resp == "Q":
            print("Bye. Comme back soon !")
            return
        elif resp == '1' :
            self.reset_grid()
            self.generate_by_random_merge()
        elif resp == '2' :
            self.reset_grid()
            self.generate_by_depth_first_search()
        elif resp == '3' :
            self.reset_grid()
            self.generate_by_prims()
    
#import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    a=Maze()

