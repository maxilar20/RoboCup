from pygame.math import Vector2 as vec2
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

        self.players_dict = {}
        for player in self.own_players:
            self.players_dict[player.player_position] = player
        print(self.players_dict)

        self.team = self.own_players[0].team
        self.goal_name = "goal_blue" if self.team == "red" else "goal_red"
        top_left, bottom_right = field.boundaries["field"]
        self.lines = self.getLinesInRect(top_left, bottom_right)
        self.line_vectors = [vec2(0, -1), vec2(1, 0), vec2(0, 1), vec2(-1, 0)]

        self.state = "Attacking"

    def getLinesInRect(self, top_left, bottom_right):
        return [
            (top_left, top_left.reflect((-1, 0))),
            (top_left, top_left.reflect((0, -1))),
            (bottom_right, bottom_right.reflect((-1, 0))),
            (bottom_right, bottom_right.reflect((0, -1))),
        ]

    def act(self, GUI):
        # print(self.team + self.state)

        if self.state == "Attacking":
            self.attack(GUI)
        elif self.state == "Defending":
            pass
        elif self.state == "Kick Off" or self.state == "Frozen":
            pass

    def attack(self, GUI):
        # Ball Plan
        ball_mov_vector = self.ballPlan(self.goal_name)
        dribbling_pos = ball_mov_vector.normalize() * -0.3

        for player in self.own_players:
            if player.player_position == "attacker_right":

                goal_pos = dribbling_pos + self.ball.position

                if (goal_pos - player.position).magnitude() > 0.3:
                    avoid_vector = self.avoidEntity(player, self.all_players, 1)
                    pursue_vector = self.pursue(player, goal_pos)
                    mov_vector = avoid_vector + pursue_vector
                    look_vector = mov_vector
                elif 0.15 < (goal_pos - player.position).magnitude() < 0.3:
                    avoid_vector = self.avoidEntity(player, self.all_players, 1)
                    pursue_vector = self.pursue(player, goal_pos)
                    mov_vector = avoid_vector + pursue_vector
                    look_vector = self.ball.position

                else:
                    pursue_vector = self.pursue(
                        player, ball_mov_vector + self.ball.position
                    )
                    mov_vector = pursue_vector
                    look_vector = self.pursue(player, self.ball.position)
            else:
                avoid_vector = self.avoidEntity(player, self.all_players, 1)
                mov_vector = avoid_vector
                look_vector = self.pursue(player, self.ball.position)

            mov_vector = mov_vector.clamp_magnitude(1)
            mov_vector_rotated = self.transformToPlayer(player, mov_vector)

            look_vector_rotated = self.transformToPlayer(player, look_vector)

            rot = np.interp(look_vector_rotated.as_polar()[1], [-180, 180], [2, -2])
            rot = max(min(rot, 1), -1)

            player.act(mov_vector_rotated, rot)

            self.show(GUI, player, mov_vector)

        self.show(GUI, self.ball, ball_mov_vector)
        self.show(GUI, self.ball, dribbling_pos, color=[255, 0, 0])

    def ballPlan(self, field):
        avoid_vector = self.avoidEntity(self.ball, self.enemy_players, 1)
        avoid_out_vector = self.avoidField(self.ball, 0.5)
        pursue_vector = self.pursue(self.ball, self.field.getCenterPosition(field))
        mov_vector = avoid_vector + pursue_vector + avoid_out_vector
        return mov_vector

    def avoidEntity(self, own, others, dist):
        avoid_vector = vec2(0.001)
        for other in others:
            if own.name != other.name:
                dif_vector = own.position - other.position
                dif_vector = dif_vector.clamp_magnitude(dist)
                dif_vector.scale_to_length(dist - dif_vector.magnitude())
                avoid_vector += dif_vector
        return avoid_vector

    def avoidField(self, own, dist):
        avoid_vector = vec2(0.001)
        for line, vector in zip(self.lines, self.line_vectors):
            dif_vector = vector * lineseg_dist(own.position, line[0], line[1])
            dif_vector = dif_vector.clamp_magnitude(dist)
            dif_vector.scale_to_length(dist - dif_vector.magnitude())
            avoid_vector += dif_vector
        return avoid_vector

    def pursue(self, own, goal_position):
        pursue_vector = goal_position - own.position
        pursue_vector = pursue_vector.normalize()
        return pursue_vector

    def transformToPlayer(self, player, vector):
        angle = mt.radians(vector.as_polar()[1]) - player.getOrientation()
        return vector.magnitude() * vec2(mt.cos(angle), mt.sin(angle))

    def show(self, GUI, player, goal, color=[0, 255, 0]):
        pygame.draw.line(
            GUI.screen,
            color,
            GUI.mapToGUI(player.position),
            GUI.mapToGUI(player.position + goal),
            1,
        )


def lineseg_dist(p, a, b):
    d = np.divide(b - a, np.linalg.norm(b - a))

    s = np.dot(a - p, d)
    t = np.dot(p - b, d)

    h = np.maximum.reduce([s, t, 0])

    c = np.cross(p - a, d)

    return np.hypot(h, np.linalg.norm(c))
