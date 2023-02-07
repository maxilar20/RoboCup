from controller import Supervisor
from Entity import *
from GUI import *
import time


class SimController(Supervisor):
    def __init__(self, boundaries, max_game_time_mins=15):
        super().__init__()

        self.boundaries = boundaries

        self.players = [Player(self, **player) for player in player_definitions]
        self.ball = Ball(self)

        self.start_game_time_seconds = time.time()
        self.max_game_time_secs = max_game_time_mins * 60

        self.red_score = 0
        self.blue_score = 0

        self.GUI = GUI()

    def run(self):
        simcontroller.get_time()

        score_text = f"    Red {self.red_score} | {self.blue_score} Blue"
        self.GUI.runGUI(
            self.ball, self.players, self.time_passed_text + score_text, self.boundaries
        )

        if simcontroller.time_up():
            simcontroller.end_simulation()

        if simcontroller.check_goal():
            simcontroller.reset_simulation()

        if simcontroller.ball_out():
            simcontroller.reset_simulation()

        # TODO: Check if there's been a fault

    def reset_simulation(self):
        self.ball.reset()
        for player in self.players:
            player.reset()

    def check_goal(self):
        if isInside(self.ball.getPosition(), self.boundaries["goal_red"]):
            self.blue_score += 1
            return True
        elif isInside(self.ball.getPosition(), self.boundaries["goal_blue"]):
            self.red_score += 1
            return True
        else:
            return False

    def ball_out(self):
        return not isInside(self.ball.getPosition(), self.boundaries["field"])

    def get_time(self):
        self.time_passed = time.time() - self.start_game_time_seconds
        self.time_passed_text = time.strftime("%M:%S", time.gmtime(self.time_passed))

    def time_up(self):
        return self.time_passed > self.max_game_time_secs

    def end_simulation(self):
        print("Sim ended")


def isInside(pos, boundary):
    return (
        pos[0] > boundary[0]
        and pos[0] < boundary[2]
        and pos[1] < boundary[1]
        and pos[1] > boundary[3]
    )


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

boundaries = {
    "goal_red": (-5, 0.7, -4.5, -0.7),
    "goal_blue": (4.5, 0.7, 5, -0.7),
    "field": (-4.5, 3, 4.5, -3),
    "penalty_red": (-4.5, 1, -4, -1),
    "penalty_blue": (4, 1, 4.5, -1),
}

if __name__ == "__main__":

    # Initializing controller
    simcontroller = SimController(boundaries, max_game_time_mins=15)

    TIME_STEP = 32
    while simcontroller.step(TIME_STEP) != -1:
        simcontroller.run()

    pygame.quit()
