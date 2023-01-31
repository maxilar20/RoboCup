class Player:
    def __init__(self, robot, player, team, position, translation):

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

        self.node = robot.getFromDef("red_1")
