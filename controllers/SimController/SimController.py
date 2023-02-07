from controller import Supervisor
from Entity import *
from GUI import *
import time


class SimController(Supervisor):
    def __init__(self, max_game_time_mins=15):
        super().__init__()

        self.GUI = GUI()

        self.start_game_time_seconds = 0
        self.max_game_time_secs = max_game_time_mins * 60

        self.red_score = 0
        self.blue_score = 0

    def run(self):
        self.GUI.runGUI(
            self.ball_pos,
            f"{self.time_passed_text}    Red {self.red_score} | {self.blue_score} Blue",
            self.players,
        )

    def reset_timer(self):
        print("Starting time")
        self.start_game_time_seconds = time.time()

    def reset_simulation(self):
        self.ball.reset()
        for player in self.players:
            player.reset()

    def spawn_players(self):
        self.players = [Player(self, **player) for player in player_definitions]

    def spawn_ball(self):
        self.ball = Ball(self)

    def inside_goal(self):
        if self.ball_pos[0] < -4.55 and self.ball_pos[1] < 0.7:
            return "blue"
        elif self.ball_pos[0] > 4.55 and self.ball_pos[1] < 0.7:
            return "red"

    def get_ball_pos(self):
        self.ball_pos = self.ball.getPosition()

    def ball_out(self):
        return abs(self.ball_pos[1]) > 3 or abs(self.ball_pos[0]) > 4.5

    def get_time(self):
        self.time_passed = time.time() - self.start_game_time_seconds
        self.time_passed_text = time.strftime("%M:%S", time.gmtime(self.time_passed))

    def time_up(self):
        time_passed = time.time() - self.start_game_time_seconds
        return time_passed > self.max_game_time_secs

    def end_simulation(self):
        print("Sim ended")

    def mapToGUI(self, pos):
        return (
            self.map_range(
                pos[0],
                -5,
                5,
                0,
                500,
            ),
            self.map_range(
                pos[1],
                -3.5,
                3.5,
                0,
                350,
            ),
        )

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def check_goal(self):
        if self.inside_goal() == "blue":
            self.blue_score += 1
            return True
        elif self.inside_goal() == "red":
            self.red_score += 1
            return True
        else:
            return False


player_definitions = [
    {
        "player": "1",
        "team": "red",
        "player_position": "goalie",
        "translation": "-4 0 0.4",
    },
    {
        "player": "2",
        "team": "red",
        "player_position": "defender",
        "translation": "-2.5 0 0.4",
    },
    {
        "player": "3",
        "team": "red",
        "player_position": "attacker_left",
        "translation": "-1 0.5 0.4",
    },
    {
        "player": "4",
        "team": "red",
        "player_position": "attacker_right",
        "translation": "-1 -0.5 0.4",
    },
    {
        "player": "1",
        "team": "blue",
        "player_position": "goalie",
        "translation": "4 0 0.4",
    },
    {
        "player": "2",
        "team": "blue",
        "player_position": "defender",
        "translation": "2.5 0 0.4",
    },
    {
        "player": "3",
        "team": "blue",
        "player_position": "attacker_left",
        "translation": "1 -0.5 0.4",
    },
    {
        "player": "4",
        "team": "blue",
        "player_position": "attacker_right",
        "translation": "1 0.5 0.4",
    },
]

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
