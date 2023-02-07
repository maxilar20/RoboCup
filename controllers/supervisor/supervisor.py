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

    simcontroller.runGUI()

    if simcontroller.time_up():
        break

    if simcontroller.goal_check() == "blue":
        print("Goal scored, Scores as follows: ")
        blue_score += 1
        print("Red team score: ", red_score)
        print("Blue team score: ", blue_score)
        # print("Resetting simulation in 5...")
        simcontroller.reset_simulation()

    elif simcontroller.goal_check() == "red":
        print("Goal scored, Scores as follows: ")
        red_score += 1
        print("Red team score: ", red_score)
        print("Blue team score: ", blue_score)
        # print("Resetting simulation in 5s...")
        simcontroller.reset_simulation()

    elif simcontroller.ball_out():
        print("Ball out of field")
        simcontroller.reset_simulation()

    i += 1

pygame.quit()

simcontroller.end_simulation()

print("Final Red team score: ", red_score)
print("Final Blue team score: ", blue_score)
