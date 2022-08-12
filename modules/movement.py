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
