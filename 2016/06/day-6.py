# returns the hidden message from a list of index counts
def get_message(index_counts: [{str: int}]) -> str:
    message = ""
    for index_count in index_counts:
        most_popular = sorted(index_count.keys(), key=lambda k: -index_count[k])
        message += "{}".format(most_popular[0])
    return message


# takes a list of strings, returns a counts map for each index of the strings
def process_rows(rows: [str], length: int) -> [{str: int}]:
    index_mappings = []
    for i in range(length):
        column = map(lambda row: row[i], rows)
        index_mapping = process_column(list(column))
        index_mappings += [index_mapping]
    return index_mappings


# returns a mapping of characters to their number of occurrences in a string
def process_column(row: [str]) -> {str: int}:
    index_mapping = {}
    for character in set(row):
        index_mapping[character] = row.count(character)
    return index_mapping


if __name__ == "__main__":
    test_sequences = ["eedadn", "drvtee", "eandsr", "raavrd", "atevrs", "tsrnev", "sdttsa", "rasrtv", "nssdts",
                      "ntnada", "svetve", "tesnvt", "vntsnd", "vrdear","dvrsen", "enarar"]
    counts = process_rows(test_sequences, 6)
    m = get_message(counts)
    assert m == "easter"
