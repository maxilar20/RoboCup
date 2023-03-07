from .Entity import Entity
import pygame


class Ball(Entity):
    def __init__(self, robot):
        super().__init__(
            robot,
            "ball",
            "RobocupSoccerBall",
            "0 0 0",
            "0 0 0 0",
            circle_radius=0.1,
        )

    def show(self, GUI):
        color = (255, 255, 255)
        pygame.draw.circle(
            GUI.screen,
            color,
            GUI.mapToGUI(self.position),
            GUI.scaleToGUI(self.circle_radius),
        )

    def debug(self, GUI):
        return
