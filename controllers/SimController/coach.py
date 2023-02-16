from pygame import math
import math as mt
import numpy as np
import pygame


class Coach:
    def __init__(self, own_players, enemy_players, field, ball):
        self.own_players = own_players
        self.enemy_players = enemy_players
        self.all_players = self.own_players + self.enemy_players
        self.field = field
        self.ball = ball

    def act(self, GUI):
        for player in self.own_players:
            if player.player_position == "attacker_right":
                avoid_vector = self.avoid(player, self.all_players)
                pursue_vector = self.pursue(player, self.ball.getPosition())
                mov_vector = avoid_vector + pursue_vector
                look_vector = mov_vector
            else:
                avoid_vector = self.avoid(player, self.all_players)
                mov_vector = avoid_vector
                look_vector = self.pursue(player, self.ball.getPosition())

            self.show(GUI, player, mov_vector)

            # Send
            mov_vector = mov_vector.clamp_magnitude(1)
            mov_vector_rotated = self.transformToPlayer(player, mov_vector)

            look_vector_rotated = self.transformToPlayer(player, look_vector)
            rot = np.interp(look_vector_rotated.as_polar()[1], [-180, 180], [2, -2])
            rot = max(min(rot, 1), -1)

            player.act(mov_vector_rotated, rot)

    def avoid(self, own, others):
        avoid_vector = math.Vector2(0.001)

        for other in others:
            if own.name != other.name:
                dif_vector = own.getPosition() - other.getPosition()
                dif_vector = dif_vector.clamp_magnitude(1)
                dif_vector.scale_to_length(1 - dif_vector.magnitude())
                avoid_vector += dif_vector
        return avoid_vector

    def pursue(self, own, goal_position):
        pursue_vector = goal_position - own.getPosition()
        pursue_vector = pursue_vector.normalize()
        return pursue_vector

    def transformToPlayer(self, player, vector):
        angle = mt.radians(vector.as_polar()[1]) - player.getOrientation()
        return vector.magnitude() * math.Vector2(mt.cos(angle), mt.sin(angle))

    def show(self, GUI, player, goal):
        pygame.draw.line(
            GUI.screen,
            (0, 255, 0),
            GUI.mapToGUI(player.getPosition()),
            GUI.mapToGUI(player.getPosition() + goal),
            1,
        )
