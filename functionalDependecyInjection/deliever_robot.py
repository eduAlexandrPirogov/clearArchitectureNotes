import math
from collections import namedtuple

DelieverState = namedtuple("DelieverState", "x y angle cargoTonnage")


def transfer_to_cleaner(message):
    print(message)

def move(transfer, dist, state):
    angle_rads = state.angle * (math.pi/180.0)
    new_state = DelieverState(
            state.x + dist * math.cos(angle_rads),
            state.y + dist * math.sin(angle_rads),
            state.angle,
            state.cargoTonnage)
    transfer(('POS(',new_state.x,',',new_state.y,')'))
    return new_state

def turn(transfer, turn_angle, state):
    new_state = DelieverState(
            state.x,
            state.y,
            state.angle + turn_angle,
            state.state)
    transfer(('ANGLE',state.angle))
    return new_state

def add_cargo(tonnag, state):
    if tonagg + state.cargoTonnage <= 50:
        new_state = DelieverState(state.x, state.y, state.angle,
                state.cargoTonnage + tonnag)
    transfer(('cargoTonnage', state.cargoTonnage))
    return new_state

def start(transfer, state):
    transfer(('START WITH', state.state))
    return state

def stop(transfer, state):
    transfer(('STOP',))
    return state

def make(transfer, code, state):
    for command in code:
        cmd = command.split(' ') 
        if cmd[0] == 'move':
            state = move(transfer, int(cmd[1]), state)
        elif cmd[0] == 'turn':
            state = turn(transfer, int(cmd[1]), state)
        elif cmd[0] == 'set':
            state = set_state(transfer, cmd[1], state)
        elif cmd[0] == 'start':
            state = start(transfer, state)
        elif cmd[0] == 'stop':
            state = stop(transfer, state)
    return state


