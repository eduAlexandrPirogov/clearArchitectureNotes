import server_api

state = server_api.create_robot()

server_api.do_robot(('move 50', 'turn 90'), state)

#deliever = server_api.create_deliever_robot()
#server_api.do_robot(server_api.move_deliever, 50, deliever)
