from enum import Enum
import typing
from hashlib import md5


class Step(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


Maze = typing.Tuple[int, int]
Cell = typing.Tuple[int, int]
Steps = typing.List[Step]
Path = typing.Tuple[Cell, Steps]
RoomSeed = typing.Callable[[Steps], typing.Tuple[bool, bool, bool, bool]]


def neighbours(seed: RoomSeed, path: Path, maze: Maze) -> [Step, Cell]:
    current, steps = path
    current_x, current_y = current
    width, height = maze

    down, up = min(height - 1, current_y + 1), max(0, current_y - 1)
    left, right = max(0, current_x - 1), min(width - 1, current_x + 1)

    up, down, left, right = (current_x, up), (current_x, down), (left, current_y), (right, current_y)
    can_up, can_down, can_left, can_right = seed(steps)
    if can_up and up != current:
        yield Step.UP, up
    if can_down and down != current:
        yield Step.DOWN, down
    if can_left and left != current:
        yield Step.LEFT, left
    if can_right and right != current:
        yield Step.RIGHT, right


def shortest_path(seed: RoomSeed, start: Cell, end: Cell, maze: Maze) -> Steps:
    paths = [(start, [])]
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            current, steps = path
            if current == end:
                return steps
            next_steps = neighbours(seed, path, maze)
            for (next_step, next_coordinate) in next_steps:
                new_path = (next_coordinate, steps[:] + [next_step])
                new_paths.append(new_path)
        paths = new_paths
    return []


def decode_steps(steps: str) -> Steps:
    return list(map(lambda step: Step(step), steps))


if __name__ == "__main__":

    puzzle_input = "hijkl"

    def test_seed(seed: str) -> RoomSeed:
        def _test_seed(steps: Steps) -> (bool, bool, bool, bool):
            ss = "".join(map(lambda s: str(s.value), steps))
            key = seed + ss
            out = md5(str.encode(key)).hexdigest()[:4]
            u, d, l, r = list(map(lambda k: k in "bcdef", out))
            return u, d, l, r
        return _test_seed


    assert shortest_path(test_seed("ihgpwlah"), (0, 0), (3, 3), (4, 4)) == decode_steps("DDRRRD")

    assert shortest_path(test_seed("kglvqrro"), (0, 0), (3, 3), (4, 4)) == decode_steps("DDUDRLRRUDRD")

    assert shortest_path(test_seed("ulqzkmiv"), (0, 0), (3, 3), (4, 4)) == decode_steps("DRURDRUDDLLDLUURRDULRLDUUDDDRR")
