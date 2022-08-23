import pure_robot
import deliever_robot

def create_robot():
    return pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

def move(howFar, state):
    return pure_robot.move(pure_robot.transfer_to_cleaner, howFar, state)

def turn(angle, state):
    return turn(angle, state)

#..etc
#If we want to use deliever Robot with different interface

def create_deliever_robot():
    return deliever_robot.DelieverState(0.0, 0.0, 0, 0)

# If methods intersect....
def move_deliever(howFar, state):
    return deliever_robot.move(deliever_robot.transfer_to_cleaner, howFar, state)

#...etc

def do_robot(method, howFar, state):
    return method(howFar, state)

