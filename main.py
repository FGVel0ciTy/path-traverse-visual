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
for x in range(board_width + 1):
    temp = []
    for y in range(board_height + 1):
        temp.append(Tile([x, y]))
    grid.append(temp)

start_tile = grid[0][0]
start_tile.g = 0

goal_tile = grid[5][10]
goal_tile.state = "goal"


def a_star_search(start: Tile, goal: Tile, steps=0, seen=[]):
    neighbors = [
        [start.coord[0], start.coord[1] + 1],
        [start.coord[0] + 1, start.coord[1] + 1],
        [start.coord[0] + 1, start.coord[1]],
        [start.coord[0] + 1, start.coord[1] - 1],
        [start.coord[0], start.coord[1] - 1],
        [start.coord[0] - 1, start.coord[1] - 1],
        [start.coord[0] - 1, start.coord[1]],
        [start.coord[0] - 1, start.coord[1] + 1],
    ]

    if start.coord == goal.coord:
        return steps

    if start.coord not in seen:
        seen.append(start.coord)
        for neighbor in neighbors:
            if 0 <= neighbor[0] <= board_width\
                    and 0 <= neighbor[1] <= board_height:
                return a_star_search(grid[neighbor[0]][neighbor[1]], goal, steps + 1, seen)

    return False


print(a_star_search(start_tile, goal_tile))
