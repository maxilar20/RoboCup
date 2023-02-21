from .Entity import Entity
from pygame.math import Vector2 as vec2
import math as mt
import numpy as np
from scipy.spatial.transform import Rotation as R


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

        self.getPosition()

    def act(self, move_vector, rot):
        message = [-move_vector[1], move_vector[0], rot, 0]

        self.emitter.setChannel(self.channel)
        self.emitter.send(message)

    def hasFallen(self):
        orientation = self.getGyro()
        angles = R.from_rotvec(orientation[3] * np.array(orientation[:3]))
        yaw = angles.as_euler("zxy", degrees=True)[2]
        return yaw > 70 or yaw < -70
