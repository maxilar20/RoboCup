from pygame import math

GAME_TIME = 15  # minutes


player_definitions = [
    {
        "player": "1",
        "team": "red",
        "player_position": "goalie",
        "translation": "-4 0 0.3",
        "channel": 0,
    },
    {
        "player": "2",
        "team": "red",
        "player_position": "defender",
        "translation": "-2.5 0 0.3",
        "channel": 1,
    },
    {
        "player": "3",
        "team": "red",
        "player_position": "attacker_left",
        "translation": "-1 0.5 0.3",
        "channel": 2,
    },
    {
        "player": "4",
        "team": "red",
        "player_position": "attacker_right",
        "translation": "-1 -0.5 0.3",
        "channel": 3,
    },
    {
        "player": "1",
        "team": "blue",
        "player_position": "goalie",
        "translation": "4 0 0.3",
        "channel": 4,
    },
    {
        "player": "2",
        "team": "blue",
        "player_position": "defender",
        "translation": "2.5 0 0.3",
        "channel": 5,
    },
    {
        "player": "3",
        "team": "blue",
        "player_position": "attacker_left",
        "translation": "1 -0.5 0.3",
        "channel": 6,
    },
    {
        "player": "4",
        "team": "blue",
        "player_position": "attacker_right",
        "translation": "1 0.5 0.3",
        "channel": 7,
    },
]

boundaries = {
    "goal_red": (math.Vector2(-5, 0.7), math.Vector2(-4.5, -0.7)),
    "goal_blue": (math.Vector2(4.5, 0.7), math.Vector2(5, -0.7)),
    "field": (math.Vector2(-4.5, 3), math.Vector2(4.5, -3)),
    "penalty_red": (math.Vector2(-4.5, 1), math.Vector2(-4, -1)),
    "penalty_blue": (math.Vector2(4, 1), math.Vector2(4.5, -1)),
}
