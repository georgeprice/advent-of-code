from functools import reduce

ORIENTATIONS = ["N", "E", "S", "W"]


def solve(steps: str) -> int:
    steps = map(str_to_step, steps.split(', '))
    final_state = reduce(update_state, steps, (0, 0, 'N'))
    return sum(map(abs, [final_state[0], final_state[1]]))


visited = set()


def update_state(prev: (int, int, str), curr: (str, int)) -> (int, int, str):
    # unpacking tuple values for previous state and current step command
    x, y, direction = prev
    rot, amount = curr

    # update the direction and coordinates
    new_dir = _update_direction(direction, rot)
    new_coordinates = (0, 0, "")
    for visited_coordinates in _get_path((x, y), new_dir, amount):
        _key = "({},{})".format(*visited_coordinates)
        if _key in visited:
            print("Already visited: {}".format(_key))
        else:
            visited.add(_key)
        new_coordinates = visited_coordinates
    return new_coordinates[0], new_coordinates[1], new_dir


def _get_path(old: (int, int), direction: str, distance: int) -> [(int, int)]:
    start = -1 if distance < 0 else 1
    step = start
    end = distance + start
    if direction in ["E", "W"]:
        for move in range(start, end, step):
            yield old[0], old[1] + (move if direction == "E" else -move)
    else:
        for move in range(start, end, step):
            yield old[0] + (move if direction == "N" else -move), old[1]


def _update_direction(direction: str, rotation: str) -> str:
    new_dir = ORIENTATIONS.index(direction) + (1 if rotation == 'R' else -1)
    return ORIENTATIONS[(new_dir + 4) if new_dir < 0 else (new_dir % 4)]


def str_to_step(step: str) -> (str, int):
    return step[0], int(step[1:])


if __name__ == "__main__":
    assert solve("R2, L3") == 5
    assert solve("R2, R2, R2") == 2
    assert solve("R5, L5, R5, R3") == 12
