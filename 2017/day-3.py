# returns the distance of index i from 1 in the spiral
def solve(i: int) -> int:
    if i == 1:
        return 0

# returns the perimeter of the spiral at a given depth
def _perimeter(depth: int) -> int:
    return depth * 8

# returns the depth of a given index in the spiral
def _depth(i: int, depth=0, counter=1) -> int:
    return depth if counter >= i else _depth(i, depth + 1, counter + _perimeter(depth + 1))

if __name__ == "__main__":

    # calculating the perimeter of the spiral at a given layer
    assert _perimeter(0) == 0
    assert _perimeter(1) == 8
    assert _perimeter(2) == 16

    def _eq(y: int) -> bool:
        return lambda x: x == y

    # calculating the layer of a given index in the spiral
    assert _depth(1) == 0
    assert all(map(_eq(1), map(_depth, range(2, 10))))
    assert all(map(_eq(2), map(_depth, range(10, 26))))
    assert all(map(_eq(3), map(_depth, range(26, 49))))


"""
37  36  35  34  33  32 31
38  17  16  15  14  13 30
39  18   5   4   3  12 29
40  19   6   1   2  11 28
41  20   7   8   9  10 27
42  21  22  23  24  25 26
43  44  45  46  47  48 49

layer(j) = 
perimeter(i) = i * 8
"""