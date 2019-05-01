import math

def solve(banks: tuple) -> int:

    cache = set()

    while banks not in cache:
        cache.add(banks)
        n_v = _next_index(banks)
        n_i = banks.index(n_v)
        handout = math.floor(n_v / (len(banks) - 1))
        
        banks = tuple([banks[i] - handout * (len(banks) - 1) if i == n_i else banks[i] + handout for i in range(banks)])

    return len(cache)

def _next_index(lst: list) -> int:
    return next(filter(_is_max(lst), lst))

def _is_max(lst: list):
    return lambda elem: elem == max(lst)

if __name__ == "__main__":

    assert solve((0, 2, 7, 0)) == 5
