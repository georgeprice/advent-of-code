from enum import Enum
from typing import AnyStr, Callable, List, MutableMapping, Tuple, Iterable


class Op(Enum):
    COPY = "cpy"
    INCREMENT = "inc"
    DECREMENT = "dec"
    JUMP_ON_NON_ZERO = "jnz"
    JUMP = "jmp"
    JUMP_ON_NON_ZERO_ABSOLUTE = "*jnz"
    ADD = "add"
    NOOP = "noop"


Command = Tuple[Op, List[str]]
VirtualMachine = Tuple[int, List[Command], MutableMapping[str, int]]
Optimiser = Callable[[List[Command]], List[Command]]


def new_command(raw: str) -> Command:
    words = raw.split(" ")
    return Op(words[0]), words[1:]


def optimise_adds(_commands: [Command]) -> [Command]:

    # first pass is to detect jump spots
    jump_spots = {}
    for _i, _command in enumerate(_commands):
        op, params = _command
        if op == Op.JUMP_ON_NON_ZERO:
            print("optimise_adds: alert: cannot perform this optimisation if jnz commands exist")
            return _commands
        if op == Op.JUMP_ON_NON_ZERO_ABSOLUTE:
            [_, location] = params
            jump_spots[location] = 1 if location not in jump_spots else jump_spots[location] + 1
    print("optimise_adds: got jump spots: {}".format(jump_spots))

    _i = 0
    while _i in range(len(_commands)):
        if _i + 2 < len(_commands):

            # we can't do this if the loops caused by jumping intertwine
            if _i + 1 in jump_spots or _i + 2 in jump_spots:
                yield _commands[_i]
                _i += 1
                continue

            first_command, second_command, third_command = _commands[_i], _commands[_i + 1], _commands[_i + 2]

            print("optimise_adds: testing commands [{}:{}]:[{}]".format(_i, _i + 2, _commands[_i:_i + 3]))

            first_op, first_params = first_command
            second_op, second_params = second_command
            third_op, third_params = third_command

            # first two operations need to be increment and decrements, and third operation needs to be a jump on zero
            if {first_op, second_op} != {Op.INCREMENT, Op.DECREMENT} or third_op != Op.JUMP_ON_NON_ZERO_ABSOLUTE:
                yield _commands[_i]
                _i += 1
                continue

            # the jump needs to go back to the first param
            [jump_condition, jump_target] = third_params
            if jump_target != _i:
                yield _commands[_i]
                _i += 1
                continue

            # the jump condition needs to be on the same register we're decrementing
            dec_target = first_params[0] if first_op is Op.DECREMENT else second_params[0]
            if jump_condition != dec_target:
                yield _commands[_i]
                _i += 1
                continue

            inc_target = first_params[0] if first_op is Op.INCREMENT else second_params[0]

            # increment and decrement commands need to be complimentary
            swap_targets = {inc_target, dec_target}
            if len(swap_targets) != 2:
                yield _commands[_i]
                _i += 1
                continue

            print("optimise_adds: found valid commands [{}:{}]:[{}]".format(_i, _i + 2, _commands[_i:_i + 3]))

            yield Op.ADD, [dec_target, inc_target]
            yield Op.NOOP, []
            yield Op.NOOP, []
            _i += 3
            continue
        yield _commands[_i]
        _i += 1


def create_absolute_jumps(_commands: [Command]) -> [Command]:
    for _i, _command in enumerate(_commands):
        op, params = _command
        if op == Op.JUMP_ON_NON_ZERO:
            value, relative = params
            try:
                int(value)
                yield Op.JUMP, [_i + int(relative)]
            except:
                yield Op.JUMP_ON_NON_ZERO_ABSOLUTE, [value, _i + int(relative)]
        else:
            yield _command


def optimisations(_commands: List[Command], optimisers: [Optimiser]) -> List[Command]:
    for optimiser in optimisers:
        _commands = list(optimiser(_commands))
        print("optimisations: ({}) {}".format(len(_commands), _commands))
    return list(_commands)


def new_virtual_machine(_commands: [str]) -> VirtualMachine:
    _commands = list(map(new_command, _commands))
    return 0, optimisations(_commands, [create_absolute_jumps, optimise_adds]), {}


def apply_command(vm: VirtualMachine, _command: Command) -> VirtualMachine:
    op, params = _command
    pc, _commands, state = vm
    if op == Op.COPY:
        target, source = params[0], params[1]
        try:
            target = int(target)
            state[source] = target
        except ValueError:
            state[source] = state[target]
        return pc + 1, _commands, state
    elif op == Op.INCREMENT:
        target = params[0]
        state[target] += 1
        return pc + 1, _commands, state
    elif op == Op.DECREMENT:
        target = params[0]
        state[target] -= 1
        return pc + 1, _commands, state
    elif op == Op.JUMP_ON_NON_ZERO:
        target, jump = params[0], int(params[1])
        if target in state and state[target] != 0:
            return pc + jump, _commands, state
    elif op == Op.JUMP_ON_NON_ZERO_ABSOLUTE:
        target, jump = params[0], int(params[1])
        if target in state and state[target] != 0:
            return jump, _commands, state
    elif op == Op.JUMP:
        jump = int(params[0])
        return jump, _commands, state
    elif op == Op.ADD:
        source, target = params[0], params[1]
        state[target] += state[source]
        state[source] = 0
        return pc + 1, _commands, state
    elif op == Op.NOOP:
        return pc + 1, _commands, state
    else:
        raise Exception("unk command: {}".format(_command))
    return pc + 1, _commands, state


def simulate(vm: VirtualMachine) -> VirtualMachine:
    pc, _commands, state = vm
    while pc < len(_commands):
        # print(state)
        pc, _commands, state = apply_command((pc, _commands, state), _commands[pc])
    return pc, _commands, state


if __name__ == "__main__":
    test_commands = ["cpy 41 a", "inc a", "inc a", "dec a", "jnz a 2", "dec a"]
    test_vm = new_virtual_machine(test_commands)
    _, _, test_state = simulate(test_vm)
    assert test_state["a"] == 42

    # commands = open("input").read().split("\n")
    # _vm = new_virtual_machine(commands)
    # _, commands, _ = _vm
    # for i, command in enumerate(commands):
    #     print(i, command[0].value, " ".join(map(str, command[1])))
    # _, _, _state = simulate(_vm)
    # print(_state)
