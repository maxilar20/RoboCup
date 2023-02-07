from controller import Supervisor
from Player import *
import time

import pygame

pygame.init()

PADDING = 0
SCALE = 1


class SimController(Supervisor):
    def __init__(self, max_game_time_mins=15):
        super().__init__()

        self.screen = pygame.display.set_mode([500, 350])
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        self.top_left_GUI = (0, 0)
        self.bottom_right_GUI = (500, 350)

        self.start_game_time_seconds = 0
        self.max_game_time_secs = max_game_time_mins * 60

    def runGUI(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        self.screen.fill((255, 255, 255))

        # Draw field
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            pygame.Rect(
                self.top_left_GUI[0],
                self.top_left_GUI[1],
                self.bottom_right_GUI[0],
                self.bottom_right_GUI[1],
            ),
        )

        # Draw Ball
        circle_pos = (
            self.map_range(
                self.ball_pos[0],
                -5,
                5,
                self.top_left_GUI[0],
                self.bottom_right_GUI[0],
            )
            + PADDING,
            self.map_range(
                self.ball_pos[1],
                -3.5,
                3.5,
                self.top_left_GUI[1],
                self.bottom_right_GUI[1],
            )
            + PADDING,
        )
        pygame.draw.circle(self.screen, (0, 0, 255), circle_pos, 10)

        # create a text surface object,
        # on which text is drawn on it.
        text = self.font.render(self.time_passed_text, True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.topleft = (10, 10)
        self.screen.blit(text, textRect)

        # Flip the display
        pygame.display.flip()

    def reset_timer(self):
        print("Starting time")
        self.start_game_time_seconds = time.time()

    def reset_simulation(self):
        ball = self.getFromDef("BALL")
        ball_position = ball.getField("translation")
        ball_position.setSFVec3f([0, 0, 1])
        red1 = self.getFromDef("red_1")
        red1_position = red1.getField("translation")
        red1_position.setSFVec3f([-4, 0, 0.4])
        red2 = self.getFromDef("red_2")
        red2_position = red2.getField("translation")
        red2_position.setSFVec3f([-2.5, 0, 0.4])
        red3 = self.getFromDef("red_3")
        red3_position = red3.getField("translation")
        red3_position.setSFVec3f([-1, 0.5, 0.4])
        red4 = self.getFromDef("red_4")
        red4_position = red4.getField("translation")
        red4_position.setSFVec3f([-1, -0.5, 0.4])
        blue1 = self.getFromDef("blue_1")
        blue1_position = blue1.getField("translation")
        blue1_position.setSFVec3f([4, 0, 0.4])
        blue2 = self.getFromDef("blue_2")
        blue2_position = blue2.getField("translation")
        blue2_position.setSFVec3f([2.5, 0, 0.4])
        blue3 = self.getFromDef("blue_3")
        blue3_position = blue3.getField("translation")
        blue3_position.setSFVec3f([1, -0.5, 0.4])
        blue4 = self.getFromDef("blue_4")
        blue4_position = blue4.getField("translation")
        blue4_position.setSFVec3f([1, 0.5, 0.4])

    def spawn_players(self):
        self.players = [Player(self, **player) for player in player_definitions]

    def spawn_ball(self):
        print("Spawning the ball at field center")
        root_node = self.getRoot()
        children_field = root_node.getField("children")
        children_field.importMFNodeFromString(
            -1, "DEF BALL RobocupSoccerBall { translation 0 0 1 }"
        )
        self.ball_node = self.getFromDef("BALL")

    def goal_check(self):
        if self.ball_pos[0] < -4.55 and self.ball_pos[1] < 0.7:
            return "blue"
        elif self.ball_pos[0] > 4.55 and self.ball_pos[1] < 0.7:
            return "red"

    def get_ball_pos(self):
        ball_position = self.ball_node.getField("translation")
        self.ball_pos = (ball_position.getSFVec3f()[0], ball_position.getSFVec3f()[1])

    def ball_out(self):
        return abs(self.ball_pos[1]) > 3 or abs(self.ball_pos[0]) > 4.5

    def get_time(self):
        self.time_passed = time.time() - self.start_game_time_seconds
        self.time_passed_text = time.strftime("%M:%S", time.gmtime(self.time_passed))

    def time_up(self):
        time_passed = time.time() - self.start_game_time_seconds

        # print(f"Game Time: {time.strftime('%M:%S',time.gmtime(time_passed))}")
        # print(f"Checking if time up")

        return time_passed > self.max_game_time_secs

    def end_simulation(self):
        print("Sim ended")

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


player_definitions = [
    {
        "player": "1",
        "team": "red",
        "position": "goalie",
        "translation": "-4 0 0.4",
    },
    {
        "player": "2",
        "team": "red",
        "position": "defender",
        "translation": "-2.5 0 0.4",
    },
    {
        "player": "3",
        "team": "red",
        "position": "attacker_left",
        "translation": "-1 0.5 0.4",
    },
    {
        "player": "4",
        "team": "red",
        "position": "attacker_right",
        "translation": "-1 -0.5 0.4",
    },
    {
        "player": "1",
        "team": "blue",
        "position": "goalie",
        "translation": "4 0 0.4",
    },
    {
        "player": "2",
        "team": "blue",
        "position": "defender",
        "translation": "2.5 0 0.4",
    },
    {
        "player": "3",
        "team": "blue",
        "position": "attacker_left",
        "translation": "1 -0.5 0.4",
    },
    {
        "player": "4",
        "team": "blue",
        "position": "attacker_right",
        "translation": "1 0.5 0.4",
    },
]
