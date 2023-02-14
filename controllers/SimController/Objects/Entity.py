from pygame import math
import numpy as np


class Entity:
    def __init__(
        self, robot, name, DEF, translation, rotation, custom_args="", circle_radius=0.1
    ):
        self.name = name
        self.translation = translation
        self.rotation = rotation
        self.circle_radius = circle_radius
        self.circle_radius_sq = circle_radius**2

        root_node = robot.getRoot()
        children_field = root_node.getField("children")

        spawn_field = f"DEF {name} {DEF} {{translation {translation} rotation {rotation} {custom_args}}}"
        children_field.importMFNodeFromString(-1, spawn_field)

        self.node = robot.getFromDef(f"{name}")
        self.position_field = self.node.getField("translation")
        self.orientation_field = self.node.getField("rotation")

    def getPosition(self):
        self.position = math.Vector2(self.position_field.getSFVec3f()[:2])
        return self.position

    def getOrientation(self):
        if self.orientation_field.getSFVec3f()[2] > 0:
            return self.orientation_field.getSFVec3f()[3]
        else:
            return (2 * 3.1415) - self.orientation_field.getSFVec3f()[3]

    def isInside(self, point):
        return point.distance_squared_to(self.position) < self.circle_radius_sq

    def reset(self):
        self.position_field.setSFVec3f([float(i) for i in self.translation.split()])


class Player(Entity):
    def __init__(self, robot, player, team, player_position, translation, channel):

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
        self.possible_distances = np.linspace(0, 3, int(3 / (2 * self.circle_radius)))
        self.distances = np.zeros(self.sensor_angles.size)

    def senseDistances(self, players):
        orientation = self.getOrientation()
        for idx, angle in enumerate(self.sensor_angles):
            sensor_dir = angle + orientation
            dir = np.array((np.cos(sensor_dir), np.sin(sensor_dir)))
            self.distances[idx] = self.sense(players, dir)

    def sense(self, players, dir):
        for dist in self.possible_distances:
            point = self.position + (dist * dir)
            for player in players:
                if player != self and player.isInside(point):
                    return dist
        else:
            return 3


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
