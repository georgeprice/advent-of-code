def decode(raw: str) -> str:

    # base case
    if raw.count("(") == 0:
        return raw

    # work out the marker substring
    first, last = raw.index("("), raw.index(")")

    # first substring that isn't affected by the marker
    prefix = raw[:first]

    # get the marker, calculate what it affects
    marker = raw[first:last+1]
    marker_count, marker_reps = decode_marker(marker)
    marker_range = raw[last+1:last+1+marker_count]

    # apply the marker to the middle section
    middle = apply_marker(marker_reps, marker_range)

    # substring after the marker
    suffix = raw[last+1+marker_count:]

    # recursive case
    return prefix + middle + decode(suffix)


def apply_marker(reps: int, raw: str) -> str:
    return raw * reps


def decode_marker(raw: str) -> (int, int):
    raw = raw.replace(")", "")
    raw = raw.replace("(", "")
    count, reps = raw.split("x")
    return int(count), int(reps)


if __name__ == "__main__":
    assert decode("A(1x5)BC") == "ABBBBBC"
    assert decode("(3x3)XYZ") == "XYZXYZXYZ"
    assert decode("A(2x2)BCD(2x2)EFG") == "ABCBCDEFEFG"
    assert decode("(6x1)(1x3)A") == "(1x3)A"
    assert decode("X(8x2)(3x3)ABCY") == "X(3x3)ABC(3x3)ABCY"
