from Objects.Entity import *
import pygame
import math as mt


class Player(Entity):
    def __init__(
        self,
        robot,
        player,
        team,
        player_position,
        translation,
        channel,
        GUI,
        emitter,
        ball,
    ):

        self.GUI = GUI
        self.emitter = emitter
        self.ball = ball

        # Player Attributes
        self.team = team
        self.player_position = player_position
        self.channel = channel

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

        self.max_sensor_dist = 1
        self.sensor_angles = np.linspace(0, 2 * 3.14, 40)[:-1]
        self.possible_distances = np.linspace(0, self.max_sensor_dist, 10)
        self.distances = np.zeros(self.sensor_angles.size)

        self.vec = math.Vector2(0)

    def act(self):

        flee = self.flee().clamp_magnitude(1)
        pursue = self.pursue(self.ball.getPosition()).normalize()

        self.vec = math.Vector2(0.0001)
        self.vec += flee
        self.vec += pursue

        self.vec = self.vec.normalize()

        if (self.vec.as_polar()[1]) > 10:
            rot = -0.5
        elif (self.vec.as_polar()[1]) < -10:
            rot = 0.5
        else:
            rot = 0

        message = [-self.vec[1], self.vec[0], rot]

        self.emitter.setChannel(self.channel)
        self.emitter.send(message)

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
            return self.max_sensor_dist

    def flee(self):
        dir_vector = math.Vector2(0.001)
        for angle, dist in zip(self.sensor_angles, self.distances):
            dir = math.Vector2((np.cos(angle + 0.2), np.sin(angle + 0.2)))
            dir_vector += dist * dir

        return dir_vector

    def pursue(self, pos):
        difference = pos - self.position
        angle = self.getOrientation()

        ang = angle - mt.radians(difference.as_polar()[1])

        return math.Vector2((np.cos(ang), -np.sin(ang)))

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
        # for angle, distance in zip(self.sensor_angles, self.distances):
        #     sensor_dir = angle + orientation
        #     dir_vector = np.array((np.cos(sensor_dir), np.sin(sensor_dir)))
        #     pygame.draw.lines(
        #         self.GUI.screen,
        #         (255, 255, 255),
        #         True,
        #         [
        #             self.GUI.mapToGUI(self.position),
        #             self.GUI.mapToGUI(self.position + distance * dir_vector),
        #         ],
        #         1,
        #     )

        dir_vector = self.vec.rotate_rad(orientation)
        pygame.draw.lines(
            self.GUI.screen,
            (255, 0, 0),
            True,
            [
                self.GUI.mapToGUI(self.position),
                self.GUI.mapToGUI(self.position + dir_vector),
            ],
            1,
        )
