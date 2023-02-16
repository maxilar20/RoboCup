from controller import Supervisor
from Objects.Player import *
from Objects.Ball import *
from Objects.Field import *
from Objects.Button import *
from Objects.GUI import *
from Objects.CONFIG import *
import time


class SimController(Supervisor):
    def __init__(self, boundaries, max_game_time_mins=15):
        super().__init__()

        self.boundaries = boundaries

        self.GUI = GUI()

        self.field = Field(boundaries, self.GUI)

        self.debug = False
        self.button1 = Button(self.GUI.screen, (10, 10), "Debug", 20, "black on white")

        self.start_game_time_seconds = time.time()
        self.max_game_time_secs = max_game_time_mins * 60

        self.red_score = 0
        self.blue_score = 0

        self.keyboard = self.getKeyboard()
        self.timeStep = int(self.getBasicTimeStep())
        self.keyboard.enable(10 * self.timeStep)

        self.emitter = self.getDevice("emitter")

        self.ball = Ball(self, self.GUI)

        self.players = [
            Player(self, **player, GUI=self.GUI, emitter=self.emitter, ball=self.ball)
            for player in player_definitions
        ]

    def run(self):
        ###################### SIMULATION ######################
        simcontroller.get_time()

        if simcontroller.time_up():
            simcontroller.end_simulation()

        if simcontroller.check_goal():
            simcontroller.reset_simulation()

        if simcontroller.ball_out():
            print("Ball Out")
            simcontroller.reset_simulation()

        # TODO: Check if there's been a fault

        ######################   Update  ######################

        for player in self.players:
            player.getPosition()

        for player in self.players:
            player.senseDistances(self.field, self.players)

        ######################   Run  ######################

        # for player in self.players:
        #     player.act()
        # self.players[0].act()

        self.moveRobot()

        ######################   GUI  ######################
        self.GUI.run()

        self.field.show()

        for player in self.players:
            player.showPlayer()
            if self.debug:
                player.showSensors()

        self.ball.show()

        self.debug = self.button1.update()
        self.GUI.drawText(self.time_passed_text, self.red_score, self.blue_score)

        self.GUI.flip()

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

    def reset_simulation(self):
        self.ball.reset()
        for player in self.players:
            player.reset()

    def check_goal(self):
        if self.field.isInside(self.ball.getPosition(), "goal_red"):
            self.blue_score += 1
            print("Blue Team Scored")
            return True
        elif self.field.isInside(self.ball.getPosition(), "goal_blue"):
            self.red_score += 1
            print("Red Team Scored")
            return True
        else:
            return False

    def ball_out(self):
        return not self.field.isInside(self.ball.getPosition(), "field")

    def get_time(self):
        self.time_passed = time.time() - self.start_game_time_seconds
        self.time_passed_text = time.strftime("%M:%S", time.gmtime(self.time_passed))

    def time_up(self):
        return self.time_passed > self.max_game_time_secs

    def end_simulation(self):
        print("Sim ended")


if __name__ == "__main__":

    simcontroller = SimController(boundaries, max_game_time_mins=GAME_TIME)

    TIME_STEP = 32
    while simcontroller.step(TIME_STEP) != -1:
        simcontroller.run()

    pygame.quit()
