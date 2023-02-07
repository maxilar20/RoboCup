from SimController import *


# Initializing controller
simcontroller = SimController(max_game_time_mins=1)

# Resetting values
simcontroller.reset_timer()

# Spawning entities
simcontroller.spawn_players()
simcontroller.spawn_ball()

blue_score = 0
red_score = 0

TIME_STEP = 32
# Running time step
i = 0
while simcontroller.step(TIME_STEP) != -1:

    simcontroller.get_ball_pos()
    simcontroller.get_time()

    simcontroller.run()

    if simcontroller.time_up():
        break

    if simcontroller.check_goal():
        print("GOAL!")
        simcontroller.reset_simulation()

    # if simcontroller.ball_out():
    #     print("Ball out of field")
    #     simcontroller.reset_simulation()

    i += 1

pygame.quit()

simcontroller.end_simulation()

print("Final Red team score: ", red_score)
print("Final Blue team score: ", blue_score)
