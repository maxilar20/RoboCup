from SimController import *

# Initializing controller
simcontroller = SimController(max_game_time_mins=0.2)

# Resetting values
simcontroller.reset_timer()
simcontroller.reset_simulation()

# Spawning entities
simcontroller.spawn_players()
simcontroller.spawn_ball()

TIME_STEP = 32
# Running time step
i = 0
while simcontroller.step(TIME_STEP) != -1:

    if simcontroller.time_up():
        break

    if simcontroller.goal():
        simcontroller.increment_counter()

    if simcontroller.ball_out():
        simcontroller.reset_simulation()

    i += 1

simcontroller.end_simulation()
