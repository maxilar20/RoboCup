from Objects.Entity import *
import pygame


class Player(Entity):
    def __init__(self, robot, player, team, player_position, translation, channel, GUI):

        self.GUI = GUI

        # Player Attributes
        self.team = team
        self.player_position = player_position

        # Node Spawning
        if team == "red":
            color = [1, 0, 0]
            rotation = "0 0 1 0"
        else:
            color = [0, 0, 1]
            rotation = "0 0 1 3.1415"

        custom_args = f"customColor {color} channel {channel}"

        super().__init__(
            robot,
            f"{team}_{player}",
            "Nao",
            translation,
            rotation,
            custom_args,
            circle_radius=0.15,
        )

        self.sensor_angles = np.linspace(0, 2 * 3.14, 20)[:-1]
        self.possible_distances = np.linspace(0, 3, 10)
        self.distances = np.zeros(self.sensor_angles.size)

    def senseDistances(self, field, players):
        orientation = self.getOrientation()
        for idx, angle in enumerate(self.sensor_angles):
            sensor_dir = angle + orientation
            dir = np.array((np.cos(sensor_dir), np.sin(sensor_dir)))
            self.distances[idx] = self.sense(field, players, dir)

    def sense(self, field, players, dir):
        for dist in self.possible_distances:
            point = self.position + (dist * dir)
            if not field.isInside(point):
                return dist
            for player in players:
                if player != self and player.isInside(point):
                    return dist
        else:
            return 3

    def showPlayer(self):
        if self.team == "red":
            color = (255, 0, 0)
        elif self.team == "blue":
            color = (0, 0, 255)

        pygame.draw.circle(
            self.GUI.screen,
            color,
            self.GUI.mapToGUI(self.position),
            self.GUI.scaleToGUI(self.circle_radius),
        )
        pygame.draw.circle(
            self.GUI.screen,
            (0, 255, 0),
            self.GUI.mapToGUI(
                self.position
                + 0.9
                * np.array(
                    (
                        self.circle_radius * np.cos(self.getOrientation() + 1),
                        self.circle_radius * np.sin(self.getOrientation() + 1),
                    )
                ),
            ),
            self.GUI.scaleToGUI(self.circle_radius) * 0.5,
        )
        pygame.draw.circle(
            self.GUI.screen,
            (0, 255, 0),
            self.GUI.mapToGUI(
                self.position
                + 0.9
                * np.array(
                    (
                        self.circle_radius * np.cos(self.getOrientation() - 1),
                        self.circle_radius * np.sin(self.getOrientation() - 1),
                    )
                ),
            ),
            self.GUI.scaleToGUI(self.circle_radius) * 0.5,
        )

    def showSensors(self):
        orientation = self.getOrientation()
        for angle, distance in zip(self.sensor_angles, self.distances):
            sensor_dir = angle + orientation
            dir_vector = np.array((np.cos(sensor_dir), np.sin(sensor_dir)))
            pygame.draw.lines(
                self.GUI.screen,
                (255, 255, 255),
                True,
                [
                    self.GUI.mapToGUI(self.position),
                    self.GUI.mapToGUI(self.position + distance * dir_vector),
                ],
                1,
            )
