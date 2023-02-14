from controller import Supervisor
from Entity import *
from GUI import *
from CONFIG import *
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

        self.keyboard = self.getKeyboard()
        self.timeStep = int(self.getBasicTimeStep())
        self.keyboard.enable(10 * self.timeStep)

        self.emitter = self.getDevice("emitter")

    def run(self):
        self.moveRobot()

        for player in self.players:
            player.getPosition()

        for player in self.players:
            player.senseDistances(self.players)

        simcontroller.get_time()

        self.runGUI()

        if simcontroller.time_up():
            simcontroller.end_simulation()

        if simcontroller.check_goal():
            simcontroller.reset_simulation()

        if simcontroller.ball_out():
            simcontroller.reset_simulation()

        # TODO: Check if there's been message fault

    def moveRobot(self, channel=0):
        message = [0.0, 0.0, 0.0]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            message[0] += -1.0

        if keys[pygame.K_RIGHT]:
            message[0] += 1.0

        if keys[pygame.K_UP]:
            message[1] += 1.0

        if keys[pygame.K_DOWN]:
            message[1] += -1.0

        self.emitter.send(message)

    def runGUI(self):
        score_text = f"    Red {self.red_score} | {self.blue_score} Blue"
        self.GUI.runGUI(
            self.ball, self.players, self.time_passed_text + score_text, self.boundaries
        )

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
        pos.x > boundary[0].x
        and pos.x < boundary[1].x
        and pos.y < boundary[0].y
        and pos.y > boundary[1].y
    )


if __name__ == "__main__":

    simcontroller = SimController(boundaries, max_game_time_mins=GAME_TIME)

    TIME_STEP = 32
    while simcontroller.step(TIME_STEP) != -1:
        simcontroller.run()

    pygame.quit()
