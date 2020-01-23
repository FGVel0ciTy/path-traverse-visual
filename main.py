# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np
import sys
from tile_queues import *
import os
import random
import time


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
        pygame.display.update((self.x * tile_width, self.y * tile_height, tile_width, tile_height))
        time.sleep(step_time)
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


def get_neighbor_coords(x, y, corners=True, distance=1, around=False, outside=False):
    # gets all valid neighboring coordinates including diagonals coords
    # Order is N, E, S, W, NE, SE, SW, NW
    neighbor_coords = [
        (x, y - distance),
        (x + distance, y),
        (x, y + distance),
        (x - distance, y)
    ]

    neighbor_coords = [neighbor for neighbor in neighbor_coords if
                       (outside or within_board(neighbor))
                       and (around or walkable(neighbor))]

    if not corners:
        return neighbor_coords

    diagonals_coords = [
        (x + distance, y - distance),
        (x + distance, y + distance),
        (x - distance, y + distance),
        (x - distance, y - distance)
    ]

    diagonals_coords = [diagonal for diagonal in diagonals_coords if
                        (outside or within_board(diagonal))
                        and (around or walkable(diagonal))
                        and (around or outside
                             or ((diagonal[0], y) in neighbor_coords or (x, diagonal[1]) in neighbor_coords))]

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

        neighbor_coords = get_neighbor_coords(current_tile.x, current_tile.y)
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


def dijkstra_search():
    start_tile.d = get_dijkstra_score(start_tile)
    open_queue = DijkstraQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        current_tile = open_queue.remove()

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = get_neighbor_coords(current_tile.x, current_tile.y)
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

        neighbor_coords = get_neighbor_coords(current_tile.x, current_tile.y)
        for x, y in neighbor_coords:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed" and grid[x, y].state != "start":
                if grid[x, y].state == "goal":
                    print(grid[x, y], "Goal reached")
                    grid[x, y].parent = current_tile
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile


def breadth_first_search():
    open_queue = [start_tile]

    while len(open_queue) != 0:
        current_tile = open_queue.pop(0)

        if current_tile.state != "start":
            current_tile.update_state("closed")

        neighbor_coords = get_neighbor_coords(current_tile.x, current_tile.y, False)
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

        neighbor_coords = reversed(get_neighbor_coords(current_tile.x, current_tile.y, False))
        for x, y in neighbor_coords:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed" and grid[x, y].state != "start":
                if grid[x, y].state == "goal":
                    grid[x, y].parent = current_tile
                    print(grid[x, y], "Goal reached")
                    return grid[x, y]
                open_queue.append(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile


def iterative_backtrack_maze():
    global start_tile
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x, y].state = "wall"
    screen.fill(colors["wall"])
    pygame.display.flip()

    start_x = random.randint(0, grid_width - 1)
    start_y = random.randint(0, grid_height - 1)

    while start_x % 2 == 0 or start_y % 2 == 0:
        start_x = random.randint(0, grid_width - 1)
        start_y = random.randint(0, grid_height - 1)

    open_queue = []
    x, y = start_x, start_y
    print(f"Maze starting at {x}, {y}")

    while x and y:
        while x and y:
            open_queue.append(grid[x, y])
            x, y = next_path(x, y)
        x, y = backtrack(open_queue)

    start_tile.update_state("normal")
    grid[start_tile.coord] = Tile(start_tile.coord)
    start_tile = grid[start_x, start_y] = Tile(start_x, start_y)
    start_tile.update_state("start")
    start_tile.g = 0

    goal_tile.update_state("goal")
    print("Finished Maze")


def next_path(x, y):
    one_away_tiles = get_neighbor_coords(x, y, corners=False, distance=1, around=True, outside=True)
    two_away_tiles = get_neighbor_coords(x, y, corners=False, distance=2, around=True, outside=True)
    if two_away_tiles:
        random_indexes = list(range(4))
        random.shuffle(random_indexes)
        for index in random_indexes:
            if within_board(two_away_tiles[index]) and grid[two_away_tiles[index]].state != "path":
                grid[two_away_tiles[index]].update_state("path")
                grid[one_away_tiles[index]].update_state("path")
                return two_away_tiles[index]
    return None, None


def backtrack(open_queue):
    while open_queue:
        x, y = open_queue.pop().coord
        two_away_tiles = get_neighbor_coords(x, y, corners=False, distance=2, around=True)
        two_away_tiles = [grid[coord] for coord in two_away_tiles if grid[coord].state != "path"
                          and grid[coord].state != "start"]

        if two_away_tiles:
            return x, y

    return None, None


def on_mouse_press():
    global start_tile
    global goal_tile
    global step_time

    step_time = 0

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

    step_time = 0 if fast_step else default_step_time


def get_solution(search_type):
    solution = searches[search_type]()
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
    global step_time
    step_time = 0

    if hard:
        screen.fill(colors["path"])
    for x in range(grid_width):
        for y in range(grid_height):
            if hard:
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

    step_time = 0 if fast_step else default_step_time


def change_search(index):
    global current_search_index
    if index == "next":
        if current_search_index >= len(searches) - 1:
            current_search_index = 0
        else:
            current_search_index += 1
    elif index == "back":
        if current_search_index <= 0:
            current_search_index = len(searches) - 1
        else:
            current_search_index += -1
    else:
        current_search_index = index
    pygame.display.set_caption(f"{search_names[current_search_index]} algorithm | "
                               f"{maze_names[current_maze_index]} maze generation")


def change_maze(index):
    global current_maze_index
    if index == "next":
        if current_maze_index >= len(mazes) - 1:
            current_maze_index = 0
        else:
            current_maze_index += 1
    elif index == "back":
        if current_maze_index <= 0:
            current_maze_index = len(mazes) - 1
        else:
            current_maze_index += -1
    else:
        current_maze_index = index
    pygame.display.set_caption(f"{search_names[current_search_index]} algorithm | "
                               f"{maze_names[current_maze_index]} maze generation")


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
search_names = [
    "A*",
    "Dijkstra",
    "Greedy",
    "DFS",
    "BFS"
]
searches = [
    a_star_search,
    dijkstra_search,
    greedy_first_search,
    depth_first_search,
    breadth_first_search
]
maze_names = [
    "Iterative"
]
mazes = [
    iterative_backtrack_maze
]

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

default_step_time = 0.00001
fast_step = False
step_time = default_step_time
current_search_index = 0
current_maze_index = 0
pygame.display.set_caption(f"{search_names[current_search_index]} algorithm | "
                           f"{maze_names[current_maze_index]} maze generation")

grid = np.empty((grid_width, grid_height), object)
for x_ in range(grid_width):
    for y_ in range(grid_height):
        grid[x_, y_] = Tile(x_, y_)
# Initial setup ^


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
                get_solution(current_search_index)
            if event.key == pygame.K_F5:
                reset_board(True)
            if event.key == pygame.K_m:
                reset_board(True)
                mazes[current_maze_index]()
            if event.key == pygame.K_RIGHT:
                change_search("next")
            if event.key == pygame.K_LEFT:
                change_search("back")
            if event.key == pygame.K_UP:
                change_maze("next")
            if event.key == pygame.K_DOWN:
                change_maze("back")
            if event.key == pygame.K_s:
                fast_step = not fast_step
                step_time = 0 if fast_step else default_step_time
                print(f"Fast step is {fast_step}")
        if True in pygame.mouse.get_pressed():
            on_mouse_press()

    pygame.display.flip()
