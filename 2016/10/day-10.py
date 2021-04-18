from typing import Tuple, List, Callable

Robot = Tuple[int, int]
State = Tuple[List[Robot], List[int]]
Instruction = Callable[[State], State]


def send(value: int, robot: Robot) -> Robot:
    low, high = robot
    if value < low or low == 0:
        low = value
    if value > high or high == 0:
        high = value
    return low, high


def parse_instruction(raw_instruction: str) -> (bool, Instruction):
    words = raw_instruction.split(" ")
    if words[0] == "value":
        return True, parse_set_instruction(raw_instruction)
    if words[0] == "bot":
        return False, parse_send_instruction(raw_instruction)
    return False, lambda x: x


def parse_set_instruction(raw_instruction: str) -> Instruction:
    words = raw_instruction.split(" ")
    value, bot_number = int(words[1]), int(words[5])

    def _send(state: State) -> State:
        robots, outputs = state
        robot = robots[bot_number]
        robot = send(value, robot)
        robots[bot_number] = robot
        return robots, outputs
    return _send


def parse_send_instruction(raw_instruction: str) -> Instruction:
    words = raw_instruction.split(" ")
    source = int(words[1])
    low_target_type, low_target_index = words[5], int(words[6])
    high_target_type, high_target_index = words[10], int(words[11])

    # local helper function, sends a value to a given target type and index in the state
    def _send_single(value: int, target_type: str, target_index: int, state: State) -> State:
        robots, outputs = state
        if target_type == "output":
            outputs[target_index] = value
        elif target_type == "bot":
            target_robot = robots[target_index]
            robots[target_index] = send(value, target_robot)
        return robots, outputs

    # returned higher-order function, updates the two targets using the source robot's low and high values
    def _send(state: State) -> State:
        robots, _ = state
        low_value, high_value = robots[source]
        state = _send_single(low_value, low_target_type, low_target_index, state)
        state = _send_single(high_value, high_target_type, high_target_index, state)
        return state
    return _send


def process(raw_instructions: [str]) -> State:
    state = ([(0, 0), (0, 0), (0, 0)], [0, 0, 0])
    instructions = []
    for raw_instructions in raw_instructions:
        assign, instruction = parse_instruction(raw_instructions)
        if assign:
            state = instruction(state)
        else:
            instructions.append(instruction)
    for instruction in instructions:
        state = instruction(state)
    return state


if __name__ == "__main__":
    test_instructions = ["value 5 goes to bot 2", "bot 2 gives low to bot 1 and high to bot 0", "value 3 goes to bot 1",
                         "bot 1 gives low to output 1 and high to bot 0",
                         "bot 0 gives low to output 2 and high to output 0",
                         "value 2 goes to bot 2"]
    _, results = process(test_instructions)
    assert results == [5, 2, 3]
