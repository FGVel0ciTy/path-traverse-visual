# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np
import sys
from tile_queues import *
import os

colors = {
    "wall": (0, 0, 0),
    "closed": (0, 0, 255),
    "open": (102, 153, 255),
    "path": (255, 255, 255),
    "goal": (255, 153, 0),
    "start": (255, 0, 0),
    "solution": (0, 255, 0)
}
display_width = 800
display_height = 800
sys.setrecursionlimit(1000000000)
os.environ['SDL_VIDEO_CENTERED'] = "0"
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
screen.fill(colors["path"])


class Tile:
    def __init__(self, x, y, weight=0, special=None, state="path"):
        self.x = x
        self.y = y
        self.weight = weight
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


def get_distance(tile1, tile2):
    return math.sqrt(math.pow(abs(tile1.x - tile2.x), 2) + math.pow(abs(tile1.y - tile2.y), 2))


def get_traveled(tile):  # distance traveled from origin
    return tile.parent.g + get_distance(tile, tile.parent)


def get_dijkstra_score(tile):
    return tile.g + tile.weight


def get_total_cost(tile):  # f-score for A* path-finding
    return tile.h + tile.g


def within_board(x, y):
    return 0 <= x < grid_width \
           and 0 <= y < grid_height


def walkable(x, y):
    return not grid[x, y].state == "wall"


def get_valid_neighbor_coords(x, y):
    # Order is N, E, S, W, NE, SE, SW, NW
    neighbors = [
        [x, y - 1],
        [x + 1, y],
        [x, y + 1],
        [x - 1, y]
    ]

    diagonals = [
        [x + 1, y - 1],
        [x + 1, y + 1],
        [x - 1, y + 1],
        [x - 1, y - 1]
    ]

    index = 0
    while index < len(neighbors):
        neighbor = neighbors[index]
        xn = neighbor[0]
        yn = neighbor[1]
        if not within_board(xn, yn) \
                or not walkable(xn, yn):
            neighbors.remove([xn, yn])
        else:
            index = index + 1

    index = 0
    while index < len(diagonals):
        diagonal = diagonals[index]
        xd = diagonal[0]
        yd = diagonal[1]
        if not within_board(xd, yd) \
                or not walkable(xd, yd) \
                or (grid[xd, y] and grid[x, yd] not in neighbors):
            diagonals.remove([xd, yd])
        else:
            index = index + 1

    neighbors += diagonals
    return neighbors


grid_height = 100
grid_width = 100

tile_width = display_width // grid_width
tile_height = display_height // grid_height

grid = np.empty((grid_width, grid_height), object)
for x_ in range(grid_width):
    for y_ in range(grid_height):
        grid[x_, y_] = Tile(x_, y_)

goal_tile = grid[75, 85]
goal_tile.mark_special("goal")

start_tile = grid[0, 0]
start_tile.g = 0
start_tile.mark_special("start")

for x_ in range(grid_width):
    for y_ in range(grid_height):
        grid[x_, y_].h = get_distance(grid[x_, y_], goal_tile)


def a_star_search(start: Tile):
    start_tile.f = get_total_cost(start_tile)
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
    start_tile.d = get_total_cost(start_tile)
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
                grid[x, y].d = get_dijkstra_score(grid[x, y])
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
            grid[x, y].d = get_dijkstra_score(grid[x, y])

    return None


def breadth_first_search(start: Tile):
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


def depth_helper(current_tile: Tile):
    neighbors = get_valid_neighbor_coords(current_tile.x, current_tile.y)

    print(current_tile, f"Traveled: {current_tile.g} units")

    if current_tile.special == "goal":
        return current_tile

    current_tile.update_state("closed")

    for x, y in neighbors:
        if grid[x, y].state != "closed":
            grid[x, y].parent = current_tile
            grid[x, y].g = get_traveled(grid[x, y])
            possible_path = depth_first_search(grid[x, y])
            if possible_path:
                return possible_path


def depth_first_search(start: Tile):
    neighbors = get_valid_neighbor_coords(start.x, start.y)

    print(start, f"Traveled: {start.g} units")

    if start.special == "goal":
        return start

    start.update_state("closed")

    for x, y in neighbors:
        if grid[x, y].state != "closed":
            grid[x, y].parent = start
            grid[x, y].g = get_traveled(grid[x, y])
            possible_path = depth_first_search(grid[x, y])
            if possible_path:
                return possible_path

    return None


def on_mouse_press():
    mx, my = pygame.mouse.get_pos()
    rb, mb, lb = pygame.mouse.get_pressed()
    print(mx, my)
    print(rb, mb, lb)
    if rb == 1:
        x = mx // (display_width // grid_width)
        y = my // (display_height // grid_height)
        grid[x, y].update_state("wall")


def get_solution():
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
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            get_solution()
        if True in pygame.mouse.get_pressed():
            on_mouse_press()

    pygame.display.flip()
