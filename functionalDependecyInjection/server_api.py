import cleaner_api
import deliever_robot
import itertools
#..etc
#If we want to use deliever Robot with different interface

def create_robot():
    return cleaner_api.create_robot()

def create_deliever_robot():
    return deliever_robot.DelieverState(0.0, 0.0, 0, 0)

#...etc

def do_cleaner_robot(code, state):
   for command in code:
            cmd = command.split(' ')
            print(cmd[0])
            if cmd[0] == 'move':
                new_state = cleaner_api.move(
                        int(cmd[1]), state)
            elif cmd[0] == 'turn':
                new_state = cleaner_api.turn(
                        int(cmd[1]), state)
            elif cmd[0] == 'set':
                new_state = cleaner_api.set_state( cmd[1], state)
            elif cmd[0] == 'start':
                new_state = cleaner_api.start( state)
            elif cmd[0] == 'stop':
                new_state = cleaner_api.stop( state)
            return new_state

def do_robot(command, state):
    #if state
    inst = state.__class__.__name__
    if  inst == "RobotState":
        return do_cleaner_robot(command, state)
    elif inst == "DelieverState":
        return do_deliever_robot(command, state)
