import pygame


class Field:
    def __init__(self, boundaries, GUI):
        self.boundaries = boundaries
        self.GUI = GUI

    def show(self):
        for boundary in self.boundaries.values():
            # Field lines
            pygame.draw.rect(
                self.GUI.screen,
                (255, 255, 255),
                pygame.Rect(
                    self.GUI.mapToGUI(boundary[0]),
                    self.GUI.mapToGUI(boundary[1]) - self.GUI.mapToGUI(boundary[0]),
                ),
                2,
            )

        # Middle line
        pygame.draw.lines(
            self.GUI.screen,
            (255, 255, 255),
            True,
            [
                self.GUI.mapToGUI((0, -3)),
                self.GUI.mapToGUI((0, 3)),
            ],
            2,
        )

        # Field circle line
        pygame.draw.circle(
            self.GUI.screen,
            (255, 255, 255),
            self.GUI.mapToGUI((0, 0)),
            self.GUI.scaleToGUI(0.85),
            2,
        )

    def isInside(self, pos, field="field"):
        boundary = self.boundaries[field]
        return (
            pos.x > boundary[0].x
            and pos.x < boundary[1].x
            and pos.y < boundary[0].y
            and pos.y > boundary[1].y
        )
