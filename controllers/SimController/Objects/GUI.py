import pygame
from pygame import math
import numpy as np
import ctypes
from ctypes import wintypes
import time


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

        self.messages = []
        self.time_passed = 0

    def show(self, debug, time_passed, scores, entities):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                w = int(event.w)
                h = int(w * 0.68)
                self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                self.window_size = (w, h)

        self.screen.fill((0, 120, 0))

        for entity in entities:
            entity.show(self)
            if debug:
                entity.debug(self)

        self.time_passed = time_passed
        time_passed_text = time.strftime("%M:%S", time.gmtime(time_passed))
        self.drawText(time_passed_text, scores)

        self.display_message()

        pygame.display.flip()
        return pygame.surfarray.array3d(self.screen)

    def start_display(self, message, time_s=3):
        self.messages.append((message, self.time_passed + time_s))
        print(message)

    def display_winner(self, team):
        self.start_display(f"{team} has won!")

    def display_message(self):
        for idx, message in enumerate(self.messages):
            scored_text = self.font.render(message[0], True, (0, 0, 0))

            scored_rect = scored_text.get_rect(center=(self.window_size[0] / 2, 50))
            scored_background = pygame.Surface(
                (scored_rect.width + 10, scored_rect.height + 10)
            )
            scored_background.fill((255, 255, 255))
            scored_background.blit(scored_text, (10, 10))
            scored_rect = scored_background.get_rect(
                center=(self.window_size[0] / 2, (idx+1) * 30)
            )
            self.screen.blit(scored_background, scored_rect)

            if self.time_passed > message[1]:
                self.messages.pop(idx)

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
        background.blit(text, text_rect)
        background_rect = background.get_rect(
            midbottom=(self.window_size[0] / 2, self.window_size[1])
        )
        self.screen.blit(background, background_rect)

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
