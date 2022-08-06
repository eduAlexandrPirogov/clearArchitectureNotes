import math

x = 0.0
y = 0.0
angle = 0

def __init__():
        x = 0.0
        y = 0.0
        angle = 0

def turn( angle):
        if angle + angle <= 360:
            angle += angle
        elif angle + angle > 360:
            angle = angle + angle - 360
        elif angle - angle < 360:
            angle = 0 - (angle + angle-360)
    
def move( sm):
        x += sm * math.cos(angle)
        y += sm * math.sin(angle)


def __init__():
        isClearing = False
        states = ["water", "soap", "brush"]
        currentState = states[0]

def start():
        isClearing = True

def stop():
        isClearing = False

def set( state):
        currentState = state


def __init__():
        robotClearing = clearing()
        robotMovement = movement()

def move( sm):
        robotMovement.move(sm)
        print("Robot arrived at ", robotMovement.x, " ", robotMovement.y)

def turn( angle):
        robotMovement.turn(angle)
        print("Robot turned at ", angle)

    #setting clearing state
    #better clear methods make as enums/classes
def set( state):
        robotClearing.set(state)
        print("Robot has set state " + state)

def start():
        robotClearing.start()
        print("Robot has started washing with " + robotClearing.currentState)

def stop():
        robotClearing.stop()
        print("Robot has stoped washing with " + robotClearing.currentState)

