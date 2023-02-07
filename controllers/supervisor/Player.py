class Player:
    def __init__(self, robot, player, team, position, translation):
        self.team = team
        self.translation = translation

        root_node = robot.getRoot()
        children_field = root_node.getField("children")

        RED_COLOR = [1, 0, 0]
        BLUE_COLOR = [0, 0, 1]

        if team == "red":
            color = RED_COLOR
            rotation = "0 0 1 0"
        else:
            color = BLUE_COLOR
            rotation = "0 0 1 3.1415"
        children_field.importMFNodeFromString(
            -1,
            f"DEF {team}_{player} Nao {{translation {translation} rotation {rotation} customColor {color}}}",
        )

        self.node = robot.getFromDef(f"{team}_{player}")

    def getPosition(self):
        position_field = self.node.getField("translation")
        return (position_field.getSFVec3f()[0], position_field.getSFVec3f()[1])

    def getOrientation(self):
        orientation_field = self.node.getField("rotation")
        return orientation_field.getSFVec3f()[3]
