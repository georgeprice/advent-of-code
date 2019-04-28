# returns the distance of index i from 1 in the spiral
def solve(i: int) -> int:
    if i == 1:
        return 0

# returns the perimeter of the spiral at a given layer
def _perimeter(layer: int) -> int:
    return layer * 8

# returns the layer of a given index in the spiral
def _layer(i: int) -> int:
    perimeters = 1
    layer = 0

    while perimeters < i:
        layer += 1
        perimeters += _perimeter(layer)
    return layer

def _eq(y: int) -> bool:
    return lambda x: x == y 

if __name__ == "__main__":

    # calculating the perimeter of the spiral at a given layer
    assert _perimeter(0) == 0
    assert _perimeter(1) == 8
    assert _perimeter(2) == 16

    # calculating the layer of a given index in the spiral
    assert _layer(1) == 0
    assert all(map(_eq(1), map(_layer, range(2, 10))))
    assert all(map(_eq(2), map(_layer, range(10, 26))))
    assert all(map(_eq(3), map(_layer, range(26, 49))))


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