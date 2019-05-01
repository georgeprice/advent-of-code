from functools import reduce


def solve(tree: dict) -> str:
    parent_nodes = filter(_non_empty_value(tree), tree.keys())
    descendants = reduce(_add, map(tree.get, parent_nodes))

    return next(filter( _excluded(set(descendants)), tree.keys()))


def _excluded(s: set):
    return lambda elem: elem not in s


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
