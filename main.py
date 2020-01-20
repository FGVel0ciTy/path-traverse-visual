# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np
import sys
from tile_queues import *
import os
import random


class Tile:
    def __init__(self, coord1, coord2=0, weight=1, state="path"):
        # This piece throughout the file is to allow tuples/lists to be used alongside x, y notation
        if isinstance(coord1, int):
            self.x = coord1
            self.y = coord2
        else:
            self.x, self.y = coord1
        self.coord = (self.x, self.y)
        self.weight = weight
        self.state = state

    def __repr__(self):
        return f"A {self.state} @ {self.x},{self.y}"

    def update_state(self, state):
        self.state = state
        pygame.draw.rect(screen, colors[state], (self.x * tile_width, self.y * tile_height, tile_width, tile_height))
        pygame.display.update()
        return self.state


def get_distance(tile1, tile2):  # Euclidean distance between two points
    return math.sqrt(math.pow(tile1.x - tile2.x, 2) + math.pow(tile1.y - tile2.y, 2))


def get_distance_manhattan(tile1, tile2):  # Manhattan distance between two points
    return math.pow(tile1.x - tile2.x, 2) + math.pow(tile1.y - tile2.y, 2)


def get_traveled(tile):  # distance traveled from origin
    return tile.parent.g + get_distance(tile, tile.parent)


def get_dijkstra_score(tile):  # retrieve the tile's cost
    return tile.g * tile.weight


def get_f_score(tile):  # f-score for A* path-finding
    return tile.h + get_dijkstra_score(tile)


def within_board(coord1, coord2=0):  # checks if coords are in board
    if isinstance(coord1, int):
        x = coord1
        y = coord2
    else:
        x, y = coord1
    return 0 <= x < grid_width and 0 <= y < grid_height


def walkable(coord1, coord2=0):  # checks if its a wall
    if isinstance(coord1, int):
        x = coord1
        y = coord2
    else:
        x, y = coord1
    return grid[x, y].state != "wall"


def get_valid_neighbor_coords(x, y, corners=True):  # gets all valid neighboring coordinates including diagonals coords
    # Order is N, E, S, W, NE, SE, SW, NW
    neighbor_coords = [
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y)
    ]

    neighbor_coords = [neighbor for neighbor in neighbor_coords if within_board(neighbor) and walkable(neighbor)]

    if not corners:
        return neighbor_coords

    diagonals_coords = [
        (x + 1, y - 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x - 1, y - 1)
    ]

    diagonals_coords = [diagonal for diagonal in diagonals_coords if within_board(diagonal) and walkable(diagonal)
                        and ((diagonal[0], y) in neighbor_coords or (x, diagonal[1]) in neighbor_coords)]

    neighbor_coords += diagonals_coords
    return neighbor_coords


def get_all_neighbor_coords(x, y, corners=True):  # gets all the neighboring coordinates including diagonals coords
    # Order is N, E, S, W, NE, SE, SW, NW
    neighbor_coords = [
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y)
    ]

    neighbor_coords = [neighbor for neighbor in neighbor_coords if within_board(neighbor)]

    if not corners:
        return neighbor_coords

    diagonals_coords = [
        (x + 1, y - 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x - 1, y - 1)
    ]

    diagonals_coords = [diagonal for diagonal in diagonals_coords if within_board(diagonal)]

    neighbor_coords += diagonals_coords
    return neighbor_coords


def a_star_search():
    # This sets the heuristic score for every tile
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x, y].h = get_distance(grid[x, y], goal_tile)

    start_tile.f = get_f_score(start_tile)
    open_queue = AStarQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        current_tile = open_queue.remove()

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = get_valid_neighbor_coords(current_tile.x, current_tile.y)
        for x, y in neighbor_coords:
            if grid[x, y].state == "closed" or grid[x, y].state == "start":
                continue

            new_g = current_tile.g + get_distance(grid[x, y], current_tile)

            try:
                if new_g < grid[x, y].g:
                    grid[x, y].g = new_g
                    grid[x, y].parent = current_tile
            except:
                grid[x, y].g = new_g
                grid[x, y].parent = current_tile

            grid[x, y].f = get_f_score(grid[x, y])

            if grid[x, y] not in open_queue:
                if grid[x, y].state == "goal":
                    print(grid[x, y], f"Goal reached after {grid[x, y].g} units traveled")
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")

    return None


