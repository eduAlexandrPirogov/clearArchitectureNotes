import pure_robot

def print_state(msg):
    print(msg)

#creating robot
def createRobot():
    return pure_robot.RobotState("RobotState", "x y angle state")

def moveRobot(howFar, RobotState):
    return move(print_state, howFar, RobotState);

def turnRobot(anlge, RobotState):
    return turn(print_state, angle, RobotState)

def setState(typeState, RobotState):
    if typeState != "WATER" or typeState != "BRUSH" or typeState != "SOAP":
        return RobotState
    return set_state(print_state, typeState, RobotState)

def start(RobotState):
    return start(print_state, RobotState)

def stop(RobotState):
    return stop(print_state, RobotState)
