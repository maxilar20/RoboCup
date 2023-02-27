from pygame.math import Vector2 as vec2
import math as mt
import numpy as np
import pygame
import random
from Objects import *


class Coach:
    def __init__(
        self,
        own_players: list[Player],
        enemy_players: list[Player],
        field: Field,
        ball: Ball,
        GUI: GUI,
    ):
        self.own_players = own_players
        self.enemy_players = enemy_players
        self.all_players = self.own_players + self.enemy_players

        self.own_players_dict = {}
        for player in own_players:
            self.own_players_dict[player.player_position] = player

        self.support_offset = vec2(random.uniform(-0.5, 0.5), random.uniform(-1.5, 1.5))
        self.defender_offset = vec2(
            random.uniform(-0.5, 0.5), random.uniform(-1.5, 1.5)
        )

        self.field = field
        self.ball = ball

        self.GUI = GUI

        self.team = self.own_players[0].team
        self.other_team = self.enemy_players[0].team
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

    def act(self):

        player_list = self.own_players.copy()

        self.players_dict = {}

        goalie = self.own_players_dict["goalie"]
        self.players_dict["goalie"] = goalie
        player_list.remove(goalie)

        attacker_right = self.closestTo(self.ball.position, player_list)
        self.players_dict["attacker_right"] = attacker_right
        player_list.remove(attacker_right)

        attacker_left = self.closestTo(self.ball.position + vec2(2, 0), player_list)
        self.players_dict["attacker_left"] = attacker_left
        player_list.remove(attacker_left)

        own_goal_pos = self.field.getCenterPosition(f"goal_{self.team}")
        self.defend_position = own_goal_pos + (
            0.5 * (self.ball.position - own_goal_pos)
        )
        self.players_dict["defender"] = player_list[0]

        self.state = "Attacking"
        if self.state == "Attacking":
            self.attack()
        elif self.state == "Defending":
            self.defend()
        elif self.state == "Kick Off" or self.state == "Frozen":
            pass

    def attack(self):
        player = self.players_dict["attacker_right"]
        goal_pos = self.field.getCenterPosition(f"goal_{self.other_team}")
        move_vector, look_vector = self.moveBall(player, goal_pos)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.players_dict["attacker_left"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        avoid_out = player.avoidField(self.lines, self.line_vectors, 0.5)
        goto_vector = player.pursue(
            self.ball.position + vec2(2, 0) + self.support_offset
        )
        move_vector = avoid_vector + goto_vector + (5 * avoid_out)
        look_vector = move_vector
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.players_dict["defender"]
        move_vector, look_vector = player.moveTo(
            self.defend_position,
            self.all_players,
            self.ball,
            self.lines,
            self.line_vectors,
        )

        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.players_dict["goalie"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

    def defend(self):
        pass

    def moveBall(self, player, goal_pos):
        ball_mov_vector = self.ballPlan(goal_pos)
        dribbling_pos = ball_mov_vector.normalize() * -0.2
        self.show(self.ball, dribbling_pos, [255, 0, 0])

        goal_pos = dribbling_pos + self.ball.position

        if (goal_pos - player.position).magnitude() > 0.5:
            avoid_vector = self.avoidEntity(player, self.all_players, dist=1)
            avoid_ball_vector = self.avoidEntity(player, [self.ball], dist=0.5)
            pursue_vector = self.pursue(player, goal_pos)
            move_vector = avoid_vector + pursue_vector + (5 * avoid_ball_vector)
            look_vector = move_vector
        elif 0.10 < (goal_pos - player.position).magnitude() < 0.5:
            avoid_vector = self.avoidEntity(player, self.all_players, dist=1)
            pursue_vector = self.pursue(player, goal_pos)
            move_vector = avoid_vector + pursue_vector
            look_vector = self.pursue(player, self.ball.position)
        else:
            pursue_vector = self.pursue(player, ball_mov_vector + self.ball.position)
            move_vector = pursue_vector
            look_vector = self.pursue(player, self.ball.position)
            if self.field.isInside(self.ball.position, f"shooting_{self.other_team}"):
                player.kick()

        return move_vector, look_vector

    def ballPlan(self, goal_pos):
        avoid_vector = self.avoidEntity(self.ball, self.enemy_players, 0.5)

        avoid_out_vector = vec2(0)
        if not self.field.isInside(self.ball.position, f"penalty_{self.other_team}"):
            avoid_out_vector = self.avoidField(self.ball, 0.5)

        pursue_vector = self.pursue(self.ball, goal_pos)
        move_vector = (3 * avoid_vector) + pursue_vector + (2 * avoid_out_vector)

        self.show(self.ball, move_vector)

        return move_vector

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

    def closestTo(self, pos, others):
        distances = []
        for other in others:
            distances.append((pos - other.position).magnitude())
        return others[np.argmin(distances)]

    def transformToPlayer(self, player, vector):
        angle = mt.radians(vector.as_polar()[1]) - player.getOrientation()
        return vector.magnitude() * vec2(mt.cos(angle), mt.sin(angle))

    def show(self, player, goal, color=[0, 255, 0]):
        pygame.draw.line(
            self.GUI.screen,
            color,
            self.GUI.mapToGUI(player.position),
            self.GUI.mapToGUI(player.position + goal),
            1,
        )


def lineseg_dist(p, a, b):
    d = np.divide(b - a, np.linalg.norm(b - a))

    s = np.dot(a - p, d)
    t = np.dot(p - b, d)

    h = np.maximum.reduce([s, t, 0])

    c = np.cross(p - a, d)

    return np.hypot(h, np.linalg.norm(c))
