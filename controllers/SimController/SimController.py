from controller import Supervisor
from Objects import Player, Ball, Field, GUI, Button
from coach import Coach
from config import GAME_TIME, PLAYERS_DEF, BOUNDARIES
import random

import pygame
from pygame.math import Vector2 as vec2


class SimController(Supervisor):
    def __init__(self, BOUNDARIES, max_game_time_mins=15):
        super().__init__()

        self.time_passed = 0
        self.max_game_time_secs = max_game_time_mins * 60
        self.timeStep = int(self.getBasicTimeStep())

        self.red_score = 0
        self.blue_score = 0

        self.GUI = GUI()

        self.debug_button = Button((10, 10), "Debug", 20, "black on white")
        self.buttons = [self.debug_button]
        self.field = Field(BOUNDARIES)
        self.ball = Ball(self)

        emitter = self.getDevice("emitter")
        self.players = [
            Player(self, **player, emitter=emitter) for player in PLAYERS_DEF
        ]

        red_team = [player for player in self.players if player.team == "red"]
        blue_team = [player for player in self.players if player.team == "blue"]

        self.red_coach = Coach(red_team, blue_team, self.field, self.ball, self.GUI)
        self.blue_coach = Coach(blue_team, red_team, self.field, self.ball, self.GUI)

        self.latest_player = None
        self.starting_team = random.choice(["red", "blue"])

    def run(self):
        self.time_passed += self.timeStep / 1000

        if simcontroller.is_time_up():
            simcontroller.end_simulation()

        if simcontroller.is_goal():
            simcontroller.kickoff_position()

        if simcontroller.is_ball_out() and self.latest_player:
            self.ball_out()

        for player in self.players:
            if player.hasFallen():
                self.fault(player)

        # GUI
        scores = (self.red_score, self.blue_score)
        self.GUI.show(
            self.time_passed, scores, self.field, self.ball, self.players, self.buttons
        )

        # Update
        for player in self.players:
            player.getPosition()
        self.ball.getPosition()

        closest, closest_dist = self.detect_closest(self.ball)
        if closest_dist < 0.4:
            self.latest_player = closest

        if self.latest_player is None:
            if self.starting_team == "red":
                self.blue_coach.freeze(self.time_passed, 1)
            else:
                self.red_coach.freeze(self.time_passed, 1)

        self.red_coach.act(self.time_passed)
        self.blue_coach.act(self.time_passed)

        self.GUI.flip()

    # Conditions
    def is_time_up(self):
        return self.time_passed > self.max_game_time_secs

    def is_goal(self):
        if self.field.isInside(self.ball.getPosition(), "goal_red"):
            self.blue_score += 1
            self.starting_team = "red"
            self.GUI.start_display("Blue team has scored")
            return True
        elif self.field.isInside(self.ball.getPosition(), "goal_blue"):
            self.red_score += 1
            self.starting_team = "blue"
            self.GUI.start_display("Red team has scored")
            return True
        else:
            return False

    def is_ball_out(self):
        return not self.field.isInside(self.ball.getPosition(), "field")

    # Actions
    def ball_out(self):
        self.ball.resetPhysics()

        new_pos = self.ball.position + vec2(
            random.choice([-0.05, 0.05]), random.choice([-0.05, 0.05])
        )
        while not self.field.isInside(new_pos):
            new_pos = self.ball.position + vec2(
                random.choice([-0.05, 0.05]), random.choice([-0.05, 0.05])
            )
        self.ball.setPosition([new_pos[0], new_pos[1], 0.2])

        self.GUI.start_display(f"Ball Out by {self.latest_player.name}")
        if self.latest_player.team == "red":
            self.red_coach.freeze(self.time_passed, 5)
        elif self.latest_player.team == "blue":
            self.blue_coach.freeze(self.time_passed, 5)

    def fault(self, player):
        player.resetHeight()
        player.resetOrientation()
        player.resetPhysics()

        closest_player, closest_dist = self.detect_closest(player)
        if closest_dist < 0.6 and player.team != closest_player.team:
            msg = f"Player {closest_player.name} made a fault to {player.name}"
            self.GUI.start_display(msg)

            if player.team == "red":
                if self.field.isInside(player.position, "penalty_blue"):
                    self.penalty_position("red")
                    self.GUI.start_display("Red team gets penalty")
                else:
                    self.blue_coach.freeze(self.time_passed, 5)
            elif player.team == "blue":
                if self.field.isInside(player.position, "penalty_red"):
                    self.penalty_position("blue")
                    self.GUI.start_display("Blue team gets penalty")
                else:
                    self.red_coach.freeze(self.time_passed, 5)
        else:
            self.GUI.start_display("Fell by itself", time_s=1)

    def end_simulation(self):
        print("Sim ended")

    def kickoff_position(self):
        self.ball.resetPosition()
        self.ball.resetPhysics()
        for player in self.players:
            player.resetPosition()
            player.resetOrientation()
            player.resetPhysics()
        self.latest_player = None

    def penalty_position(self, team):
        if team == "red":
            self.red_coach.state = "Penalty own"
            self.blue_coach.state = "Penalty other"
            self.ball.setPosition([3.2, -0.1, 0.3])
        elif team == "blue":
            self.red_coach.state = "Penalty other"
            self.blue_coach.state = "Penalty own"
            self.ball.setPosition([-3.2, -0.1, 0.3])

        self.ball.resetPhysics()
        for player in self.players:
            player.setPosition(player.penalty_pos)
            player.resetOrientation()

    def detect_closest(self, player):
        closest = None
        closest_dist = 99
        for other_player in self.players:
            if player != other_player:
                dist = (player.position - other_player.position).magnitude()
                if dist < closest_dist:
                    closest = other_player
                    closest_dist = dist
        return closest, closest_dist


if __name__ == "__main__":

    simcontroller = SimController(BOUNDARIES, max_game_time_mins=GAME_TIME)

    TIME_STEP = 32
    while simcontroller.step(TIME_STEP) != -1:
        simcontroller.run()

    pygame.quit()
