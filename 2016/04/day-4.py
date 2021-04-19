import string


def solve(encrypted_name: str, sector_id: int, check_sum: str) -> bool:
    # get the number of occurrences for each letter in the encrypted name
    letter_counts = parse(encrypted_name.replace("-", ""))

    # group the letter counts by their number of occurrences
    grouped = group_by_count(letter_counts)

    # sort the letters into descending order based on their number of occurrences
    descending_order = sorted(grouped.items(), key=lambda kv: -kv[0])

    # append the characters after sorting each grouping alphabetically
    sorted_alphabetically = []
    for pair in descending_order:
        _, chars = pair
        sorted_alphabetically += sorted(chars)

    # join them together to get the full checksum
    got_check_sum = "".join(sorted_alphabetically)

    # check the given checksum matches the start of what we got
    return got_check_sum[:len(check_sum)] == check_sum


# inverts a mapping of strings to their occurrences to a map of occurrences to a list of strings
def group_by_count(letter_map: {str: int}) -> {int: [str]}:
    grouped = {}
    for pair in letter_map.items():
        letter, occurrences = pair
        exists = occurrences in grouped
        if not exists:
            grouped[occurrences] = []
        grouped[occurrences] += [letter]
    return grouped


def parse(name: str) -> {str: int}:
    characters = set(name)
    counts = {}
    for character in characters:
        counts[character] = name.count(character)
    return counts


def parse_file() -> [(str, int, str)]:
    with open("input") as w:
        for l in w.readlines():
            # tidy the line data and split by -
            cells = l.replace("\n", "").split("-")

            # parse the sector id and checksum data
            last_cells = cells[-1].rstrip("]").split("[")
            sector_id, checksum = int(last_cells[0]), last_cells[1]

            # reformat the encrypted name
            encrypted_name = "-".join(cells[:-1])
            yield encrypted_name, sector_id, checksum


def perform_shift_cipher(encrypted: str, shift: int) -> str:
    shift_cipher = string.ascii_lowercase
    out = ""
    for char in encrypted:
        if char in shift_cipher:
            shifted_index = (shift_cipher.index(char) + shift) % len(shift_cipher)
            out += shift_cipher[shifted_index]
        elif char == "-":
            out += " "
    return out


if __name__ == "__main__":
    assert solve("aaaaa-bbb-z-y-x", 123, "abxyz")
    assert solve("a-b-c-d-e-f-g-h", 987, "abcde")
    assert solve("not-a-real-room", 404, "oarel")
    assert not solve("totally-real-room", 200, "decoy")
