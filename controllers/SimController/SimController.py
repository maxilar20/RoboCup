from controller import Supervisor
from objects import Player, Ball, Field, GUI, Button
from coach import Coach
from config import GAME_TIME, PLAYERS_DEF, BOUNDARIES

import pygame

import time


class SimController(Supervisor):
    def __init__(self, BOUNDARIES, max_game_time_mins=15):
        super().__init__()

        self.start_game_time_seconds = time.time()
        self.max_game_time_secs = max_game_time_mins * 60

        self.red_score = 0
        self.blue_score = 0

        self.timeStep = int(self.getBasicTimeStep())

        self.emitter = self.getDevice("emitter")

        self.GUI = GUI()

        self.BOUNDARIES = BOUNDARIES
        self.field = Field(BOUNDARIES)

        self.debug = False
        self.debug_button = Button((10, 10), "Debug", 20, "black on white")
        self.buttons = [self.debug_button]

        self.ball = Ball(self)

        self.players = [
            Player(self, **player, emitter=self.emitter) for player in PLAYERS_DEF
        ]

        self.red_team = [player for player in self.players if player.team == "red"]
        self.blue_team = [player for player in self.players if player.team == "blue"]
        self.red_coach = Coach(self.red_team, self.blue_team, self.field, self.ball)
        self.blue_coach = Coach(self.blue_team, self.red_team, self.field, self.ball)

    def run(self):
        # SIMULATION
        simcontroller.get_time()

        if simcontroller.time_up():
            simcontroller.end_simulation()

        if simcontroller.check_goal():
            simcontroller.reset_simulation()

        if simcontroller.ball_out():
            print("Ball Out")
            simcontroller.reset_simulation()

        # TODO: Check if there's been a fault

        # Run

        # for player in self.players:
        #     player.act()
        # self.players[0].act()

        # self.moveRobot(3)

        # GUI
        self.debug = self.debug_button.update()
        scores = (self.red_score, self.blue_score)
        self.GUI.show(
            self.debug,
            self.time_passed_text,
            scores,
            self.field,
            self.ball,
            self.players,
            self.buttons,
        )

        # Update
        self.red_coach.act(self.GUI)

        self.GUI.flip()

    def moveRobot(self, channel=0):
        message = [0.0, 0.0, 0.0, 0.0]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            message[0] += -1.0

        if keys[pygame.K_d]:
            message[0] += 1.0

        if keys[pygame.K_w]:
            message[1] += 1.0

        if keys[pygame.K_s]:
            message[1] += -1.0

        if keys[pygame.K_q]:
            message[2] += -1.0

        if keys[pygame.K_e]:
            message[2] += 1.0

        if keys[pygame.K_SPACE]:
            message[3] = 1

        if keys[pygame.K_r]:
            message[3] = 2

        self.emitter.setChannel(channel)
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

    simcontroller = SimController(BOUNDARIES, max_game_time_mins=GAME_TIME)

    TIME_STEP = 32
    while simcontroller.step(TIME_STEP) != -1:
        simcontroller.run()

    pygame.quit()
