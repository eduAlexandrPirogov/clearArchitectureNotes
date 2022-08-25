import pure_robot

class RobotApi:

    def __init__(self):
        self.dict = {}

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

    def make(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        cmd = command.split(' ')
        if cmd[0] == 'move':
            self.cleaner_state = self.dict[cmd[0]](self.dict['msg'], int(cmd[1]),
                    self.cleaner_state)
        elif cmd[0] == 'turn':
            self.cleaner_state = self.dict[cmd[0]](self.dict['msg'], int(cmd[1]),
                    self.cleaner_state)
        elif cmd[0] == 'set':
            self.cleaner_state = self.dict[cmd[0]](self.dict['msg'], cmd[1],
                    self.cleaner_state)
        elif cmd[0] == 'start':
            self.cleaner_state = self.dict[cmd[0]](self.dict['msg'], self.cleaner_state)
        elif cmd[0] == 'stop':
            self.cleaner_state = self.dict[cmd[0]](self.dict['msg'], self.cleaner_state)

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
