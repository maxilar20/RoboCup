from controller import Supervisor
from Player import *

TIME_STEP = 32
robot = Supervisor()


def end_simulation():
    print("sim ended")


def time_up():
    print("checking if time up")


def start_timer():
    print("starting time")


def reset_simulation():
    print("reseting sim")


def goal():
    print("checking if there is goal")


def increment_counter():
    pass


def ball_out():
    pass


def spawn_players():
    for player in player_definitions:
        Player(robot, **player)


def spawn_ball():
    print("Spawing the ball at field center")
    root_node = robot.getRoot()
    children_field = root_node.getField("children")
    children_field.importMFNodeFromString(-1, 'DEF BALL RobocupSoccerBall { translation 0 0 1 }')
    ball_node = robot.getFromDef('BALL')

player_definitions = [
    {
        "player": "1",
        "team": "red",
        "position": "goalie",
        "translation": "-4 0 0.4",
    },
    {
        "player": "2",
        "team": "red",
        "position": "defender",
        "translation": "-2.5 0 0.4",
    },
    {
        "player": "3",
        "team": "red",
        "position": "attacker_left",
        "translation": "-1 0.5 0.4",
    },
    {
        "player": "4",
        "team": "red",
        "position": "attacker_right",
        "translation": "-1 -0.5 0.4",
    },
    {
        "player": "1",
        "team": "blue",
        "position": "goalie",
        "translation": "4 0 0.4",
    },
    {
        "player": "2",
        "team": "blue",
        "position": "defender",
        "translation": "2.5 0 0.4",
    },
    {
        "player": "3",
        "team": "blue",
        "position": "attacker_left",
        "translation": "1 -0.5 0.4",
    },
    {
        "player": "4",
        "team": "blue",
        "position": "attacker_right",
        "translation": "1 0.5 0.4",
    },
]


start_timer()

reset_simulation()

# Spawning entities
spawn_players()
spawn_ball()

# Running time step
i = 0
while robot.step(TIME_STEP) != -1:

    if time_up():
        break

    if goal():
        increment_counter()

    if ball_out():
        reset_simulation()

    i += 1

end_simulation()
