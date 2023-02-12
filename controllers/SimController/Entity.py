class Entity:
    def __init__(self, robot, name, DEF, translation, rotation, custom_args=""):

        self.translation = translation

        root_node = robot.getRoot()
        children_field = root_node.getField("children")

        spawn_field = f"DEF {name} {DEF} {{translation {translation} rotation {rotation} {custom_args}}}"
        children_field.importMFNodeFromString(-1, spawn_field)

        self.node = robot.getFromDef(f"{name}")
        self.position_field = self.node.getField("translation")
        self.orientation_field = self.node.getField("rotation")

    def getPosition(self):
        return (
            self.position_field.getSFVec3f()[0],
            self.position_field.getSFVec3f()[1],
        )

    def getOrientation(self):
        return (
            self.orientation_field.getSFVec3f()[3]
            * self.orientation_field.getSFVec3f()[2]
        )

    def reset(self):
        self.position_field.setSFVec3f([float(i) for i in self.translation.split()])


class Player(Entity):
    def __init__(self, robot, player, team, player_position, translation, channel):

        self.name = f"{team}_{player}"
        self.team = team
        self.player_position = player_position

        RED_COLOR = [1, 0, 0]
        BLUE_COLOR = [0, 0, 1]

        if team == "red":
            color = RED_COLOR
            self.rotation = "0 0 1 0"
        else:
            color = BLUE_COLOR
            self.rotation = "0 0 1 3.1415"

        custom_args = f"customColor {color} channel {channel}"
        super().__init__(
            robot, self.name, "Nao", translation, self.rotation, custom_args
        )


class Ball(Entity):
    def __init__(self, robot):

        self.name = f"ball"
        self.translation = "0 0 0"
        self.rotation = "0 0 0 0"

        super().__init__(
            robot, self.name, "RobocupSoccerBall", self.translation, self.rotation
        )
