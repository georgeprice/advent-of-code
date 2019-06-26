from functools import reduce

KEY_PAD = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def solve(commands: list) -> list:

    # starting on the '5' key
    state = (1, 1)

    for command in commands:
        state = reduce(_update_state, command, state)
        yield _to_keys(state)


def _to_keys(coordinates: (int, int)) -> int:
    """
    Converts (x, y) coordinates to the equivalent integer keys on a keypad
    :param coordinates: an (x, y) coordinate tuple
    :return: the integer key found on the keypad at that position
    """
    x, y = coordinates
    return KEY_PAD[y][x]


def _update_state(start: (int, int), command: str) -> (int, int):
    """
    Returns a new (x, y) state given a start state and command (U/D/L/R)
    :param start: the original x, y state
    :param command: a movement command to be performed
    :return: a new (x, y) state after performing
    """
    x, y = start
    if command == 'U':
        return x, max(0, y - 1)
    if command == 'D':
        return x, min(2, y + 1)
    if command == 'L':
        return max(0, x - 1), y
    if command == 'R':
        return min(2, x + 1), y


if __name__ == "__main__":

    # testing no overlap
    assert list(solve(["UUUU", "UUUU", "DDDD", "DDDD"])) == [2, 2, 8, 8]
    assert list(solve(["RRRR", "RRRR", "LLLL", "LLLL"])) == [6, 6, 4, 4]

    # test case from problem spec
    assert list(solve(["ULL", "RRDDD", "LURDL", "UUUUD"])) == [1, 9, 8, 5]


