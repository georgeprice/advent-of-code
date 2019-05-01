def solve(instructions: list) -> int:
    registers = {}
    for target, command, value, source, op, val in map(_parse, instructions):
        if target not in registers:
            registers[target] = 0
        condition = "{}{}{}".format(int(registers[source] if source in registers else 0), op, val)
        if eval(condition):
            registers[target] += int(value) * (1 if command == "inc" else -1)

    return registers[sorted(registers.keys(), key=registers.get).pop()]


def _parse(instruction: str) -> tuple:
    target, command, value, _, source, op, val = instruction.split(' ')
    return target, command, value, source, op, val


if __name__ == "__main__":
    assert solve([
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10"
    ]) == 1
