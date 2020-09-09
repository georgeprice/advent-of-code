from enum import Enum
import typing


class Tile(Enum):
    SAFE = "."
    TRAP = "^"


Row = typing.List[Tile]


def get_listeners(x: int, above: Row) -> [Tile]:
    left, center, right = x - 1, x, x + 1
    if left < 0:
        yield Tile.SAFE
    else:
        yield above[left]
    yield above[center]
    if right >= len(above):
        yield Tile.SAFE
    else:
        yield above[right]


def generate_tile(x: int, above: Row) -> Tile:
    left, center, right = get_listeners(x, above)
    if (left, center, right) == (Tile.TRAP, Tile.TRAP, Tile.SAFE):
        return Tile.TRAP
    if (left, center, right) == (Tile.SAFE, Tile.TRAP, Tile.TRAP):
        return Tile.TRAP
    if (left, center, right) == (Tile.TRAP, Tile.SAFE, Tile.SAFE):
        return Tile.TRAP
    if (left, center, right) == (Tile.SAFE, Tile.SAFE, Tile.TRAP):
        return Tile.TRAP
    return Tile.SAFE


def generate_row(above: Row) -> Row:
    return [generate_tile(x, above) for x in range(len(above))]


def generate_maze(start: Row, height: int) -> [Row]:
    rows = [start]
    for i in range(height - 1):
        new_row = generate_row(rows[i])
        rows.append(new_row)
    return rows


def parse_row_string(raw: str) -> Row:
    return [Tile(r) for r in raw]


def count_safe(rows: [Row]) -> int:
    counts = map(lambda row: row.count(Tile.SAFE), rows)
    return sum(counts)


if __name__ == "__main__":
    test_in = parse_row_string("..^^.")
    assert count_safe(generate_maze(test_in, 3)) == 6

    test_in = parse_row_string(".^^.^.^^^^")
    assert count_safe(generate_maze(test_in, 10)) == 38
