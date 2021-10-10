from enum import Enum
import typing
from itertools import chain, combinations

"""
    Custom data structures...
"""


class Electrical(Enum):
    MICROCHIP = "M"
    GENERATOR = "G"


Movable = typing.Tuple[typing.AnyStr, Electrical]
State = typing.Tuple[int, typing.List[typing.List[Movable]]]

""" 
    Generating strings for different data structures
    Used for pretty formatting and hashing to detect dupes
"""


def movable_string(movable: Movable) -> str:
    element, electrical = movable
    return str(element) + str(electrical.value)


def floor_string(floor: [Movable]) -> str:
    strings = sorted(map(movable_string, floor))
    return "[{}]".format(",".join(strings))


def floors_string(floors: [[Movable]]) -> str:
    return "".join(map(floor_string, floors))


def state_string(state: State) -> str:
    elevator, floors = state
    return str(elevator)+"~"+floors_string(floors)


"""
    Functions for state tuples
"""


# clone performs a deep-clone of the nested lists in a state
def clone(state: State) -> State:
    cloned_floors = []
    elevator, floors = state
    for floor in floors:
        cloned_floors.append(floor[:])
    return elevator, cloned_floors


# complete returns if the elevator is on the top floor with all the movable objects
def complete(state: State) -> bool:
    elevator, floors = state
    for i in range(0, len(floors) - 1):
        if len(floors[i]) > 0:
            return False
    c = elevator == len(floors) - 1
    return c


# valid returns if a state can be moved to without losing
def valid(state: State) -> bool:
    _, floors = state
    return all(map(valid_floor, floors))


# valid_floor returns whether a floor is valid (each microchip has a generator if a conflicting generator exists)
def valid_floor(floor: [Movable]) -> bool:

    elements, unbound_microchips, generators = set(), {}, {}
    for element, electrical in floor:
        elements.update(element)
        if element not in unbound_microchips:
            unbound_microchips[element] = 0
        if electrical == Electrical.MICROCHIP:
            unbound_microchips[element] += 1
        elif electrical == Electrical.GENERATOR:
            unbound_microchips[element] -= 1
            generators[element] = True

    # if there's just one element then who cares
    if len(unbound_microchips.keys()) < 2:
        return True

    # if there are no generators then no frying can be done
    if len(generators) == 0:
        return True

    # microchips w/out a generator will be fried if a conflicting generator exists
    if unbound_microchips[Element.LITHIUM] > 0 and generators[Element.HYDROGEN] > 0:
        return False
    if unbound_microchips[Element.HYDROGEN] > 0 and generators[Element.LITHIUM] > 0:
        return False
    return True


"""
    Creating solutions for a given state
"""


def _moves(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, 3))


# moves returns a list of all states that can be reached by one move from the current state
def moves(current: State) -> [State]:
    elevator_floor, floors = current
    below, above = max(0, elevator_floor-1), min(elevator_floor+1, len(floors) - 1)
    for new_elevator in [below, above]:
        if new_elevator == elevator_floor:
            continue

        # generate all combinations of objects to move from this floor to the next
        for move in _moves(floors[elevator_floor]):

            # move objects from one floor to the next
            _, new_floors = clone(current)
            current_floor = new_floors[elevator_floor]
            new_floor = new_floors[new_elevator]
            for movable in move:
                current_floor.remove(movable)
                new_floor.append(movable)

            # check that the modified floors are valid
            valid_new_floor = valid_floor(new_floor)
            valid_current_floor = valid_floor(current_floor)
            if valid_new_floor and valid_current_floor:
                yield new_elevator, new_floors


def solve(floors: [[Movable]]) -> int:
    state = (0, floors[:])
    return _solve(state)


def _solve(state: State) -> int:
    children = [state]
    i = 0
    visited = {}
    while len(children) > 0:

        # check if any child states have solved it
        completed = any(map(lambda c: complete(c), children))
        if completed:
            return i

        # get the next moves you can reach from this state
        new_children = []
        for child in children:
            for new_child in moves(child):
                h = state_string(new_child)
                if h in visited:
                    continue
                visited[h] = True
                new_children.append(new_child)

        children = new_children
        i += 1
    return -1


if __name__ == "__main__":
    first_floor = [(Element.HYDROGEN, Electrical.MICROCHIP), (Element.LITHIUM, Electrical.MICROCHIP)]
    second_floor = [(Element.HYDROGEN, Electrical.GENERATOR)]
    third_floor = [(Element.LITHIUM, Electrical.GENERATOR)]
    fourth_floor = []
    test_floors = [first_floor, second_floor, third_floor, fourth_floor]
    moves = solve(test_floors)
    assert moves == 11
