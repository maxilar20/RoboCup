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

        goal_name = "goal_blue" if self.own_players[0].team == "red" else "goal_red"
        ball_mov_vector = self.ballPlan(GUI, goal_name)
        dribbling_pos = ball_mov_vector.normalize() * -0.3
        self.show(GUI, self.ball, ball_mov_vector)
        self.show(GUI, self.ball, dribbling_pos, color=[255, 0, 0])

        for player in self.own_players:
            if player.player_position == "attacker_right":

                goal_pos = dribbling_pos + self.ball.getPosition()

                if (goal_pos - player.getPosition()).magnitude() > 0.15:
                    avoid_vector = self.avoid(player, self.all_players, 1)
                    pursue_vector = self.pursue(player, goal_pos)
                    mov_vector = avoid_vector + pursue_vector
                    look_vector = mov_vector
                else:
                    pursue_vector = self.pursue(
                        player, ball_mov_vector + self.ball.getPosition()
                    )
                    mov_vector = pursue_vector
                    look_vector = self.pursue(player, self.ball.getPosition())
            else:
                avoid_vector = self.avoid(player, self.all_players, 1)
                mov_vector = avoid_vector
                look_vector = self.pursue(player, self.ball.getPosition())

            mov_vector = mov_vector.clamp_magnitude(1)
            mov_vector_rotated = self.transformToPlayer(player, mov_vector)

            look_vector_rotated = self.transformToPlayer(player, look_vector)

            rot = np.interp(look_vector_rotated.as_polar()[1], [-180, 180], [2, -2])
            rot = max(min(rot, 1), -1)

            self.show(GUI, player, mov_vector)
            player.act(mov_vector_rotated, rot)

    def ballPlan(self, GUI, field):
        avoid_vector = self.avoid(self.ball, self.enemy_players, 1.5)
        pursue_vector = self.pursue(self.ball, self.field.getCenterPosition(field))
        mov_vector = avoid_vector + pursue_vector
        return mov_vector

    def avoid(self, own, others, dist):
        avoid_vector = math.Vector2(0.001)

        for other in others:
            if own.name != other.name:
                dif_vector = own.getPosition() - other.getPosition()
                dif_vector = dif_vector.clamp_magnitude(dist)
                dif_vector.scale_to_length(dist - dif_vector.magnitude())
                avoid_vector += dif_vector
        return avoid_vector

    def pursue(self, own, goal_position):
        pursue_vector = goal_position - own.getPosition()
        pursue_vector = pursue_vector.normalize()
        return pursue_vector

    def transformToPlayer(self, player, vector):
        angle = mt.radians(vector.as_polar()[1]) - player.getOrientation()
        return vector.magnitude() * math.Vector2(mt.cos(angle), mt.sin(angle))

    def show(self, GUI, player, goal, color=[0, 255, 0]):
        pygame.draw.line(
            GUI.screen,
            color,
            GUI.mapToGUI(player.getPosition()),
            GUI.mapToGUI(player.getPosition() + goal),
            1,
        )
