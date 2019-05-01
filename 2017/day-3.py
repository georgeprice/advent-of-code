from functools import lru_cache
import sys

sys.setrecursionlimit(10000)


@lru_cache(maxsize=5012)
def _depth(i: int) -> int:
    # i = 4*n*(n+1) solve for n

    if i == 1:
        return 0
    depth = 1
    while i > (4 * depth * (depth + 1)) + 1:
        depth += 1
    return depth


@lru_cache(maxsize=2056)
def _dist(i: int) -> int:
    """
    RULES
    - dist(1) == 0
    - if the previous i was on the previous depth, then increment
    - otherwise...
        - the upper-bound for a depth's distance is depth * 2
        - the lower-bound for a depth's distance is the depth
        - if the previous i was the upper-bound, decrement
        - if the previous i was the lower-bound, increment
        - if the previous i was the first on the depth, decrement
    """

    # base case: i is the root so it's distance is 0
    if i == 1:
        return 0

    # if this is the first index on this depth...
    if _depth(i - 1) != _depth(i):
        return _dist(i - 1) + 1

    # if the previous index was the upper bound...
    if _dist(i - 1) == _depth(i) * 2:
        return _dist(i - 1) - 1

    # if the previous index was the lower bound...
    if _dist(i - 1) == _depth(i):
        return _dist(i - 1) + 1

    # if the previous index was the first on this depth
    if _depth(i - 1) != _depth(i - 2):
        return _dist(i - 1) - 1

    # otherwise, go up if it's a pattern, else go down
    return _dist(i - 1) + 1 if _dist(i - 1) - _dist(i - 2) > 0 else _dist(i - 1) - 1


if __name__ == "__main__":

    def _eq(y: int):
        return lambda x: x == y

    # calculating the layer of a given index in the spiral
    assert _depth(1) == 0
    assert all(map(_eq(1), map(_depth, range(2, 10))))
    assert all(map(_eq(2), map(_depth, range(10, 26))))
    assert all(map(_eq(3), map(_depth, range(26, 49))))

    # calculating the manhattan distance

    assert _dist(1) == 0
    assert _dist(19) == 2
    assert _dist(12) == 3
    assert _dist(23) == 2
    assert _dist(1024) == 31
