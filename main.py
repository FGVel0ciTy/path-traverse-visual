# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np

board_height = 10
board_width = 10


class Tile:
    def __init__(self, x, y, state="path"):
        self.x = x
        self.y = y
        self.state = state

    def __repr__(self):
        return f"State {self.state} @ {self.x},{self.y}"


def get_distance(tile1, tile2):
    return math.sqrt(math.pow(abs(tile1.x - tile2.x), 2) + math.pow(abs(tile1.y - tile2.y), 2))


def get_traveled(tile):  # distance traveled from origin
    return tile.parent.g + get_distance(tile, tile.parent)


def get_total_cost(tile):  # f-score for A* path-finding
    return tile.h + tile.g


def within_board(x, y):
    return 0 <= x <= board_width \
           and 0 <= y <= board_height


grid = np.empty((board_width + 1, board_height + 1), object)
for x_ in range(board_width + 1):
    for y_ in range(board_height + 1):
        grid[x_, y_] = Tile(x_, y_)

goal_tile = grid[10, 5]
goal_tile.state = "goal"

start_tile = grid[0, 0]
start_tile.g = 0

for x_ in range(board_width + 1):
    for y_ in range(board_height + 1):
        grid[x_, y_].h = get_distance(grid[x_, y_], goal_tile)

start_tile.f = get_total_cost(start_tile)


def a_star_search(current_tile: Tile, goal: Tile):
    neighbors = [
        [current_tile.x, current_tile.y + 1],
        [current_tile.x + 1, current_tile.y + 1],
        [current_tile.x + 1, current_tile.y],
        [current_tile.x + 1, current_tile.y - 1],
        [current_tile.x, current_tile.y - 1],
        [current_tile.x - 1, current_tile.y - 1],
        [current_tile.x - 1, current_tile.y],
        [current_tile.x - 1, current_tile.y + 1]
    ]

    print(current_tile, f"Heuristic Score: {current_tile.h} units")

    if current_tile.state == "goal":
        return current_tile.g

    if current_tile.state != "seen":
        current_tile.state = "seen"
        for x, y in neighbors:
            if within_board(x, y) and \
                    grid[x, y].state != "seen":
                grid[x, y].parent = current_tile
                grid[x, y].g = get_traveled(grid[x, y])
                grid[x, y].f = get_total_cost(grid[x, y])
                return a_star_search(grid[x, y], goal)

    return -1


def depth_first_search(current_tile: Tile, goal: Tile):
    neighbors = [
        [current_tile.x, current_tile.y + 1],
        [current_tile.x + 1, current_tile.y + 1],
        [current_tile.x + 1, current_tile.y],
        [current_tile.x + 1, current_tile.y - 1],
        [current_tile.x, current_tile.y - 1],
        [current_tile.x - 1, current_tile.y - 1],
        [current_tile.x - 1, current_tile.y],
        [current_tile.x - 1, current_tile.y + 1]
    ]

    print(current_tile, f"Traveled: {current_tile.g} units")

    if current_tile.state == "goal":
        return current_tile.g

    if current_tile.state != "seen":
        current_tile.state = "seen"
        for x, y in neighbors:
            if within_board(x, y) and \
                    grid[x, y].state != "seen":
                grid[x, y].parent = current_tile
                grid[x, y].g = get_traveled(grid[x, y])
                return depth_first_search(grid[x, y], goal)

    return -1


print(a_star_search(start_tile, goal_tile))
