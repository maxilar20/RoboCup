from controller import Supervisor
from Player import *
import time


class SimController(Supervisor):
    def __init__(self, max_game_time_mins=15):
        super().__init__()
        self.start_game_time_seconds = 0
        self.max_game_time_secs = max_game_time_mins * 60

    def reset_timer(self):
        print("Starting time")
        self.start_game_time_seconds = time.time()

    def reset_simulation(self):
        print("Reseting sim")

    def spawn_players(self):
        self.players = [Player(self, **player) for player in player_definitions]

    def spawn_ball(self):
        print("Spawning the ball at field center")
        root_node = self.getRoot()
        children_field = root_node.getField("children")
        children_field.importMFNodeFromString(-1, 'DEF BALL RobocupSoccerBall { translation 0 0 1 }')
        ball_node = self.getFromDef('BALL')
    
    '''
    Tried a different method for goal check using goal objects:

    def goal_check(self):
        print("checking goal")
        
        ball_node = self.getFromDef('BALL')
        goal_node_blue = self.getFromDef('GOAL_BLUE')
        goal_node_red = self.getFromDef('GOAL_RED')
        
        ball_position = ball_node.getField("translation").getSFVec3f()
        goal_position_blue = goal_node_blue.getField("translation").getSFVec3f()
        goal_position_red = goal_node_red.getField("translation").getSFVec3f()

    '''

    def goal_check(self):
        print("Checking goal")

        ball_node = self.getFromDef('BALL')
        ball_position = ball_node.getField("translation")
        ball_x = ball_position.getSFVec3f()[0]
        ball_y = ball_position.getSFVec3f()[1]

        if ball_x < -4.55 and ball_y < 0.7:
            #print("Score for blue team")
            return "blue"
        elif ball_x > 4.55 and ball_y < 0.7:
            #print("Score for red team")
            return "red"

    def ball_out(self):
        pass

    def time_up(self):
        time_passed = time.time() - self.start_game_time_seconds

        print(f"Game Time: {time.strftime('%M:%S',time.gmtime(time_passed))}")
        print(f"Checking if time up")

        return time_passed > self.max_game_time_secs

    def end_simulation(self):
        print("Sim ended")


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
