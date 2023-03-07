from pygame import math


class Entity:
    def __init__(
        self, robot, name, DEF, translation, rotation, custom_args="", circle_radius=0.1
    ):
        self.robot = robot
        self.name = name

        self.DEF = DEF
        self.translation = translation

        self.rotation = rotation
        self.custom_args = custom_args
        self.circle_radius = circle_radius

        self.circle_radius_sq = circle_radius**2

        self.spawn()

        self.node = self.robot.getFromDef(f"{self.name}")
        self.position_field = self.node.getField("translation")

        self.orientation_field = self.node.getField("rotation")
        self.getPosition()
        self.getOrientation()

    def spawn(self):
        root_node = self.robot.getRoot()
        children_field = root_node.getField("children")

        spawn_field = f"DEF {self.name} {self.DEF} {{translation {self.translation} rotation {self.rotation} {self.custom_args}}}"
        children_field.importMFNodeFromString(-1, spawn_field)

    def getPosition(self):
        self.position = math.Vector2(self.position_field.getSFVec3f()[:2])
        return self.position

    def getOrientation(self):
        if self.orientation_field.getSFVec3f()[2] > 0:
            self.orientation = self.orientation_field.getSFVec3f()[3]
        else:
            self.orientation = (2 * 3.1415) - self.orientation_field.getSFVec3f()[3]
        return self.orientation

    def getGyro(self):
        return self.orientation_field.getSFRotation()

    def isInside(self, point):
        return point.distance_squared_to(self.position) < (self.circle_radius_sq)

    def setPosition(self, pos):
        if type(pos) == str:
            self.position_field.setSFVec3f([float(i) for i in pos.split()])
        else:
            self.position_field.setSFVec3f(pos)

    def resetPosition(self):
        self.position_field.setSFVec3f([float(i) for i in self.translation.split()])

    def resetOrientation(self):
        self.orientation_field.setSFRotation([float(i) for i in self.rotation.split()])

    def resetHeight(self):
        position = list(self.getPosition())
        position.append(0.32)
        self.position_field.setSFVec3f(position)

    def resetPhysics(self):
        self.node.resetPhysics()

    def update(self):
        self.getPosition()
        self.getOrientation()

    def show(self):
        return
