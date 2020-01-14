# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame

board_height = 10
board_width = 10


class Tile:
    def __init__(self, coordinates, state="path"):
        self.coord = coordinates
        self.state = state

    def __repr__(self):
        return f"State {self.state} @ {self.coord[0]},{self.coord[1]}"


def get_distance(tile1, tile2):
    return math.sqrt(
        math.pow(abs(tile1.coord[0] - tile2.coord[0]), 2) +
        math.pow(abs(tile1.coord[1] - tile2.coord[1]), 2)
    )


def get_traveled(tile):  # distance traveled from origin
    return tile.parent.g + get_distance(tile, tile.parent)


def get_total_cost(tile):  # f-score for A* path-finding
    return tile.h + tile.g


grid = []
for x in range(board_width):
    for y in range(board_height):
        grid[x, y] = Tile(x, y)

start_tile = grid[0, 0]
start_tile.g = 0

goal_tile = grid[10, 10]


def a_star_search(start: Tile, end: Tile):
    neighbors = []

