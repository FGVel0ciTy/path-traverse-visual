# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np
import sys
import time

colors = {
    "wall": (255, 255, 255),
    "closed": (0, 0, 255),
    "open": (102, 153, 255),
    "path": (0, 0, 0),
    "goal": (255, 153, 0),
    "start": (255, 0, 0),
    "solution": (0, 255, 0)
}
sys.setrecursionlimit(1000000000)
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
screen.fill(colors["wall"])


class Tile:
    def __init__(self, x, y, special=None, state="path"):
        self.x = x
        self.y = y
        self.state = state
        self.special = special

    def __repr__(self):
        return f"A {self.special} {self.state} @ {self.x},{self.y}"

    def mark_special(self, special):
        self.special = special
        pygame.draw.rect(screen, colors[special], (self.x * tile_width, self.y * tile_height, tile_width, tile_height))

    def update_state(self, state):
        if not self.special:
            self.state = state
            pygame.draw.rect(screen, colors[state], (self.x * tile_width, self.y * tile_height, tile_width, tile_height))
            pygame.display.update()


class AStarQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return " ".join([str(i) for i in self.queue])

    def __contains__(self, item):
        return item in self.queue

    def is_empty(self):
        return len(self.queue) == []

    def insert(self, item):
        self.queue.append(item)

    def remove(self):
        try:
            min_f_index = 0
            for index in range(len(self.queue)):
                if self.queue[index].f < self.queue[min_f_index].f:
                    min_f_index = index
            deleted_tile = self.queue[min_f_index]
            del self.queue[min_f_index]
            return deleted_tile
        except IndexError:
            print()
            exit()


class DijkstraQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return " ".join([str(i) for i in self.queue])

    def __contains__(self, item):
        return item in self.queue

    def is_empty(self):
        return len(self.queue) == []

    def insert(self, item):
        self.queue.append(item)

    def remove(self):
        try:
            min_g_index = 0
            for index in range(len(self.queue)):
                if self.queue[index].g < self.queue[min_g_index].g:
                    min_g_index = index
            deleted_tile = self.queue[min_g_index]
            del self.queue[min_g_index]
            return deleted_tile
        except IndexError:
            print()
            exit()


def get_distance(tile1, tile2):
    return math.sqrt(math.pow(abs(tile1.x - tile2.x), 2) + math.pow(abs(tile1.y - tile2.y), 2))


def get_traveled(tile):  # distance traveled from origin
    return tile.parent.g + get_distance(tile, tile.parent)


def get_total_cost(tile):  # f-score for A* path-finding
    return tile.h + tile.g


def within_board(x, y):
    return 0 <= x < board_width \
           and 0 <= y < board_height


def get_valid_neighbor_coords(x, y):
    # Order is N, E, S, W, NE, SE, SW, NW
    neighbors = [
        [x, y - 1],
        [x + 1, y],
        [x, y + 1],
        [x - 1, y],
        [x + 1, y - 1],
        [x + 1, y + 1],
        [x - 1, y + 1],
        [x - 1, y - 1]
    ]

    index = 0
    while index < len(neighbors):
        neighbor = neighbors[index]
        x = neighbor[0]
        y = neighbor[1]
        if not within_board(x, y):
            neighbors.remove([x, y])
        else:
            index = index + 1

    return neighbors


board_height = 100
board_width = 100

tile_width = 1000 / board_width
tile_height = 1000 / board_height

grid = np.empty((board_width, board_height), object)
for x_ in range(board_width):
    for y_ in range(board_height):
        grid[x_, y_] = Tile(x_, y_)

goal_tile = grid[90, 5]
goal_tile.mark_special("goal")

start_tile = grid[25, 20]
start_tile.g = 0
start_tile.mark_special("start")

for x_ in range(board_width):
    for y_ in range(board_height):
        grid[x_, y_].h = get_distance(grid[x_, y_], goal_tile)

start_tile.f = get_total_cost(start_tile)


def a_star_search(start: Tile):
    open_queue = AStarQueue()
    open_queue.insert(start)
    closed = []

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        if best_tile.special == "goal":
            print(best_tile, "Goal reached")
            return best_tile

        best_tile.update_state("closed")
        closed.append(best_tile)
        neighbors = get_valid_neighbor_coords(best_tile.x, best_tile.y)
        print(best_tile)
        for x, y in neighbors:
            if grid[x, y] in closed:
                continue
            if not (grid[x, y] in open_queue):
                grid[x, y].g = best_tile.g + get_distance(grid[x, y], best_tile)
                grid[x, y].f = get_total_cost(grid[x, y])
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")

            new_g = best_tile.g + get_distance(grid[x, y], best_tile)
            if new_g >= grid[x, y].g:
                try:
                    grid[x, y].parent
                except:
                    grid[x, y].parent = best_tile
                continue

            grid[x, y].parent = best_tile
            grid[x, y].g = new_g
            grid[x, y].f = get_total_cost(grid[x, y])

    return None


def dijkstra_search(start: Tile):
    open_queue = DijkstraQueue()
    open_queue.insert(start)
    closed = []

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        if best_tile.special == "goal":
            print(best_tile, "Goal reached")
            return best_tile

        best_tile.update_state("closed")
        closed.append(best_tile)
        neighbors = get_valid_neighbor_coords(best_tile.x, best_tile.y)
        print(best_tile)
        for x, y in neighbors:
            if grid[x, y] in closed:
                continue
            if not (grid[x, y] in open_queue):
                grid[x, y].g = best_tile.g + get_distance(grid[x, y], best_tile)
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")

            new_g = best_tile.g + get_distance(grid[x, y], best_tile)
            if new_g >= grid[x, y].g:
                try:
                    grid[x, y].parent
                except:
                    grid[x, y].parent = best_tile
                continue

            grid[x, y].parent = best_tile
            grid[x, y].g = new_g

    return None


def depth_first_search(current_tile: Tile):
    neighbors = get_valid_neighbor_coords(current_tile.x, current_tile.y)

    print(current_tile, f"Traveled: {current_tile.g} units")

    if current_tile.special == "goal":
        return current_tile

    current_tile.update_state("closed")

    for x, y in neighbors:
        if grid[x, y].state != "closed":
            grid[x, y].parent = current_tile
            grid[x, y].g = get_traveled(grid[x, y])
            return depth_first_search(grid[x, y])

    return None


solution: Tile = a_star_search(start_tile)
while True:
    try:
        solution.parent.mark_special("solution")
        solution = solution.parent
    except:
        solution.mark_special("start")
        break

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()
