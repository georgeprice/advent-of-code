import enum
import functools
import typing


class Command(enum.Enum):
    SWAP_POS = "swap position"
    SWAP_LETTER = "swap letter"
    ROTATE_LEFT = "rotate left"
    ROTATE_RIGHT = "rotate right"
    ROTATE_POS = "rotate position"
    REVERSE = "reverse"
    MOVE = "move"


Operation = typing.Tuple[Command, typing.List]
OperationHandler = typing.Callable[[typing.List, str], str]


@functools.cache
def handler(command: Command) -> OperationHandler:
    def _swap_pos(args: [int], _input: str) -> str:
        i, j = args[0], args[1]
        _input = list(_input)
        _input[i], _input[j] = _input[j], _input[i]
        return "".join(_input)

    def _swap_letter(args: [str], _input: str) -> str:
        a, b = args[0], args[1]
        _output = ""
        for (i, c) in enumerate(_input):
            if c == a:
                _output += b
            elif c == b:
                _output += a
            else:
                _output += c
        return _output

    def _rotate_left(args: [int], _input: str) -> str:
        _start = args[0]
        return (_input + _input + _input)[_start: _start + len(_input)]

    def _rotate_right(args: [int], _input: str) -> str:
        _start = len(_input) + len(_input) - args[0]
        return (_input + _input + _input)[_start: _start + len(_input)]

    def _rotate_pos(args: [int], _input: str) -> str:
        _index = _input.index(args[0])
        _rotations = _index + 1 + (1 if _index >= 4 else 0)
        return _rotate_right([_rotations], _input)

    def _reverse(args: [int], _input: str) -> str:
        i, j = args[0], args[1]
        _reversed = _input[i: j+1][::-1]
        return _input[:i] + _reversed + _input[j+1:]

    def _move(args: [int], _input: str) -> str:
        i, j = args[0], args[1]
        _i_char = _input[i]
        _input = list(_input)
        del _input[i]
        _input.insert(j, _i_char)
        return "".join(_input)

    operation_handler: typing.Dict[Command, OperationHandler] = {
        Command.SWAP_POS: _swap_pos,
        Command.SWAP_LETTER: _swap_letter,
        Command.ROTATE_LEFT: _rotate_left,
        Command.ROTATE_RIGHT: _rotate_right,
        Command.ROTATE_POS: _rotate_pos,
        Command.REVERSE: _reverse,
        Command.MOVE: _move,
    }

    return operation_handler[command]


# apply performs an operation tuple's logic onto a string, returning the modified string
def apply(op: Operation, s: str) -> str:
    _command, _args = op
    _handler = handler(_command)
    return _handler(_args, s)


if __name__ == '__main__':
    _commands: [Operation] = [
        (Command.SWAP_POS, [4, 0]),
        (Command.SWAP_LETTER, ["d", "b"]),
        (Command.REVERSE, [0, 4]),
        (Command.ROTATE_LEFT, [1]),
        (Command.MOVE, [1, 4]),
        (Command.MOVE, [3, 0]),
        (Command.ROTATE_POS, ["b"]),
        (Command.ROTATE_POS, ["d"]),
    ]
    _input = "abcde"
    for _op in _commands:
        print("> applying {} to '{}'".format(_op, _input))
        _input = apply(_op, _input)
        print("\t> got {}".format(_input))
    pass
