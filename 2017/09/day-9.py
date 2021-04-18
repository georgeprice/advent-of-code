def parse_score(stream: str) -> int:
    totals, group_depth, cancelled, in_garbage = 0, False, False, False
    for character in stream:

        # last character was "!" so ignore this one
        if cancelled:
            cancelled = False

        # ignore the next character
        elif character == "!":
            cancelled = True

        # start of some self-contained garbage
        elif character == "<":
            in_garbage = True

        # end of some self-contained garbage
        elif character == ">":
            in_garbage = False

        # start of a group
        elif character == "{" and not in_garbage:
            group_depth += 1

        # end of a group
        elif character == "}" and not in_garbage:
            totals += group_depth
            group_depth -= 1

    return totals


if __name__ == "__main__":
    assert parse_score("{}") == 1
    assert parse_score("{{{}}}") == 6
    assert parse_score("{{},{}}") == 5
    assert parse_score("{{{},{},{{}}}}") == 16
    assert parse_score("{<a>,<a>,<a>,<a>}") == 1
    assert parse_score("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
    assert parse_score("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
    assert parse_score("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3
