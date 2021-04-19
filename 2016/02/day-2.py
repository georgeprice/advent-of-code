import enum
from functools import reduce
import typing


class Command(enum.Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


CommandHandler = typing.Callable[[str, Command], str]


def solve(actions: list, initial: str, handler: CommandHandler) -> list:
    states = []
    for action in actions:
        for command in map(Command, action):
            initial = handler(initial, command)
        states.append(initial)
    return states


KEY_PAD = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
_keypad_lut = {
    "1": (0, 0),
    "2": (1, 0),
    "3": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 2),
    "8": (1, 2),
    "9": (2, 2),
}


def _keypad_handler(state: str, command: Command) -> str:
    x, y = _keypad_lut[state]
    if command is command.Up:
        x, y = x, max(0, y - 1)
    elif command is command.Down:
        x, y = x, min(2, y + 1)
    elif command is Command.Left:
        x, y = max(0, x - 1), y
    elif command is Command.Right:
        x, y = min(2, x + 1), y
    return KEY_PAD[y][x]


_advanced_keypad_lut = {
    "1": {
        Command.Down: "3",
    },
    "2": {
        Command.Down: "6",
        Command.Right: "3",
    },
    "3": {
        Command.Up: "1",
        Command.Down: "7",
        Command.Right: "4",
        Command.Left: "2",
    },
    "4": {
        Command.Down: "8",
        Command.Left: "3",
    },
    "5": {
        Command.Right: "6",
    },
    "6": {
        Command.Up: "2",
        Command.Down: "A",
        Command.Right: "7",
        Command.Left: "5",
    },
    "7": {
        Command.Up: "3",
        Command.Down: "B",
        Command.Right: "8",
        Command.Left: "6",
    },
    "8": {
        Command.Up: "4",
        Command.Down: "C",
        Command.Right: "9",
        Command.Left: "7",
    },
    "9": {
        Command.Left: "8",
    },
    "A": {
        Command.Up: "6",
        Command.Right: "B",
    },
    "B": {
        Command.Up: "7",
        Command.Down: "D",
        Command.Right: "C",
        Command.Left: "A",
    },
    "C": {
        Command.Up: "8",
        Command.Left: "B",
    },
    "D": {
        Command.Up: "B",
    },
}


def _advanced_keypad_handler(state: str, command: Command) -> str:
    if command in _advanced_keypad_lut[state]:
        return _advanced_keypad_lut[state][command]
    return state


if __name__ == "__main__":

    # testing no overlap
    assert list(solve(["UUUU", "UUUU", "DDDD", "DDDD"])) == [2, 2, 8, 8]
    assert list(solve(["RRRR", "RRRR", "LLLL", "LLLL"])) == [6, 6, 4, 4]

    # test case from problem spec
    assert list(solve(["ULL", "RRDDD", "LURDL", "UUUUD"])) == [1, 9, 8, 5]


