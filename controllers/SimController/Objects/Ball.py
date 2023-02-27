from .Entity import Entity


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
