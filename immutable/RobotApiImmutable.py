import pure_robot

class CleanerApi:

   # def __init__(:
   #     cleaner_state = pure_robot.RobotState(0.0,0.0,0, pure_robot.WATER)
    
    def create_new_robot(self):
        return pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    def transfer_to_clearner(self, message):
        print(message)

    def get_x(self, cleaner_state):
        return cleaner_state.x

    def get_y(self, cleaner_state):
        return cleaner_state.y

    def get_angle(self, cleaner_state):
        return cleaner_state.angle

    def get_state(self, cleaner_state):
        return cleaner_state.state

    def activate_cleaner(self, code, cleaner_state): 
        for command in code:
            cmd = command.split(' ') 
            if cmd[0] == 'move':
                cleaner_state = pure_robot.move(self.transfer_to_clearner,
                        int(cmd[1]), cleaner_state)
            elif cmd[0] == 'turn':
                cleaner_state = pure_robot.turn(self.transfer_to_clearner,
                        int(cmd[1]), cleaner_state)
            elif cmd[0] == 'set':
                cleaner_state = pure_robot.set_state(self.transfer_to_clearner, cmd[1], cleaner_state)
            elif cmd[0] == 'start':
                cleaner_state = pure_robot.start(self.transfer_to_clearner, cleaner_state)
            elif cmd[0] == 'stop':
                cleaner_state = pure_robot.stop(self.transfer_to_clearner, cleaner_state)
        return cleaner_state
