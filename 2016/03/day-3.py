import typing

Triangle = typing.Tuple[int, int, int]


def solve(triangles: typing.Iterable[Triangle]) -> int:
    return len(list(filter(_is_triangle, triangles)))


def _is_triangle(triangle: Triangle) -> bool:
    """
    Returns true if a triple of triangle side lengths forms a valid triangle
        NOTE: the task said to check that a + b > c for all a, b, c lengths but that doesn't feel right...
    :param triangle: a triple of lengths of the sides of the triangle
    :return: True if this triple of lengths forms a valid triangle
    """
    a, b, c = sorted(triangle)
    return a + b > c


def _parse_row(row: str) -> [int]:
    cells = row.strip(" ").strip("\n").split(" ")
    cells = filter(len, cells)
    return map(int, cells)


if __name__ == "__main__":

    def _load_row_triangles() -> typing.Iterable[Triangle]:
        with open("input.txt") as w:
            for line in w.readlines():
                cells = _parse_row(line)
                yield next(cells), next(cells), next(cells)

    print(solve(_load_row_triangles()))

    def _load_column_triangles() -> typing.Iterable[Triangle]:
        with open("input.txt") as w:
            lines = w.readlines()
            for i in range(0, len(lines), 3):
                tidied = [cell for row in map(_parse_row, lines[i:i+3]) for cell in row]
                yield tidied[0], tidied[3], tidied[6]
                yield tidied[1], tidied[4], tidied[7]
                yield tidied[2], tidied[5], tidied[8]

    print(solve(_load_column_triangles()))

