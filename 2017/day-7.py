from functools import reduce


def solve(tree: dict) -> str:
    roots = filter(_non_empty_value(tree), tree.keys())
    descendants = reduce(_add, map(tree.get, roots))

    return (set(tree.keys()) - set(descendants)).pop()


def _add(a: list, b: list) -> list:
    return a + b


def _non_empty_value(dct: dict):
    return lambda key: any(dct[key])


if __name__ == "__main__":
    sample_tree = {
        "pbga": [],
        "xhth": [],
        "ebii": [],
        "havc": [],
        "ktlj": [],
        "fwft": ["ktlj", "cntj", "xhth"],
        "goyg": [],
        "padx": ["pbga", "havc", "goyg"],
        "tknk": ["ugml", "padx", "fwft"],
        "jptl": [],
        "ugml": ["gyxo", "ebii", "jptl"],
        "gyxo": [],
        "cntj": []
    }

    assert solve(sample_tree) == "tknk"
