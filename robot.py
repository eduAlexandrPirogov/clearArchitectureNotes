import math

class movement:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0

    def turn(self, angle):
        if self.angle + angle <= 360:
            self.angle += angle
        elif self.angle + angle > 360:
            self.angle = self.angle + angle - 360
        elif self.angle - angle < 360:
            self.angle = 0 - (self.angle + angle-360)
    
    def move(self, sm):
        self.x += sm * math.cos(self.angle)
        self.y += sm * math.sin(self.angle)

class clearing:
    def __init__(self):
        self.isClearing = False
        self.states = ["water", "soap", "brush"]
        self.currentState = self.states[0]

    def start(self):
        self.isClearing = True

    def stop(self):
        self.isClearing = False

    def set(self, state):
        self.currentState = state

class robot:
    def __init__(self):
        self.robotClearing = clearing()
        self.robotMovement = movement()

    def move(self, sm):
        self.robotMovement.move(sm)
        print("Robot arrived at ", self.robotMovement.x, " ", self.robotMovement.y)

    def turn(self, angle):
        self.robotMovement.turn(angle)
        print("Robot turned at ", angle)

    #setting clearing state
    #better clear methods make as enums/classes
    def set(self, state):
        self.robotClearing.set(state)
        print("Robot has set state " + state)

    def start(self):
        self.robotClearing.start()
        print("Robot has started washing with " + self.robotClearing.currentState)

    def stop(self):
        self.robotClearing.stop()
        print("Robot has stoped washing with " + self.robotClearing.currentState)

 
r = robot()
inp = "";
while(inp != "exit"):
    inp = input("> ")
    if inp == "stop":
        r.stop()
    elif inp == "start":
        r.start()
    #...etc
    else:
        print("unknown command")
