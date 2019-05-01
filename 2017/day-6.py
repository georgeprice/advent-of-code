import math

def solve(banks: tuple) -> int:

    cache = set()
    count = len(banks)

    while banks not in cache:

        cache.add(banks)

        n_i, n_v = _next_index(banks)
        indiv_handout = math.floor(n_v / (count - 1))
        total_handout = indiv_handout * (count - 1)

        banks = tuple([
            banks[i] - total_handout if i == n_i else banks[i] + indiv_handout
            for i in range(count)
        ])

    return len(cache)

def _next_index(lst: list) -> int:
    return next(filter(_is_max_pair(lst), enumerate(lst)))


def _is_max_pair(lst: list):
    return lambda pair: pair[1] == max(lst)

if __name__ == "__main__":

    assert solve((0, 2, 7, 0)) == 5
