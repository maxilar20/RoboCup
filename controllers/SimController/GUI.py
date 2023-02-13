import pygame
from pygame import math
import numpy as np
import ctypes
from ctypes import wintypes


class GUI:
    def __init__(self, window_size=math.Vector2((334, 230))):

        pygame.init()

        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Robocup")
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)

        hwnd = pygame.display.get_wm_info()["window"]

        user32 = ctypes.WinDLL("user32")
        user32.SetWindowPos.restype = wintypes.HWND
        user32.SetWindowPos.argtypes = [
            wintypes.HWND,
            wintypes.HWND,
            wintypes.INT,
            wintypes.INT,
            wintypes.INT,
            wintypes.INT,
            wintypes.UINT,
        ]
        user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)

        self.font = pygame.font.Font("freesansbold.ttf", 15)

    def runGUI(self, ball, players, upper_text, boundaries):
        self.screen.fill((0, 120, 0))

        self.drawField(boundaries)
        self.drawBall(ball)
        self.drawText(upper_text)
        self.drawPlayers(players)
        self.drawDistances(players)

        # Flip the display
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def drawText(self, upper_text):
        text = self.font.render(upper_text, True, (255, 255, 255), (10, 10, 10))
        textRect = text.get_rect()
        textRect.topleft = (30, 10)
        self.screen.blit(text, textRect)

    def drawField(self, boundaries):
        for boundary in boundaries.values():
            # Field lines
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                pygame.Rect(
                    self.mapToGUI(boundary[0]),
                    self.mapToGUI(boundary[1]) - self.mapToGUI(boundary[0]),
                ),
                2,
            )

        # Middle line
        pygame.draw.lines(
            self.screen,
            (255, 255, 255),
            True,
            [
                self.mapToGUI((0, -3)),
                self.mapToGUI((0, 3)),
            ],
            2,
        )

        # Field circle line
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            self.mapToGUI((0, 0)),
            self.scaleToGUI(0.85),
            2,
        )

    def drawBall(self, ball_obj, color=(255, 255, 255)):
        pygame.draw.circle(
            self.screen,
            color,
            self.mapToGUI(ball_obj.getPosition()),
            self.scaleToGUI(ball_obj.circle_radius),
        )

    def drawPlayers(self, players):
        for player in players:
            if player.team == "red":
                color = (255, 0, 0)
            elif player.team == "blue":
                color = (0, 0, 255)

            pygame.draw.circle(
                self.screen,
                color,
                self.mapToGUI(player.position),
                self.scaleToGUI(player.circle_radius),
            )
            pygame.draw.circle(
                self.screen,
                (0, 255, 0),
                self.mapToGUI(
                    player.position
                    + 0.9
                    * np.array(
                        (
                            player.circle_radius * np.cos(player.getOrientation() + 1),
                            player.circle_radius * np.sin(player.getOrientation() + 1),
                        )
                    ),
                ),
                self.scaleToGUI(player.circle_radius) * 0.5,
            )
            pygame.draw.circle(
                self.screen,
                (0, 255, 0),
                self.mapToGUI(
                    player.position
                    + 0.9
                    * np.array(
                        (
                            player.circle_radius * np.cos(player.getOrientation() - 1),
                            player.circle_radius * np.sin(player.getOrientation() - 1),
                        )
                    ),
                ),
                self.scaleToGUI(player.circle_radius) * 0.5,
            )

    def drawDistances(self, players):
        for player in players:
            orientation = player.getOrientation()
            for angle, distance in zip(player.sensor_angles, player.distances):
                sensor_dir = angle + orientation
                dir_vector = np.array((np.cos(sensor_dir), np.sin(sensor_dir)))
                pygame.draw.lines(
                    self.screen,
                    (255, 255, 255),
                    True,
                    [
                        self.mapToGUI(player.position),
                        self.mapToGUI(player.position + distance * dir_vector),
                    ],
                    1,
                )

    def mapToGUI(self, pos):
        return math.Vector2(
            self.map_range(
                pos[0],
                -5,
                5,
                0,
                self.window_size[0],
            ),
            self.map_range(
                pos[1],
                3.5,
                -3.5,
                0,
                self.window_size[1],
            ),
        )

    def scaleToGUI(self, pos):
        return self.map_range(pos, 0, 5, 0, self.window_size[0] / 2)

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
