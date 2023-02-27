from controller import Supervisor
from Objects import Player, Ball, Field, GUI, Button
from coach import Coach
from config import GAME_TIME, PLAYERS_DEF, BOUNDARIES

import pygame

import time


class SimController(Supervisor):
    def __init__(self, BOUNDARIES, max_game_time_mins=15):
        super().__init__()

        self.time_passed = 0
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
        self.red_coach = Coach(
            self.red_team, self.blue_team, self.field, self.ball, self.GUI
        )
        self.blue_coach = Coach(
            self.blue_team, self.red_team, self.field, self.ball, self.GUI
        )

        self.latest_player = None

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

    def run(self):
        # SIMULATION
        self.time_passed += self.timeStep / 1000
        self.time_passed_text = time.strftime("%M:%S", time.gmtime(self.time_passed))

        # Time up check
        if simcontroller.time_up():
            simcontroller.end_simulation()

        # Goal check
        if simcontroller.check_goal():
            simcontroller.kickoff_position()

        # Ball out check
        closest, closest_dist = self.detect_closest(self.ball)
        if closest_dist < 0.4:
            self.latest_player = closest

        if simcontroller.ball_out():
            if self.latest_player:
                self.GUI.start_display(f"Ball Out by {self.latest_player.name}")
                if self.latest_player.team == "red":
                    self.red_coach.freeze(self.time_passed, 5)
                elif self.latest_player.team == "red":
                    self.blue_coach.freeze(self.time_passed, 5)

        # Penalty check
        for player in self.players:
            if player.hasFallen():
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
                            self.blue_coach.freeze(self.time_passed, 5)
                else:
                    self.GUI.start_display("Fell by itself", time_s=1)

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
        for player in self.players:
            player.getPosition()
        self.ball.getPosition()

        self.red_coach.act(self.time_passed)
        self.blue_coach.act(self.time_passed)

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

    def kickoff_position(self):
        self.ball.resetPosition()
        self.ball.resetPhysics()
        for player in self.players:
            player.resetPosition()
            player.resetOrientation()
            player.resetPhysics()
        self.latest_player = None

        self.red_coach.state = "Attacking"
        self.blue_coach.state = "Attacking"

    def penalty_position(self, team):
        if team == "red":
            self.red_coach.state = "Penalty own"
            self.blue_coach.state = "Penalty other"
            self.ball.setPosition([3.2, -0.1, 0.3])
        elif team == "blue":
            self.red_coach.state = "Penalty other"
            self.blue_coach.state = "Penalty own"
            self.ball.setPosition([-3.2, -0.1, 0.3])

        for player in self.players:
            player.setPosition(player.penalty_pos)
            player.resetOrientation()
        self.latest_player = None

    def check_goal(self):
        if self.field.isInside(self.ball.getPosition(), "goal_red"):
            self.blue_score += 1
            print("Blue Team Scored")
            self.GUI.start_display("Blue team has scored")
            return True
        elif self.field.isInside(self.ball.getPosition(), "goal_blue"):
            self.red_score += 1
            print("Red Team Scored")
            self.GUI.start_display("Red team has scored")
            return True
        else:
            return False

    def ball_out(self):
        return not self.field.isInside(self.ball.getPosition(), "field")

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
