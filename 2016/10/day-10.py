from functools import reduce
from typing import Tuple, Union, List


# SendInstruction describes an instruction to send a low and high value from one robot to two others
SendInstruction = Tuple[int, bool, bool, int]

# SetInstruction describes an instruction to send a value to a robot
SetInstruction = Tuple[int, int]

# Robot describes a {low, high} value pairing
Robot = Tuple[int, int]

# State describes the current setup of robots and outputs in the system
State = Tuple[List[Robot], List[int]]


def _new_state(_robots: List[Robot], _outputs: List[int]) -> State:
    return _robots, _outputs


def _active(_robot: Robot) -> bool:
    _low, _high = _robot
    return _low > 0 and _high > 0


# _set will attempt to send a value to a robot
def _set(_value: int, _current: Robot) -> Robot:
    _low, _high = _current

    # no values have been set, so just set the highest value
    if _low == -1 and _high == -1:
        _new = _low, _value
        print("_send(_value: {}, _current: {}): created (none set already): {}".format(_value, _current, _new))

    # just the highest value has been set
    elif _low == -1:
        _new = min(_value, _high), max(_value, _high)
        print("_send(_value: {}, _current: {}): created (highest set already): {}".format(_value, _current, _new))

    # both values have been set so chose lowest and highest of the three
    else:
        _values = {_low, _value, _high}
        print(_values)
        _new = (min(_values), max(_values))
        print("_send(_value: {}, _current: {}): created (both set): {}".format(_value, _current, _new))

    return _new


# _handle_instruction modifies the state of the system using an instruction
def _handle_instruction(_state: State, _instruction: Union[SetInstruction, List[SendInstruction]]) -> State:

    print("_handle_instruction: processing instruction {}".format(_instruction))

    # setting a robot's value directly
    if _instruction is SetInstruction:
        return _handle_set_instruction(_state=_state, _instruction=_instruction)
    return _handle_send_instructions(_state=_state, _instructions=_instruction)


def _handle_set_instruction(_state: State, _instruction: SetInstruction) -> State:

    # unpack the state tuple
    _robots, _outputs = _state

    # sending a value to a robot
    _value, _target = _instruction
    _target_robot = _robots[_target]
    _robots[_target] = _set(_value, _target_robot)
    print("_handle_set_instruction: value: {}, target (index: {}): {}"
          ", _new_robot: {}".format(_value, _target, _target_robot, _robots[_target]))
    return _robots, _outputs


def _handle_send_instructions(_state: State, _instructions: List[SendInstruction]) -> State:
    _robots, _outputs = _state
    for _instruction in _instructions:
        # unpack the instruction
        _from, _is_low, _send_to_robot, _target = _instruction

        # find the robot that the value is being sent from
        _from_low, _from_high = _robots[_from]

        # decide which value we want to send to the target
        _send_value = _from_low if _is_low else _from_high

        # sanity check that we're not trying to send a value that hasn't been populated yet...
        if _send_value == -1:
            _message = "_handle_send_instructions: cannot send value {} (low? {}) from robot #{} ({})".format(
                _send_value, _is_low, _from, _robots[_from])
            raise Exception(_message)

        # update the state of the robot as it just sent a value
        _from_robot = (-1, _from_high) if _is_low else (_from_low, -1)

        # update the robot we've sent the value from
        _robots[_from] = _from_robot

        # send the value to another robot
        if _send_to_robot:
            _target_robot = _robots[_target]
            _target_robot = _set(_value=_send_value, _current=_target_robot)
            _message = "_handle_send_instructions: send: handling instruction: {}, sent value {} (low? {}) from robot #{} " \
                       "({}) to robot #{} ({}), updated sender to {}, receiver to {}" \
                .format(_instruction, _send_value, _is_low, _from, _robots[_from], _target, _robots[_target],
                        _from_robot, _target_robot)
            print(_message)
            _robots[_target] = _target_robot
        else:
            _outputs[_target] = _send_value
            _message = "_handle_send_instructions: send: handling instruction: {}, sent value {} (low? {}) from robot #{} " \
                       "({}) to output #{}, updated sender to {}, output to {}" \
                .format(_instruction, _send_value, _is_low, _from, _robots[_from], _target,
                        _from_robot, _outputs[_target])
            print(_message)

    return _robots, _outputs


def parse_instruction(raw: str) -> [Union[SetInstruction, SendInstruction]]:
    _words = raw.split(" ")
    if _words[0] == "bot":
        _from = int(_words[1])
        _to_low_name, _to_low_target = _words[5], int(_words[6])
        _to_low_instruction = (_from, True, _to_low_name == "bot", _to_low_target)
        _to_high_name, _to_high_target = _words[10], int(_words[11])
        _to_high_instruction = (_from, False, _to_high_name == "bot", _to_high_target)
        _instructions = [_to_low_instruction, _to_high_instruction]
        print("parse_instruction(raw: {}): created send instructions: {}".format(raw, _instructions))
        return _instructions
    elif _words[0] == "value":
        _value, _target = int(_words[1]), int(_words[len(_words) - 1])
        _set_instruction = (_value, _target)
        print("parse_instruction(raw: {}): created set instruction: {}".format(raw, _set_instruction))
        return [_set_instruction]
    else:
        message = "could not parse instruction type from instruction {}".format(_words[0])
        raise Exception(message)
    pass


