import pure_robot

class RobotApi:

    def setup(self, f_move, f_turn, f_set_state, f_start, f_stop,
            f_transfer):
        self.f_move = f_move
        self.f_turn = f_turn
        self.f_set_state = f_set_state
        self.f_start = f_start
        self.f_stop = f_stop
        self.f_transfer = f_transfer

    def add_function(self, name, function):
        self.dict[name] = function

    def executeMoveCommand(self, command, arg):
        if command == 'move':
            self.cleaner_state = self.dict[command](self.dict['msg'], int(arg),
                    self.cleaner_state)
        elif command == 'turn':
            self.cleaner_state = self.dict[command](self.dict['msg'], int(arg),
                    self.cleaner_state)



    def make(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        cmd = command.split(' ')
        isCommand = False
        arg = -1
        for var in cmd:
            if var.isnumeric():
                isCommand = True
                arg = int(var)
            elif var == 'set':
                self.cleaner_state = self.dict[var](self.dict['msg'], var,
                    self.cleaner_state)
            elif var == 'start':
                self.cleaner_state = self.dict[var](self.dict['msg'], self.cleaner_state)
            elif var == 'stop':
                self.cleaner_state = self.dict[var](self.dict['msg'], self.cleaner_state)
            elif isCommand:
                self.executeMoveCommand(var, arg)
                isCommand = False
                    
    def __init__(self):
        self.dict = {}

    def __call__(self, command):
        return self.make(command)

def transfer_to_cleaner(message):
    print(message)

api = RobotApi()
api.add_function('move', pure_robot.move)
api.add_function('turn', pure_robot.turn)
api.add_function('set', pure_robot.set_state)
api.add_function('start', pure_robot.start)
api.add_function('stop', pure_robot.stop)
api.add_function('msg', pure_robot.transfer_to_cleaner)
#api.setup(pure_robot.move, pure_robot.turn, pure_robot.set_state, 
#        pure_robot.start, pure_robot.stop, transfer_to_cleaner)
