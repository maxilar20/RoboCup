import pygame


class Field:
    def __init__(self, boundaries):
        self.boundaries = boundaries

    def getCenterPosition(self, field="field"):
        return (self.boundaries[field][0] + self.boundaries[field][1]) / 2

    def isInside(self, pos, field="field"):
        boundary = self.boundaries[field]
        return (
            pos.x > boundary[0].x
            and pos.x < boundary[1].x
            and pos.y < boundary[0].y
            and pos.y > boundary[1].y
        )

    def show(self, GUI):
        for boundary in self.boundaries.values():
            # Field lines
            pygame.draw.rect(
                GUI.screen,
                (255, 255, 255),
                pygame.Rect(
                    GUI.mapToGUI(boundary[0]),
                    GUI.mapToGUI(boundary[1]) - GUI.mapToGUI(boundary[0]),
                ),
                2,
            )

        # Field circle line
        pygame.draw.circle(
            GUI.screen,
            (255, 255, 255),
            GUI.mapToGUI((0, 0)),
            GUI.scaleToGUI(0.85),
            2,
        )

    def debug(self, GUI):
        return
