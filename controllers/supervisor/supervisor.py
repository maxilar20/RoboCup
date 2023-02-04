from SimController import *

# Initializing controller
simcontroller = SimController(max_game_time_mins=1)

# Resetting values
simcontroller.reset_timer()
simcontroller.reset_simulation()

# Spawning entities
simcontroller.spawn_players()
simcontroller.spawn_ball()

blue_score = 0
red_score = 0

TIME_STEP = 32
# Running time step
i = 0
while simcontroller.step(TIME_STEP) != -1:

    if simcontroller.time_up():
        break

    if simcontroller.goal_check() == "blue": #problem with goal counting, keeps incrementing until while ends. Should only increment once.
        blue_score+=1
    elif simcontroller.goal_check() == "red":
        red_score+=1

    if simcontroller.ball_out():
        simcontroller.reset_simulation()

    i += 1

simcontroller.end_simulation()

print("Red team score: ", red_score)
print("Blue team score: ", blue_score)