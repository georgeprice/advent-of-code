def solve(x: list) -> int:
    if len(x) == 0:
        return 0
    return max(x[0]) - min(x[0]) + solve(x[1:])

if __name__ == "__main__":
    assert solve([[5, 1, 9, 8], [7, 5, 3], [2, 4, 6, 8]]) == 18
