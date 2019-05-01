def solve(x: str) -> int:
    return sum(map(lambda x: int(x[0]), filter(_match, zip(_shift(x), x))))


def _match(pair_tuple: tuple) -> bool:
    return pair_tuple[0] == pair_tuple[1]


def _shift(x: str, c: int = 1) -> int: 
    return x if c == 0 else _shift(x[-1] + x[:len(x) - 1], c - 1)


if __name__ == "__main__":
    assert solve("1122") == 3
    assert solve("1111") == 4
    assert solve("1234") == 0
    assert solve("91212129") == 9