def simulate(_instructions: List[Union[SetInstruction, List[SendInstruction]]]) -> State:

    print("simulate(_instructions: {})".format(len(_instructions)))

    # create a flattened array of all set and send instructions
    _sets, _sends = [], []

    # keep track of how many robots and outputs we need to create by snooping the instructions
    _robot_count, _output_count = 0, 0
    for _instruction in _instructions:
        print("simulate(_instructions: {}): got instruction: {}".format(len(_instructions), _instruction))

        if _instruction is SetInstruction or len(_instruction) == 2:
            print("simulate(_instructions: {}): got set instruction: {}".format(len(_instructions), _instruction))
            _, _target_robot = _instruction
            _robot_count = max(_robot_count, _target_robot + 1)

            # add this set instruction to our list of all set instructions to process
            _sets.append(_instruction)
        if _instruction is SendInstruction or len(_instruction) == 4:
            print("simulate(_instructions: {}): got send instruction: {}".format(len(_instructions), _instruction))

            _from, _is_low, _send_to_robot, _target = _instruction
            if _send_to_robot:
                _robot_count = max(_robot_count, _target + 1, _from + 1)
            else:
                _output_count = max(_robot_count, _target + 1)

            # add these send instructions to our list of all send instructions to process
            _sends.append(_instruction)

    print("simulate: got {} set instructions, got {} send instructions".format(len(_sets), len(_sends)))
    print("simulate: we need {} robots, and {} outputs".format(_robot_count, _output_count))

    _robots = [(-1, -1) for _ in range(_robot_count)]
    _outputs = [0 for _ in range(_output_count)]
    _state = (_robots, _outputs)

    print("simulate: created state: {}".format(_state))

    print("simulate: setting up send listeners for all robots")
    _listeners = [list() for _ in range(_robot_count)]
    for _send_instruction in _sends:
        source, _, _, _ = _send_instruction
        _listeners[source].append(_send_instruction)
    print("simulate: setup send listeners for all robots: {}".format(_listeners))

    print("simulate: running through all set instructions")
    for _set_instruction in _sets:
        _state = _handle_set_instruction(_state, _set_instruction)
        print("simulate: handled set instruction: {}, got new state: {}".format(_set_instruction, _state))

    for i, _robot in enumerate(_robots):
        print("{}: {}".format(i, _robot))

    robot_ran = True
    while robot_ran:
        robot_ran = False
        _robots, _outputs = _state
        for i, _robot in enumerate(_robots):
            _low, _high = _robot
            _can_send = _low > 0 and _high > 0
            print("{}: {}: send? {}".format(i, _robot, _can_send))
            if _can_send:
                robot_ran = True
                _robot_instructions = _listeners[i]
                print("robot #{} ({}) can now carry out instructions: {}".format(i, _robot, _robot_instructions))
                _state = _handle_send_instructions(_state, _robot_instructions)
                _listeners[i] = list()
                print("got new state: {}".format(_state))
    return _state


if __name__ == "__main__":

    # test set
    assert _set(5, (-1, -1)) == (-1, 5)
    assert _set(5, (0, 0)) == (0, 5)
    assert _set(5, (0, 6)) == (0, 6)
    assert _set(7, (0, 5)) == (0, 7)
    assert _set(5, (-1, 6)) == (5, 6)
    assert _set(5, (-1, 6)) == (5, 6)
    assert _set(5, (10, 13)) == (5, 13)

    # test parsing instructions
    _raw = "value 71 goes to bot 52"
    assert parse_instruction(_raw) == [(71, 52)]
    _raw = "bot 159 gives low to bot 8 and high to bot 175"
    assert parse_instruction(_raw) == [(159, True, True, 8), (159, False, True, 175)]
    _raw = "bot 123 gives low to output 8 and high to bot 321"
    assert parse_instruction(_raw) == [(123, True, False, 8), (123, False, True, 321)]
    _raw = "bot 123 gives low to output 8 and high to output 321"
    assert parse_instruction(_raw) == [(123, True, False, 8), (123, False, False, 321)]
    _raw = "bot 123 gives low to bot 8 and high to output 321"
    assert parse_instruction(_raw) == [(123, True, True, 8), (123, False, False, 321)]

    # test handling set instructions
    assert _handle_set_instruction(_new_state(_robots=[(0, 0)],
                                              _outputs=[]), (5, 0)) \
           == _new_state(_robots=[(0, 5)], _outputs=[])
    assert _handle_set_instruction(_new_state(_robots=[(-1, 7)],
                                              _outputs=[]), (5, 0)) \
           == _new_state(_robots=[(5, 7)], _outputs=[])
    assert _handle_set_instruction(_new_state(_robots=[(5, 7), (1, 1), (-1, 10)],
                                              _outputs=[10]), (5, 2)) \
           == _new_state(_robots=[(5, 7), (1, 1), (5, 10)], _outputs=[10])

    test_instructions = ["value 5 goes to bot 2", "bot 2 gives low to bot 1 and high to bot 0", "value 3 goes to bot 1",
                         "bot 1 gives low to output 1 and high to bot 0",
                         "bot 0 gives low to output 2 and high to output 0",
                         "value 2 goes to bot 2"]
    instructions = []
    for instruction in map(parse_instruction, test_instructions):
        instructions.extend(instruction)
    _, results = simulate(instructions)
    assert results[:3] == [5, 2, 3]


