import typing

Elf = typing.Tuple[int, int]


# simulate runs a single turn of the game, returning the remaining elves and whether changes had been made (bool)
def simulate(elves: [Elf]) -> Elf:

    current_index = 0
    while len(elves) > 1:

        # get the details for the current elf
        elf_id, elf_presents = elves[current_index]

        # get the details for the next elf to our left
        neighbour_index = (current_index + 1) % len(elves)
        neighbour_id, neighbour_presents = elves[neighbour_index]

        print("\telf {} takes {} presents from elf {}".format(elf_id, neighbour_presents, neighbour_id))

        # update the current elf, get rid of the neighbour
        elves[current_index] = (elf_id, elf_presents + neighbour_presents)
        del elves[neighbour_index]

        # we'll run the next elf
        current_index = (neighbour_index % len(elves))

    return elves[0]


if __name__ == '__main__':
    n = 10
    _elves = list((i, 1) for i in range(1, n + 1))
    (_elf_id, _elf_presents) = simulate(_elves)
    print("Elf {} gets {} presents".format(_elf_id, _elf_presents))
