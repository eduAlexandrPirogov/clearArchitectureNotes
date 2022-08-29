import pure_robot
from pymonad import *


#can't understand how to resolve it

class intMonad:

    def __init__(self, num):
        self.num = num

    def getVal(self):
        return self.num

    def bind(self, monad, function):
        return Monad(function(monad.getVal()))

def bind(monad, function):
    return intMonad(function(monad.getVal()))

x = bind(intMonad(5), lambda a : a + 2)
y = bind(x, lambda a : a + 1)
print(y.getVal())

class Monad:

    def __init__(self, state):
        self.state = state

    def getVal(self):
        return self.state

def transfer(msg):
    print(msg)

r = Monad(pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER))
x1 = bind(r, pure_robot.move(transfer, 50))
