def solve(instructions: list) -> int:
    pc = 0
    while pc < len(instructions):
        instructions[pc] += 1
        pc += instructions[pc] - 1
    return pc


if __name__ == "__main__":
    assert solve([0, 3, 0, 1, -3]) == 5
