import pygame
from pygame import math
import numpy as np
import ctypes
from ctypes import wintypes


class GUI:
    def __init__(self, window_size=(334, 230)):

        pygame.init()

        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)
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

    def run(self):
        self.screen.fill((0, 120, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def flip(self):
        # Flip the display
        pygame.display.flip()

    def drawText(self, time_passed, red_score, blue_score):
        score_text = f"Red {red_score} | {blue_score} Blue      "
        text = self.font.render(
            score_text + time_passed, True, (0, 0, 0), (255, 255, 255)
        )
        textRect = text.get_rect()
        textRect.midbottom = (self.window_size[0] / 2, self.window_size[1])
        self.screen.blit(text, textRect)

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
