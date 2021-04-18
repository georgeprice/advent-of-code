from enum import Enum
from typing import List, MutableMapping, Tuple


class Op(Enum):
    COPY = "cpy"
    INCREMENT = "inc"
    DECREMENT = "dec"
    JUMP_ON_ZERO = "jnz"


Command = Tuple[Op, List[str]]
VirtualMachine = Tuple[int, List[Command], MutableMapping[str, int]]


def new_command(raw: str) -> Command:
    words = raw.split(" ")
    return Op(words[0]), words[1:]


def new_virtual_machine(commands: [str]) -> VirtualMachine:
    return 0, list(map(new_command, commands)), {}


def apply_command(vm: VirtualMachine, command: Command) -> VirtualMachine:
    op, params = command
    pc, commands, state = vm
    if op == Op.COPY:
        target, source = params[0], params[1]
        try:
            target = int(target)
            state[source] = target
        except ValueError:
            state[source] = state[target]
    elif op == Op.INCREMENT:
        target = params[0]
        state[target] += 1
    elif op == Op.DECREMENT:
        target = params[0]
        state[target] -= 1
    elif op == Op.JUMP_ON_ZERO:
        target, jump = params[0], int(params[1])
        if state[target] != 0:
            return pc + jump, commands, state
    return pc + 1, commands, state


def simulate(vm: VirtualMachine) -> VirtualMachine:
    pc, commands, state = vm
    while pc < len(commands):
        pc, commands, state = apply_command((pc, commands, state), commands[pc])
    return pc, commands, state


if __name__ == "__main__":
    test_commands = ["cpy 41 a", "inc a", "inc a", "dec a", "jnz a 2", "dec a"]
    test_vm = new_virtual_machine(test_commands)
    _, _, test_state = simulate(test_vm)
    print(test_state)
    pass
