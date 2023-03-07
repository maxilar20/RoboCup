from pygame import math

GAME_TIME = 1  # minutes


PLAYERS_DEF = [
    {
        "player": "1",
        "team": "red",
        "player_position": "goalie",
        "kickoff_pos": "-4 0 0.3",
        "penalty_pos": "-4 0 0.3",
        "channel": 0,
    },
    {
        "player": "2",
        "team": "red",
        "player_position": "defender",
        "kickoff_pos": "-2.5 0 0.3",
        "penalty_pos": "-2 3.2 0.3",
        "channel": 1,
    },
    {
        "player": "3",
        "team": "red",
        "player_position": "attacker_left",
        "kickoff_pos": "-1 0.5 0.3",
        "penalty_pos": "-1 3.2 0.3",
        "channel": 2,
    },
    {
        "player": "4",
        "team": "red",
        "player_position": "attacker_right",
        "kickoff_pos": "-1 -0.5 0.3",
        "penalty_pos": "2.25 0 0.3",
        "channel": 3,
    },
    {
        "player": "1",
        "team": "blue",
        "player_position": "goalie",
        "kickoff_pos": "4 0 0.3",
        "penalty_pos": "4 0 0.3",
        "channel": 4,
    },
    {
        "player": "2",
        "team": "blue",
        "player_position": "defender",
        "kickoff_pos": "2.5 0 0.3",
        "penalty_pos": "2 3.2 0.3",
        "channel": 5,
    },
    {
        "player": "3",
        "team": "blue",
        "player_position": "attacker_left",
        "kickoff_pos": "1 -0.5 0.3",
        "penalty_pos": "1 3.2 0.3",
        "channel": 6,
    },
    {
        "player": "4",
        "team": "blue",
        "player_position": "attacker_right",
        "kickoff_pos": "1 0.5 0.3",
        "penalty_pos": "-2.25 0 0.3",
        "channel": 7,
    },
]

BOUNDARIES = {
    "field": (math.Vector2(-4.5, 3), math.Vector2(4.5, -3)),
    "goal_red": (math.Vector2(-5, 0.7), math.Vector2(-4.5, -0.7)),
    "goal_blue": (math.Vector2(4.5, 0.7), math.Vector2(5, -0.7)),
    "penalty_red": (math.Vector2(-4.5, 1), math.Vector2(-4, -1)),
    "penalty_blue": (math.Vector2(4, 1), math.Vector2(4.5, -1)),
    "shooting_red": (math.Vector2(-4.5, 1.5), math.Vector2(-3.5, -1.5)),
    "shooting_blue": (math.Vector2(3.5, 1.5), math.Vector2(4.5, -1.5)),
    "side_red": (math.Vector2(-4.5, 3), math.Vector2(0, -3)),
    "side_blue": (math.Vector2(0, 3), math.Vector2(4.5, -3)),
    "flank1": (math.Vector2(-4.5, -2.5), math.Vector2(4.5, -3)),
    "flank2": (math.Vector2(-4.5, 3), math.Vector2(4.5, 2.5)),
}