def dijkstra_search():
    start_tile.d = get_dijkstra_score(start_tile)
    open_queue = DijkstraQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        current_tile = open_queue.remove()

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = get_valid_neighbor_coords(current_tile.x, current_tile.y)
        for x, y in neighbor_coords:
            if grid[x, y].state == "closed" or grid[x, y].state == "start":
                continue

            new_g = current_tile.g + get_distance(grid[x, y], current_tile)

            try:
                if new_g < grid[x, y].g:
                    grid[x, y].g = new_g
                    grid[x, y].parent = current_tile
            except:
                grid[x, y].g = new_g
                grid[x, y].parent = current_tile

            grid[x, y].d = get_dijkstra_score(grid[x, y])

            if grid[x, y] not in open_queue:
                if grid[x, y].state == "goal":
                    print(grid[x, y], f"Goal reached after {grid[x, y].g} units traveled")
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")

    return None


def greedy_first_search():
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x, y].h = get_distance(grid[x, y], goal_tile)

    open_queue = GreedyQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        current_tile = open_queue.remove()

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = get_valid_neighbor_coords(current_tile.x, current_tile.y)
        for x, y in neighbor_coords:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed" and grid[x, y].state != "start":
                if grid[x, y].state == "goal":
                    print(grid[x, y], "Goal reached")
                    grid[x, y].parent = current_tile
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile

    return None


