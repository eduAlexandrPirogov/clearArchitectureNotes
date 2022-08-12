import math
import clearing
import movement

class robot:
    def __init__(self):
        self.robotClearing = clearing.clearing()
        self.robotMovement = movement.movement()

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
