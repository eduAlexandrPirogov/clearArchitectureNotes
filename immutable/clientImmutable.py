from RobotApiImmutable import CleanerApi

cleaner_api = CleanerApi()

client_robot = cleaner_api.create_new_robot()
"""
client_robot = cleaner_api.activate_cleaner(('move 100'), client_robot)
client_robot = cleaner_api.activate_cleaner('turn -90', client_robot)
client_robot = cleaner_api.activate_cleaner('set soap', client_robot)
client_robot = cleaner_api.activate_cleaner('start', client_robot)
client_robot = cleaner_api.activate_cleaner('move 50', client_robot)
client_robot = cleaner_api.activate_cleaner('stop', client_robot)
"""
client_robot = cleaner_api.activate_cleaner((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
    ), client_robot)

print (cleaner_api.get_x(client_robot),
        cleaner_api.get_y(client_robot),
        cleaner_api.get_angle(client_robot),
        cleaner_api.get_state(client_robot))

