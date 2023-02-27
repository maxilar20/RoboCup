import pygame
from pygame import math
import numpy as np
import ctypes
from ctypes import wintypes


class GUI:
    def __init__(self, window_size=(334, 230)):

        pygame.init()

        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        pygame.display.set_caption("Robocup")
        icon = pygame.image.load("Objects/icon.png")
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

        self.font = pygame.font.Font("freesansbold.ttf", 20)

        self.message_flag = False

    def show(self, debug, time_passed, scores, field, ball, players, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                w = int(event.w)
                h = int(w * 0.68)
                self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                self.window_size = (w, h)

        self.screen.fill((0, 120, 0))

        self.showField(field)
        self.showBall(ball)
        for player in players:
            self.showPlayer(player)
            if debug:
                self.showSensors(player)
        for button in buttons:
            self.showButton(button)

        self.drawText(time_passed, scores)

        self.display_message()

    def start_display(self, message, time_s=3):
        self.scored_time = pygame.time.get_ticks()
        self.msg_time = time_s * 1000
        self.message_flag = True
        self.message = message
        print(message)

    def display_message(self):
        if self.message_flag:
            if pygame.time.get_ticks() - self.scored_time < self.msg_time:
                scored_text = self.font.render(self.message, True, (0, 0, 0))

                scored_rect = scored_text.get_rect(center=(self.window_size[0] / 2, 50))
                scored_background = pygame.Surface(
                    (scored_rect.width + 20, scored_rect.height + 20)
                )
                scored_background.fill((255, 255, 255))
                scored_background.blit(scored_text, (10, 10))
                scored_rect = scored_background.get_rect(
                    center=(self.window_size[0] / 2, 30)
                )
                self.screen.blit(scored_background, scored_rect)
            else:
                self.message_flag = False

    def flip(self):
        pygame.display.flip()

    def showButton(self, button):
        button.fg, button.bg = button.colors.split(" on ")
        pygame.draw.line(
            self.screen,
            (150, 150, 150),
            (button.x, button.y),
            (button.x + button.w, button.y),
            5,
        )
        pygame.draw.line(
            self.screen,
            (150, 150, 150),
            (button.x, button.y - 2),
            (button.x, button.y + button.h),
            5,
        )
        pygame.draw.line(
            self.screen,
            (50, 50, 50),
            (button.x, button.y + button.h),
            (button.x + button.w, button.y + button.h),
            5,
        )
        pygame.draw.line(
            self.screen,
            (50, 50, 50),
            (button.x + button.w, button.y + button.h),
            [button.x + button.w, button.y],
            5,
        )
        pygame.draw.rect(
            self.screen, button.bg, (button.x, button.y, button.w, button.h)
        )
        self.screen.blit(button.text_render, button.position)

    def drawText(self, time_passed, scores):
        score_text = f"Red {scores[0]} | {scores[1]} Blue      "
        text = self.font.render(score_text + time_passed, True, (0, 0, 0))
        text_padding = 5
        background_size = (
            text.get_width() + text_padding * 2,
            text.get_height() + text_padding * 2,
        )
        background = pygame.Surface(background_size)
        background.fill((255, 255, 255))
        text_rect = text.get_rect(center=background.get_rect().center)
        # text_rect.move_ip(text_padding, text_padding)
        background.blit(text, text_rect)
        background_rect = background.get_rect(
            midbottom=(self.window_size[0] / 2, self.window_size[1])
        )
        self.screen.blit(background, background_rect)

        # text = self.font.render(
        #     score_text + time_passed, True, (0, 0, 0), (255, 255, 255)
        # )
        # textRect = text.get_rect()
        # textRect.midbottom = (self.window_size[0] / 2, self.window_size[1])
        # self.screen.blit(text, textRect)

    def showBall(self, ball):
        color = (255, 255, 255)
        pygame.draw.circle(
            self.screen,
            color,
            self.mapToGUI(ball.getPosition()),
            self.scaleToGUI(ball.circle_radius),
        )

    def showField(self, field):
        for boundary in field.boundaries.values():
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

    def showPlayer(self, player):
        pygame.draw.circle(
            self.screen,
            player.color,
            self.mapToGUI(player.getPosition()),
            self.scaleToGUI(player.circle_radius),
        )
        pygame.draw.circle(
            self.screen,
            (0, 255, 0),
            self.mapToGUI(
                player.getPosition()
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
                player.getPosition()
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

    def showSensors(self, player):
        orientation = player.getOrientation()
        for angle, distance in zip(player.sensor_angles, player.distances):
            sensor_dir = angle + orientation
            dir_vector = np.array((np.cos(sensor_dir), np.sin(sensor_dir)))
            pygame.draw.lines(
                self.screen,
                (255, 255, 255),
                True,
                [
                    self.mapToGUI(player.getPosition()),
                    self.mapToGUI(player.getPosition() + distance * dir_vector),
                ],
                1,
            )

        dir_vector = player.move_vector.rotate_rad(orientation)
        pygame.draw.lines(
            self.screen,
            (255, 0, 0),
            True,
            [
                self.mapToGUI(player.getPosition()),
                self.mapToGUI(player.getPosition() + dir_vector),
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
