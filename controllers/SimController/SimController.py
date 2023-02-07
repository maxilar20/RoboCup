from controller import Supervisor
from Entity import *
from GUI import *
import time


class SimController(Supervisor):
    def __init__(self, max_game_time_mins=15):
        super().__init__()

        self.start_game_time_seconds = time.time()
        self.max_game_time_secs = max_game_time_mins * 60

        self.GUI = GUI()

        self.red_score = 0
        self.blue_score = 0

        self.players = [Player(self, **player) for player in player_definitions]
        self.ball = Ball(self)

    def run(self):

        simcontroller.get_ball_pos()
        simcontroller.get_time()

        score_text = f"    Red {self.red_score} | {self.blue_score} Blue"
        self.GUI.runGUI(self.ball_pos, self.time_passed_text + score_text, self.players)

        if simcontroller.time_up():
            simcontroller.end_simulation()

        if simcontroller.check_goal():
            simcontroller.reset_simulation()

        if simcontroller.ball_out():
            simcontroller.reset_simulation()

    def reset_simulation(self):
        self.ball.reset()
        for player in self.players:
            player.reset()

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


if __name__ == "__main__":

    # Initializing controller
    simcontroller = SimController(max_game_time_mins=15)

    TIME_STEP = 32
    while simcontroller.step(TIME_STEP) != -1:
        simcontroller.run()

    pygame.quit()
