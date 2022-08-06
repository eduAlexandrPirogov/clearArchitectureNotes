import math

x = 0.0
y = 0.0
angle = 0

isClearing = False
states = ["water", "soap", "brush"]
currentState = states[0]


robotClearing = clearing()
robotMovement = movement()

def turn(angle):
        if angle + angle <= 360:
            angle += angle
        elif angle + angle > 360:
            angle = angle + angle - 360
        elif angle - angle < 360:
            angle = 0 - (angle + angle-360)
    
def move(sm):
        x += sm * math.cos(angle)
        y += sm * math.sin(angle)
        print("Robot arrived at ", x, " ", y)

def start():
        isClearing = True

def stop():
        isClearing = False

def set(state):
        currentState = state


