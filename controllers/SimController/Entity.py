class Entity:
    def __init__(
        self, robot, name, DEF, translation, rotation, custom_args="", circle_radius=0.1
    ):
        self.name = name
        self.translation = translation
        self.rotation = rotation
        self.circle_radius = circle_radius

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

        # Player Attributes
        self.team = team
        self.player_position = player_position

        # Node Spawning
        if team == "red":
            color = [1, 0, 0]
            rotation = "0 0 1 0"
        else:
            color = [0, 0, 1]
            rotation = "0 0 1 3.1415"

        custom_args = f"customColor {color} channel {channel}"

        super().__init__(
            robot,
            f"{team}_{player}",
            "Nao",
            translation,
            rotation,
            custom_args,
            circle_radius=0.15,
        )


class Ball(Entity):
    def __init__(self, robot):
        super().__init__(
            robot,
            "ball",
            "RobocupSoccerBall",
            "0 0 0",
            "0 0 0 0",
            circle_radius=0.1,
        )
