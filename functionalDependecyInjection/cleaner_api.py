import pure_robot

def create_robot():
    return pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

def move(howFar, state):
    return pure_robot.move(pure_robot.transfer_to_cleaner, howFar, state)

def turn(angle, state):
    return turn(angle, state)
#..etc
#If we want to use deliever Robot with different interface
