def solve(x: str) -> bool:
    return len(set(x.split(' '))) == len(x.split(' '))

if __name__ == "__main__":

    assert solve("aa bb cc dd ee")
    assert not solve("aa bb cc dd aa")
    assert solve("aa bb cc dd aaa")
