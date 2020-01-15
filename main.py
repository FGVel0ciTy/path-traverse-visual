# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np
import sys
import time

screen = pygame.display.set_mode((1000, 1000))
colors = {
    "wall": (255, 255, 255),
    "seen": (0, 0, 255),
    "path": (0, 0, 0),
    "goal": (0, 255, 0),
    "start": (255, 0, 0)
}
sys.setrecursionlimit(1000000000)


class Tile:
    def __init__(self, x, y, state="path"):
        self.x = x
        self.y = y
        self.state = state

    def __repr__(self):
        return f"State {self.state} @ {self.x},{self.y}"

    def update_state(self, state):
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
    neighbors = [
        [x, y - 1],
        [x + 1, y],
        [x, y + 1],
        [x - 1, y],
        [x + 1, y - 1],
        [x + 1, y + 1],
        [x - 1, y - 1],
        [x - 1, y + 1]
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

goal_tile = grid[0, 80]
goal_tile.update_state("goal")

start_tile = grid[49, 49]
start_tile.g = 0
start_tile.update_state("start")

for x_ in range(board_width):
    for y_ in range(board_height):
        grid[x_, y_].h = get_distance(grid[x_, y_], goal_tile)

start_tile.f = get_total_cost(start_tile)


def a_star_search(start: Tile, goal: Tile):
    open_queue = AStarQueue()
    open_queue.insert(start)
    closed = []

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        if best_tile.state == "goal":
            print(best_tile, "Goal reached")
            return True

        best_tile.update_state("seen")
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

            new_g = best_tile.g + get_distance(grid[x, y], best_tile)
            if new_g >= grid[x, y].g:
                continue

            grid[x, y].parent = best_tile
            grid[x, y].g = new_g
            grid[x, y].f = get_total_cost(grid[x, y])

    return False


def dijkstra_search(start: Tile, goal: Tile):
    open_queue = DijkstraQueue()
    open_queue.insert(start)
    closed = []

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        if best_tile.state == "goal":
            print(best_tile, "Goal reached")
            return True

        best_tile.update_state("seen")
        closed.append(best_tile)
        neighbors = get_valid_neighbor_coords(best_tile.x, best_tile.y)
        print(best_tile)
        for x, y in neighbors:
            if grid[x, y] in closed:
                continue
            if not (grid[x, y] in open_queue):
                grid[x, y].g = best_tile.g + get_distance(grid[x, y], best_tile)
                open_queue.insert(grid[x, y])

            new_g = best_tile.g + get_distance(grid[x, y], best_tile)
            if new_g >= grid[x, y].g:
                continue

            grid[x, y].parent = best_tile
            grid[x, y].g = new_g

    return False


def depth_first_search(current_tile: Tile, goal: Tile):
    neighbors = get_valid_neighbor_coords(current_tile.x, current_tile.y)

    print(current_tile, f"Traveled: {current_tile.g} units")

    if current_tile.state == "goal":
        return True

    current_tile.update_state("seen")

    for x, y in neighbors:
        if grid[x, y].state != "seen":
            grid[x, y].parent = current_tile
            grid[x, y].g = get_traveled(grid[x, y])
            return depth_first_search(grid[x, y], goal)

    return False


print(dijkstra_search(start_tile, goal_tile))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()