def breadth_first_search():
    open_queue = [start_tile]

    while len(open_queue) != 0:
        current_tile = open_queue.pop(0)

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = get_valid_neighbor_coords(current_tile.x, current_tile.y)
        for x, y in neighbor_coords:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed" and grid[x, y].state != "start":
                if grid[x, y].state == "goal":
                    grid[x, y].parent = current_tile
                    print(grid[x, y], "Goal reached")
                    return grid[x, y]
                open_queue.append(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile


def depth_first_search():
    open_queue = [start_tile]

    while len(open_queue) != 0:
        current_tile = open_queue.pop()

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = reversed(get_valid_neighbor_coords(current_tile.x, current_tile.y, False))
        for x, y in neighbor_coords:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed" and grid[x, y].state != "start":
                if grid[x, y].state == "goal":
                    grid[x, y].parent = current_tile
                    print(grid[x, y], "Goal reached")
                    return grid[x, y]
                open_queue.append(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile


def recursive_backtrack():  # CURRENTLY BROKEN
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x, y].state = "wall"
    screen.fill(colors["wall"])
    start_tile.update_state("start")
    goal_tile.update_state("goal")

    open_queue = [start_tile]
    closed = [start_tile]

    while len(open_queue) > 0:
        current_tile = open_queue.pop()
        neighbor_coords = get_all_neighbor_coords(current_tile.x, current_tile.y, False)
        neighbor_coords = [coord for coord in neighbor_coords if grid[coord] not in closed]
        if neighbor_coords:
            random_index = random.randint(0, len(neighbor_coords) - 1)
            next_tile = grid[neighbor_coords[random_index]]
            next_tile.update_state("path")
            closed += [grid[coord] for coord in neighbor_coords]
            open_queue.append(next_tile)
    print("Finished Maze")


def on_mouse_press():
    global start_tile
    global goal_tile
    mx, my = pygame.mouse.get_pos()
    x = mx // (display_width // grid_width)
    y = my // (display_height // grid_height)
    rb, mb, lb = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    print(mx, my)
    print(rb, mb, lb)
    if rb:
        if keys[pygame.K_LCTRL]:
            if not grid[x, y] == goal_tile:
                start_tile.update_state("normal")
                grid[start_tile.coord] = Tile(start_tile.coord)
                grid[x, y] = Tile(x, y)
                start_tile = grid[x, y]
                start_tile.update_state("start")
                start_tile.g = 0
        elif keys[pygame.K_LALT]:
            if not grid[x, y] == start_tile:
                goal_tile.update_state("normal")
                grid[goal_tile.coord] = Tile(goal_tile.coord)
                grid[x, y] = Tile(x, y)
                goal_tile = grid[x, y]
                goal_tile.update_state("goal")
        else:
            if grid[x, y] != goal_tile and grid[x, y] != start_tile:
                grid[x, y].update_state("normal")
                grid[x, y].update_state("wall")
    elif lb:
        if grid[x, y].state == "wall":
            grid[x, y].update_state("path")


def get_solution(search_type):
    solution: Tile = searches[search_type]()
    if solution:
        while True:
            try:
                solution.parent.update_state("solution")
                solution = solution.parent
            except:
                solution.update_state("start")
                print("Solution Found")
                break


def reset_board(hard=True):
    global grid
    global start_tile
    global goal_tile

    for x in range(grid_width):
        for y in range(grid_height):
            if hard:
                screen.fill(colors["path"])
                grid[x, y] = Tile(x, y)
            else:
                if grid[x, y].state == "solution" or grid[x, y].state == "open" or grid[x, y].state == "closed":
                    grid[x, y] = Tile(x, y)
                    grid[x, y].update_state("path")

    start_tile = grid[start_tile.coord] = Tile(start_tile.coord)
    start_tile.update_state("start")
    start_tile.g = 0

    goal_tile = grid[goal_tile.coord] = Tile(goal_tile.coord)
    goal_tile.update_state("goal")


def change_algorithm(algorithm):
    global current_search
    current_search = algorithm
    pygame.display.set_caption(f"{current_search} algorithm")


# Initial setup
colors = {
    "wall": (0, 0, 0),
    "closed": (0, 0, 255),
    "open": (102, 153, 255),
    "path": (255, 255, 255),
    "normal": (255, 255, 255),
    "goal": (255, 153, 0),
    "start": (255, 0, 0),
    "solution": (0, 255, 0)
}
searches = {
    "dijkstra's": dijkstra_search,
    "a*": a_star_search,
    "dfs": depth_first_search,
    "bfs": breadth_first_search,
    "greedy": greedy_first_search
}
mazes = {
    "recursive": recursive_backtrack
}

display_width = 800
display_height = 800
grid_height = 100
grid_width = 100
tile_width = display_width // grid_width
tile_height = display_height // grid_height

os.environ['SDL_VIDEO_CENTERED'] = "0"
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
screen.fill(colors["path"])
current_search = "a*"
pygame.display.set_caption(f"{current_search} algorithm")

grid = np.empty((grid_width, grid_height), object)
for x_ in range(grid_width):
    for y_ in range(grid_height):
        grid[x_, y_] = Tile(x_, y_)
# Initial setup


goal_tile = grid[99, 99]
goal_tile.update_state("goal")

start_tile = grid[0, 0]
start_tile.g = 0
start_tile.update_state("start")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Quitting")
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                print("Getting Solution")
                reset_board(False)
                get_solution(current_search)
            if event.key == pygame.K_F5:
                print("Refreshing")
                reset_board(True)
            if event.key == pygame.K_m:
                mazes["recursive"]()
            if event.key == pygame.K_a:
                change_algorithm("a*")
            if event.key == pygame.K_d:
                change_algorithm("dijkstra's")
            if event.key == pygame.K_b:
                change_algorithm("bfs")
            if event.key == pygame.K_EQUALS:
                change_algorithm("dfs")
            if event.key == pygame.K_g:
                change_algorithm("greedy")
        if True in pygame.mouse.get_pressed():
            on_mouse_press()

    pygame.display.flip()
