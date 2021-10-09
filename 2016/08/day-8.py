import sys


class Screen:

    def __init__(self, width: int, length: int):

        # initialise the 2D array of cells
        self._cells = []
        for _ in range(length):
            row = []
            for _ in range(width):
                row.append(".")
            self._cells.append(row)

    # creates an AxB rectangle onto our Screen cells
    def rect(self, a: int, b: int):
        for h in range(b):
            for w in range(a):
                self._cells[h][w] = "#"

    # shifts a row right
    def rotate_row(self, row: int, amount: int):
        self._cells[row] = self._shift(self._cells[row][:], amount)

    # shifts a column down
    def rotate_column(self, col: int, amount: int):
        column = [row[col] for row in self._cells]
        shifted = self._shift(column, amount)
        for h in range(len(shifted)):
            self._cells[h][col] = shifted[h]

    def lit(self) -> int:
        count = 0
        for row in self._cells:
            for col in row:
                if col == "#":
                    count += 1
        return count

    @staticmethod
    def _shift(row: [str], amount: int) -> [str]:
        row_cells = row[:] + row[:]
        start = len(row) - amount
        end = start + len(row)
        return row_cells[start:end]

    def __str__(self):
        row_strings = []
        for h in self._cells:
            row_strings.append("".join(h))
        return "\n".join(row_strings)


# Command modifies the state of the screen
class Command:

    def __init__(self, raw: str):
        # parses the raw command string, creates an apply method to modify a Screen
        self.command, a, b = self._parse(raw)
        if self.command == "rect":
            self.apply = lambda s: s.rect(a, b)
        elif self.command == "row":
            self.apply = lambda s: s.rotate_row(a, b)
        elif self.command == "column":
            self.apply = lambda s: s.rotate_column(a, b)
        elif self.command == "exit":
            self.apply = sys.exit
        else:
            self.apply = lambda _: print("Unknown command ", self.command)

    @staticmethod
    def _parse(raw: str) -> (str, int, int):
        _command, _a, _b = "unk", 0, 0
        words = raw.split(" ")
        if len(words) == 1:
            _command = words[0]
        elif len(words) == 2:
            _command = words[0]
            _a, _b = words[1].split("x")
        else:
            _command = words[1]
            _a = words[2].split("=")[1]
            _b = words[4]
        return _command, int(_a), int(_b)


if __name__ == "__main__":
    screen = Screen(50, 6)
    with open("input.txt") as f:
        ls = f.readlines()
        commands = map(Command, ls)
        for command in commands:
            command.apply(screen)

    print(screen)
    print("lit:", screen.lit())
