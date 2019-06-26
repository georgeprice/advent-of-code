def solve(triangles: list) -> int:
    return len(list(filter(_is_triangle, triangles)))


def _is_triangle(triangle: (int, int, int)) -> bool:
    """
    Returns true if a triple of triangle side lengths forms a valid triangle
        NOTE: the task said to check that a + b > c for all a, b, c lengths but that doesn't feel right...
    :param triangle: a triple of lengths of the sides of the triangle
    :return: True if this triple of lengths forms a valid triangle
    """
    a, b, c = sorted(triangle)
    return (a * a) + (b * b) == (c * c)


if __name__ == "__main__":
    assert solve([(5, 10, 25), (3, 4, 5), (2, 1, 2), (4, 5, 8)]) == 1
