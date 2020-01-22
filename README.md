
## path-traverse-visual
This project is basically a bunch of path searching algorithms visualized. So far you can make paths (place/destroy walls), move the goal/start, generate mazes, and do the searches. The searching algorithms that I have implemented is A*, Dijkstra, Breadth First, Depth First, and Greedy First Searches. The maze algorithm so far is recursive/iterative backtracking

## Setting Up
You must have a python environment with [PyGame](https://www.pygame.org/) and the [NumPy](https://numpy.org/) modules.

This install line should do the trick: ```pip install pygame numpy```

After that you can just run the main.py file and get started

## Controls
Placing walls - Left Mouse Click

Destroying walls - Right Mouse Click

Moving start - Ctrl+Left Mouse Click

Moving goal - Ctrl+Left Mouse Click

Changing Algorithms (Just press specified key):
  - A*: a
  - Dijkstra: d
  - Breadth First Search: b
  - Greedy First Search: g
  - Depth First Search: =
  
Reset Grid - F5

Generate Maze - m

Fast Step (No sleep timer between steps) - s

Start Algorithm - Return or Enter

## Problems
* When there is no path, the program auto closes
* Sometimes PyGame doesn't update so the program will "freeze." Just let it run and the algorithm will finish up and update it at the end

## Future Goals
* Optimize how I implement the algorithms (They are kind of jank rn)
* Add Play/Pausing
* Randomly generate mazes
* Fix the bugs

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE used
* [PyGame](https://www.pygame.org/) - Visuals
* [NumPy](https://numpy.org/) - Grid System

## Authors

* **Vel0ciTy** - *Main Author* - [Finally got one!](https://lecongkhoiviet.netlify.com/) 😁

## Acknowledgments

* StackOverflow 😀
* [Medium](https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2)
* [Stanford CS](http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html)
* Wikipedia
* A bunch of other sites
