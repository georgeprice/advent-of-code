# parses the raw string - only true if no hypernet sequences are ABBA, but at least one non-hypernet sequences is
def solve(raw: str) -> bool:
    hn, nhn = parse(raw)
    return not any(map(is_abba, hn)) and any(map(is_abba, nhn))


# parses a raw "IPv7" IP into two lists - hypernet sequences and non-hypernet sequences
def parse(raw: str) -> ([str], [str]):
    hypernet_sequences, non_hypernet_sequences = [], []
    is_hypernet_sequence = False
    start_index = 0
    while start_index < len(raw) - 3:
        start_character = raw[start_index]

        # checking for special start characters - not included in the sequence but control sequence type
        if start_character == "]":
            is_hypernet_sequence = False
            start_index += 1
            continue
        if start_character == "[":
            is_hypernet_sequence = True
            start_index += 1
            continue

        # keep extending the sequence until we hit another special character ("[" or "]")
        next_index = 0
        for next_index, next_character in enumerate(raw[start_index:]):
            sequence = raw[start_index:start_index + next_index]
            if next_character == "]" or next_character == "[":
                break
        else:
            sequence = raw[start_index:]

        start_index += next_index

        # put sequence into associated list
        if is_hypernet_sequence:
            hypernet_sequences += [sequence]
        else:
            non_hypernet_sequences += [sequence]
    return hypernet_sequences, non_hypernet_sequences


def is_abba(raw: str) -> bool:
    # base case - check the 4 character string is a palindrome
    if len(raw) == 4:
        if len(set(raw)) != 2:
            return False
        return raw[0] == raw[3] and raw[1] == raw[2]

    # recursive case - try all 4 character substrings
    children = []
    for i in range(len(raw)-3):
        children += [raw[i:i+4]]
    return any(map(is_abba, children))


if __name__ == "__main__":
    assert solve("abba[mnop]qrst")
    assert not solve("abcd[bddb]xyyx")
    assert not solve("aaaa[qwer]tyui")
    assert solve("ioxxoj[asdfgh]zxcvbn")
