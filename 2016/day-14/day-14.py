import hashlib
from functools import lru_cache


def hashes(salt: str) -> [str, int]:
    i = -1
    while True:
        i += 1
        h = _hash("{}{}".format(salt, i))
        try:
            triples = triplets(h)
            triple = next(triples)
        except StopIteration:
            continue
        for j in range(1, 1001):
            j_hash = _hash("{}{}".format(salt, i+j))
            if fivers(j_hash, triple):
                yield h, i
                breaktatu


@lru_cache(maxsize=22728)
def _hash(raw: str) -> str:
    encoded = str.encode(raw)
    combined_hash = hashlib.md5(encoded).hexdigest()
    return combined_hash


def triplets(h: str) -> [str]:
    groups = [h[i:i + 3] for i in range(len(h) - 2)]
    return filter(equal, groups)


def fivers(h: str, k: str) -> bool:
    return k[0] * 5 in h


def equal(group: [str]) -> bool:
    return set(group) == {group[0]}


if __name__ == "__main__":
    hs = hashes("abc")
    for i in range(64):
        h, j = next(hs)
        print(i, j, h)
