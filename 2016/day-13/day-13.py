from enum import Enum
from typing import Callable, List, Tuple

# custom types
Cell = Tuple[int, int]
Maze = Tuple[int, int, List[List[bool]]]
MazeSeed = Callable[[int, int], bool]
Path = List[Cell]


# generate_maze creates a new maze using a seed and [width x height] dimensions
def generate_maze(seed: MazeSeed, width: int, height: int) -> Maze:
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(seed(x, y))
        rows.append(row)
    return width, height, rows


# neighbours returns all cells that can be moved to from a starting cell
def neighbours(cell: Cell, maze: Maze) -> [Cell]:

    # unpack tuple parameters
    current_x, current_y = cell
    width, height, maze_cells = maze

    # calculate coordinates of neighbours
    down, up = min(height - 1, current_y + 1), max(0, current_y - 1)
    left, right = max(0, current_x - 1), min(width - 1, current_x + 1)
    ns = [(left, current_y), (right, current_y), (current_x, down), (current_x, up)]

    # filter down possible neighbours
    for (x, y) in ns:
        if maze_cells[y][x]:
            yield x, y


# visited returns whether a cell has been visited in a path
def visited(path: Path, cell: Cell) -> bool:
    for neighbour in path:
        if equal(cell, neighbour):
            return True
    return False


def equal(a: Cell, b: Cell) -> bool:
    return a[0] == b[0] and a[1] == b[1]


def shortest_path(start: Cell, end: Cell, maze: Maze) -> Path:
    paths = [[start]]
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            last_visited = path[-1]
            if equal(last_visited, end):
                return path
            next_visited = neighbours(last_visited, maze)
            unvisited = filter(lambda cell: not visited(path, cell), next_visited)
            for u in unvisited:
                new_paths.append(path[:] + [u])
        paths = new_paths
    return []


if __name__ == "__main__":
    favourite_number = 10

    def test_seed(x: int, y: int) -> bool:
        h = x*x + 3*x + 2*x*y + y + y*y + favourite_number
        h = "{0:b}".format(h)
        return h.count("1") % 2 == 0

    mz = generate_maze(test_seed, 10, 7)
    p = shortest_path((1, 1), (7, 4), mz)
    print(len(p))
