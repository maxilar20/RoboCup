from .entity import Entity
from pygame import math
import math as mt
import numpy as np


class Player(Entity):
    def __init__(
        self, robot, player, team, player_position, translation, channel, emitter
    ):
        self.emitter = emitter

        # Player Attributes
        self.team = team
        self.player_position = player_position
        self.channel = channel

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
            translation,
            rotation,
            custom_args,
            circle_radius=0.15,
        )

        self.max_sensor_dist = 1
        self.sensor_angles = np.linspace(0, 2 * 3.14, 40)[:-1]
        self.possible_distances = np.linspace(0, self.max_sensor_dist, 10)
        self.distances = np.zeros(self.sensor_angles.size)

        self.move_vector = math.Vector2(0)

    def act(self, move_vector, rot):

        message = [-move_vector[1], move_vector[0], rot, 0]

        self.emitter.setChannel(self.channel)
        self.emitter.send(message)
