from pygame.math import Vector2 as vec2
import math as mt
import numpy as np
import pygame


class Coach:
    def __init__(self, own_players, enemy_players, field, ball, GUI):
        self.own_players = {}
        for player in own_players:
            self.own_players[player.player_position] = player

        self.enemy_players = {}
        for player in enemy_players:
            self.enemy_players[player.player_position] = player

        self.all_players = self.own_players | self.enemy_players
        self.field = field
        self.ball = ball

        self.GUI = GUI

        self.team = self.own_players["goalie"].team
        self.other_team = self.enemy_players["goalie"].team
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
<<<<<<< HEAD
        print(self.team)
        self.closestTo(self.ball, self.own_players)

=======
        # print(self.team + self.state)
>>>>>>> d71b4db4b75a4ffb36f5fb45e7126a47b6838550
        if self.field.isInside(self.ball.position, f"{self.other_team}_side"):
            self.state = "Attacking"
        elif self.field.isInside(self.ball.position, f"{self.team}_side"):
            self.state = "Defending"

        if self.state == "Attacking":
            self.attack()
        elif self.state == "Defending":
            self.defend()
        elif self.state == "Kick Off" or self.state == "Frozen":
            pass

    def attack(self):
        player = self.own_players["attacker_right"]
        goal_pos = self.field.getCenterPosition(f"goal_{self.other_team}")
        move_vector, look_vector = self.moveBall(player, goal_pos)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.own_players["attacker_left"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.own_players["defender"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.own_players["goalie"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

    def defend(self):
        player = self.own_players["attacker_right"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.own_players["attacker_left"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.own_players["defender"]
        move_vector, look_vector = self.moveBall(
            player, self.own_players["attacker_right"].position
        )
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

        player = self.own_players["goalie"]
        avoid_vector = player.avoidEntity(self.all_players, dist=1)
        move_vector = avoid_vector
        look_vector = player.pursue(self.ball.position)
        player.act(move_vector, look_vector)
        self.show(player, move_vector)

    def moveBall(self, player, goal_pos):
        ball_mov_vector = self.ballPlan(goal_pos)
        dribbling_pos = ball_mov_vector.normalize() * -0.3

        goal_pos = dribbling_pos + self.ball.position

        if (goal_pos - player.position).magnitude() > 0.3:
            avoid_vector = self.avoidEntity(player, self.all_players, dist=1)
            pursue_vector = self.pursue(player, goal_pos)
            move_vector = avoid_vector + pursue_vector
            look_vector = move_vector
        elif 0.15 < (goal_pos - player.position).magnitude() < 0.3:
            avoid_vector = self.avoidEntity(player, self.all_players, dist=1)
            pursue_vector = self.pursue(player, goal_pos)
            move_vector = avoid_vector + pursue_vector
            look_vector = self.ball.position

        else:
            pursue_vector = self.pursue(player, ball_mov_vector + self.ball.position)
            move_vector = pursue_vector
            look_vector = self.pursue(player, self.ball.position)

        return move_vector, look_vector

    def ballPlan(self, goal_pos):
        avoid_vector = self.avoidEntity(self.ball, self.enemy_players, 1)
        avoid_out_vector = self.avoidField(self.ball, 0.5)
        pursue_vector = self.pursue(self.ball, goal_pos)
        move_vector = avoid_vector + pursue_vector + avoid_out_vector
        return move_vector

    def avoidEntity(self, own, others, dist):
        avoid_vector = vec2(0.001)
        for other in others.values():
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

    def closestTo(self, own, others):
        distances = []
        for other in others.values():
            distances.append((own.position - other.position).magnitude())

        print(distances, min(distances))

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
