from Objects.Entity import *
import pygame


class Ball(Entity):
    def __init__(self, robot, GUI):
        self.GUI = GUI

        super().__init__(
            robot,
            "ball",
            "RobocupSoccerBall",
            "0 0 0",
            "0 0 0 0",
            circle_radius=0.1,
        )

    def show(self):
        color = (255, 255, 255)
        pygame.draw.circle(
            self.GUI.screen,
            color,
            self.GUI.mapToGUI(self.getPosition()),
            self.GUI.scaleToGUI(self.circle_radius),
        )
