def dragon_curve(code: str) -> str:
    suffix = code[::-1].replace("0", "a").replace("1", "0").replace("a", "1")
    return code + "0" + suffix


def dragon_curve_until(code: str, i: int) -> str:
    while len(code) < i:
        code = dragon_curve(code)
    return code[:i]


def pairs(code: str) -> [(str, str)]:
    ps = [(code[i], code[i+1]) for i in range(0, len(code) - 1, 2)]
    return ps


def check_sum_pair(p: (str, str)) -> str:
    a, b = p
    if a == b:
        return "1"
    return "0"


def check_sum(code: str) -> str:
    res = "".join(map(check_sum_pair, pairs(code)))
    if len(res) % 2 == 0:
        return check_sum(res)
    return res


def solve(seed: str, disk_length: int) -> str:
    padded = dragon_curve_until(seed, disk_length)
    return check_sum(padded)


if __name__ == "__main__":

    assert dragon_curve("1") == "100"
    assert dragon_curve("0") == "001"
    assert dragon_curve("11111") == "11111000000"
    assert dragon_curve("111100001010") == "1111000010100101011110000"

    test_pairs = pairs("110010110100")
    assert test_pairs == [("1", "1"), ("0", "0"), ("1", "0"), ("1", "1"), ("0", "1"), ("0", "0")]
    assert check_sum("110010110100") == "100"

    assert solve("10000", 20) == "01100"

    puzzle_input = "100110111000111001010101"
    puzzle_output = solve(puzzle_input, 272)
    print(puzzle_input, puzzle_output)
