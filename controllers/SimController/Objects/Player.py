from .Entity import Entity
from pygame.math import Vector2 as vec2
import math as mt
import numpy as np
from scipy.spatial.transform import Rotation as R
import pygame


class Player(Entity):
    def __init__(
        self,
        robot,
        player,
        team,
        player_position,
        kickoff_pos,
        penalty_pos,
        channel,
        emitter,
    ):
        self.emitter = emitter

        # Player Attributes
        self.team = team
        self.player_position = player_position
        self.channel = channel
        self.penalty_pos = penalty_pos

        # Node Spawning
        if team == "red":
            self.color = (255, 0, 0)
            spawn_color = [1, 0, 0]
            rotation = "0 0 1 0"
        else:
            self.color = (0, 0, 255)
            spawn_color = [0, 0, 1]
            rotation = "0 0 1 3.1415"

        custom_args = f"customColor {spawn_color} channel {channel}"

        super().__init__(
            robot,
            f"{team}_{player}",
            "Nao",
            kickoff_pos,
            rotation,
            custom_args,
            circle_radius=0.15,
        )

        self.move_vector = vec2(0.001)
        self.look_vector = vec2(0.001)

    def act(self):
        move_vector = self.move_vector
        move_vector = move_vector.clamp_magnitude(1)
        move_vector_rotated = self.transformToPlayer(self, move_vector)

        look_vector = self.look_vector
        look_vector_rotated = self.transformToPlayer(self, look_vector)

        rot = np.interp(look_vector_rotated.as_polar()[1], [-180, 180], [2, -2])
        rot = max(min(rot, 1), -1)

        self.sendCommand(move_vector_rotated, rot)

    def kick(self):
        self.emitter.setChannel(self.channel)
        self.emitter.send([0.0, 0.0, 0.0, 1.0])

    def sendCommand(self, move_vector, rot):
        message = [-move_vector[1], move_vector[0], rot, 0]
        self.emitter.setChannel(self.channel)
        self.emitter.send(message)

    def hasFallen(self):
        orientation = self.getGyro()
        angles = R.from_rotvec(orientation[3] * np.array(orientation[:3]))
        yaw = angles.as_euler("zxy", degrees=True)[2]
        return yaw > 70 or yaw < -70

    def moveTo(self, goal, entities_avoid, entity_look, lines, line_vectors):
        avoid_vector = self.avoidEntity(entities_avoid, dist=1)
        avoid_out = self.avoidField(lines, line_vectors, 0.5)
        goto_vector = self.pursue(goal)
        move_vector = avoid_vector + goto_vector + (5 * avoid_out)
        if (goal - self.position).magnitude() < 0.5:
            look_vector = entity_look.position - self.position
        else:
            look_vector = move_vector

        return move_vector, look_vector

    def avoidEntity(self, others, dist=1):
        avoid_vector = vec2(0.001)
        for other in others:
            if self.name != other.name:
                dif_vector = self.position - other.position
                dif_vector = dif_vector.clamp_magnitude(dist)
                dif_vector.scale_to_length(dist - dif_vector.magnitude())
                avoid_vector += dif_vector
        return avoid_vector

    def avoidField(self, lines, line_vectors, dist):
        avoid_vector = vec2(0.001)
        for line, vector in zip(lines, line_vectors):
            dif_vector = vector * lineseg_dist(self.position, line[0], line[1])
            dif_vector = dif_vector.clamp_magnitude(dist)
            dif_vector.scale_to_length(dist - dif_vector.magnitude())
            avoid_vector += dif_vector
        return avoid_vector

    def pursue(self, goal_position):
        pursue_vector = goal_position - self.position
        pursue_vector = pursue_vector.normalize()
        return pursue_vector

    def transformToPlayer(self, player, vector):
        angle = mt.radians(vector.as_polar()[1]) - player.orientation
        return vector.magnitude() * vec2(mt.cos(angle), mt.sin(angle))

    def show(self, GUI):
        pygame.draw.circle(
            GUI.screen,
            self.color,
            GUI.mapToGUI(self.position),
            GUI.scaleToGUI(self.circle_radius),
        )
        pygame.draw.circle(
            GUI.screen,
            (0, 255, 0),
            GUI.mapToGUI(
                self.position
                + 0.9
                * np.array(
                    (
                        self.circle_radius * np.cos(self.orientation + 1),
                        self.circle_radius * np.sin(self.orientation + 1),
                    )
                ),
            ),
            GUI.scaleToGUI(self.circle_radius) * 0.5,
        )
        pygame.draw.circle(
            GUI.screen,
            (0, 255, 0),
            GUI.mapToGUI(
                self.position
                + 0.9
                * np.array(
                    (
                        self.circle_radius * np.cos(self.orientation - 1),
                        self.circle_radius * np.sin(self.orientation - 1),
                    )
                ),
            ),
            GUI.scaleToGUI(self.circle_radius) * 0.5,
        )

    def debug(self, GUI):
        pygame.draw.line(
            GUI.screen,
            [255, 0, 0],
            GUI.mapToGUI(self.position),
            GUI.mapToGUI(self.position + self.move_vector),
            1,
        )
        pygame.draw.line(
            GUI.screen,
            [0, 255, 0],
            GUI.mapToGUI(self.position),
            GUI.mapToGUI(self.position + self.look_vector.normalize()),
            1,
        )


def lineseg_dist(p, a, b):
    d = np.divide(b - a, np.linalg.norm(b - a))
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)
    h = np.maximum.reduce([s, t, 0])
    c = np.cross(p - a, d)
    return np.hypot(h, np.linalg.norm(c))
