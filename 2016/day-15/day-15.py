from typing import Tuple

# Disc = [Disc #, # Positions, Start Position]
Disc = Tuple[int, int, int]


def passes(disc: Disc, drop_time: int) -> bool:
    number, positions, start = disc
    time = number + drop_time
    return ((start + time) % positions) == 0


def solve(discs: [Disc]) -> int:
    t = 0
    while True:
        ok = all(map(lambda d: passes(d, t), discs))
        if ok:
            return t
        t += 1


if __name__ == "__main__":
    first, second = (1, 5, 4), (2, 2, 1)
    assert passes(first, 0)
    assert not passes(second, 0)

    assert passes(first, 5)
    assert passes(second, 5)

    assert solve([first, second]) == 5
