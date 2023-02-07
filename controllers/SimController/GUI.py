import pygame
import numpy as np


class GUI:
    def __init__(self, window_size=(500, 350)):
        pygame.init()

        self.screen = pygame.display.set_mode(window_size)
        self.font = pygame.font.Font("freesansbold.ttf", 15)

    def runGUI(self, ball, players, upper_text, boundaries):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill((0, 120, 0))

        self.drawField(boundaries)
        self.drawBall(ball.getPosition())
        self.drawText(upper_text)
        self.drawPlayers(players)

        # Flip the display
        pygame.display.flip()

    def drawText(self, upper_text):
        text = self.font.render(
            upper_text,
            True,
            (255, 255, 255),
        )
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
                    self.mapToGUI((boundary[0], boundary[1])),
                    np.array(self.mapToGUI((boundary[2], boundary[3])))
                    - np.array(self.mapToGUI((boundary[0], boundary[1]))),
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

    def drawBall(self, ball_pos, color=(255, 255, 255), size=5):
        pygame.draw.circle(self.screen, color, self.mapToGUI(ball_pos), size)

    def drawPlayers(self, players):
        for player in players:
            if player.team == "red":
                color = (255, 0, 0)
            elif player.team == "blue":
                color = (0, 0, 255)

            self.drawBall(player.getPosition(), color=color, size=10)
            self.drawBall(
                np.array(player.getPosition())
                + np.array(
                    (
                        0.1 * np.cos(player.getOrientation() + 1),
                        0.1 * np.sin(player.getOrientation() + 1),
                    )
                ),
                color=(0, 255, 0),
                size=3,
            )
            self.drawBall(
                np.array(player.getPosition())
                + np.array(
                    (
                        0.1 * np.cos(player.getOrientation() - 1),
                        0.1 * np.sin(player.getOrientation() - 1),
                    )
                ),
                color=(0, 255, 0),
                size=3,
            )

    def mapToGUI(self, pos):
        return (
            self.map_range(
                pos[0],
                -5,
                5,
                0,
                500,
            ),
            self.map_range(
                pos[1],
                -3.5,
                3.5,
                0,
                350,
            ),
        )

    def scaleToGUI(self, pos):
        return self.map_range(pos, 0, 5, 0, 255)

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
