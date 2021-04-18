import typing

Blacklist = typing.Tuple[int, int]


def solve(blacklists: typing.Iterable[Blacklist]) -> int:
    for i in range(4294967296):
        blacklists = list(filter(lambda bl: bl[1] >= i, blacklists))
        if not any(filter(lambda bl: bl[0] <= i, blacklists)):
            return i
    return 0


if __name__ == '__main__':
    _blacklists: [Blacklist] = [(5, 8), (0, 2), (4, 7)]
    lowest = solve(_blacklists)
    print("Got lowest: {}".format(lowest))
