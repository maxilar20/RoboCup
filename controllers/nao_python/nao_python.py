from controller import Robot, Motion
import math
import numpy as np
from scipy import interpolate


class Nao(Robot):
    def __init__(self):
        Robot.__init__(self)

        # initialize stuff
        self.timeStep = int(self.getBasicTimeStep())
        self.findAndEnableDevices()

        # Walking parameters
        self.walk_speed = 1
        self.stride_time = 0.12
        self.smoothing = 0.8

        # init variables
        self.idx = 0
        self.t = 0
        self.start_t = self.t
        self.end_t = self.start_t + self.stride_time
        self.current_stride = [0.0, 0.0, 0.0]
        self.new_stride = [0.0, 0.0, 0.0]
        self.l, self.r = np.array([0.18, 0, 0, 0]), np.array([0.18, 0, 0, 0])

        self.state = "walking"
        self.old_state = self.state

        # Animate handwave
        self.handWave = Motion("./motions/HandWave.motion")
        self.handWave.setLoop(False)
        self.handWave.play()

    def run(self):
        self.t += self.timeStep / 1000

        self.message = self.receiveMessage()

        if not self.message:
            return

        # Inputs
        if self.message[3] == 0:
            self.new_state = "walking"
            self.state_done = False
        elif self.message[3] == 1:
            self.new_state = "kicking"
            self.state_done = False
        elif self.message[3] == 2:
            self.new_state = "standing"
            self.state_done = False

        # State Machine
        if self.state == "walking":
            print("Walking")

            self.walk_speed = 1
            self.smoothing = 0.8
            self.walk()

        elif self.state == "kicking":
            print("Kicking")

            self.walk_speed = 1
            self.smoothing = 0
            self.kick()

        elif self.state == "standing":
            print("Standing")

        # Change of state
        if self.state_done:
            self.old_state = self.state
            self.state = self.new_state

            if self.old_state != self.state:
                self.idx = 0

    def kick(self):
        self.updateStride("kick")

        if self.idx > len(self.motion) - 1:
            self.state_done = True
            return

        if self.t > self.end_t:
            self.start_t = self.t
            self.end_t = self.start_t + self.stride_time
            self.idx += 1

        if self.start_t < self.t < self.end_t:
            inverse_kinematics = self.inverseKinematics()
            self.moveLegs(inverse_kinematics)

    def walk(self):
        self.updateStride("walk")

        self.old_stride = self.new_stride
        self.new_stride = [
            0.08 * self.message[0],
            0.12 * self.message[1],
            0.75 * self.message[2],
        ]

        if self.t > self.end_t:
            self.start_t = self.t
            self.end_t = self.start_t + self.stride_time
            self.idx += 1

        if self.idx > len(self.motion) - 1:
            self.idx = 0

        if self.idx in [1, 5]:
            self.state_done = True
            if self.current_stride != self.new_stride:
                self.current_stride = self.new_stride

            self.new_stride = [0.0, 0.0, 0.0]
            stride_distance = np.linalg.norm(self.current_stride[:1])
            self.stride_time = max((stride_distance / self.walk_speed), 0.1)

        if self.start_t < self.t < self.end_t:
            inverse_kinematics = self.inverseKinematics()
            self.moveLegs(inverse_kinematics)

    def moveLegs(self, inverse_kineamtics):
        prefixes = ["L", "R"]
        for prefix, pos in zip(prefixes, inverse_kineamtics):
            L = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
            a = math.acos(((0.1**2) - (0.1**2) + (L**2)) / (2 * 0.1 * L))
            c = math.acos(((0.1**2) + (0.1**2) - (L**2)) / (2 * 0.1 * 0.1))
            alpha = math.atan2(pos[1], pos[0])

            HipPitch = a + alpha
            KneePitch = math.pi - c
            HipRoll = -math.asin(pos[2] / L)
            HipYawPitch = pos[3]

            self.actuateLegs(prefix, HipPitch, KneePitch, HipRoll, HipYawPitch)

    def actuateLegs(self, prefix, HipPitch, KneePitch, HipRoll, HipYawPitch):
        self.legJoints[prefix + "HipPitch"]["joint"].setPosition(-HipPitch)
        self.legJoints[prefix + "KneePitch"]["joint"].setPosition(KneePitch)
        self.legJoints[prefix + "AnklePitch"]["joint"].setPosition(HipPitch - KneePitch)
        self.legJoints[prefix + "HipRoll"]["joint"].setPosition(HipRoll)
        self.legJoints[prefix + "AnkleRoll"]["joint"].setPosition(-HipRoll)
        self.legJoints[prefix + "HipYawPitch"]["joint"].setPosition(HipYawPitch)

    def inverseKinematics(self):
        time_array = [self.start_t, self.end_t]
        motion_l = np.array([self.motion[self.idx - 1][0], self.motion[self.idx][0]]).T
        motion_r = np.array([self.motion[self.idx - 1][1], self.motion[self.idx][1]]).T

        self.interp_l = interpolate.interp1d(time_array, np.array(motion_l), "linear")
        self.interp_r = interpolate.interp1d(time_array, np.array(motion_r), "linear")

        self.old_l = self.l
        self.old_r = self.r

        smoothing_comp = 1 - self.smoothing
        self.l = self.old_l * self.smoothing + self.interp_l(self.t) * smoothing_comp
        self.r = self.old_r * self.smoothing + self.interp_r(self.t) * smoothing_comp

        return (self.l, self.r)

    def receiveMessage(self):
        if self.receiver.getQueueLength() > 0:
            message = self.receiver.getFloats()
            self.receiver.nextPacket()
            return message

    def updateStride(self, action):
        if action == "walk":
            strd = self.current_stride

            cnstd_l = min(strd[0], 0)
            cnstd_r = max(strd[0], 0)

            self.motion = [
                ((0.14, strd[1], cnstd_l, -strd[2]), (0.16, 0, -0.05, strd[2])),
                ((0.16, strd[1], cnstd_l, -strd[2]), (0.16, 0, -0.05, 0)),
                ((0.16, 0, 0.05, -strd[2]), (0.16, -strd[1], -cnstd_l, 0)),
                ((0.16, 0, 0.05, -strd[2]), (0.14, -strd[1], -cnstd_l, strd[2])),
                ((0.16, 0, 0.05, 0), (0.14, 0, 0, strd[2])),
                ((0.16, 0, 0.05, 0), (0.14, strd[1], cnstd_r, strd[2])),
                ((0.16, 0, 0.05, 0), (0.16, strd[1], cnstd_r, strd[2])),
                ((0.16, -strd[1], -cnstd_r, 0), (0.16, 0, -0.05, strd[2])),
                ((0.14, -strd[1], -cnstd_r, -strd[2]), (0.16, 0, -0.05, 0)),
                ((0.14, 0, 0, -strd[2]), (0.16, 0, -0.05, 0)),
            ]

        elif action == "kick":
            self.motion = [
                ((0.16, 0, 0, 0), (0.16, 0, 0, 0)),
                ((0.16, 0, 0.05, 0), (0.16, 0, 0, 0)),
                ((0.16, 0, 0.05, 0), (0.12, 0, 0, 0)),
                ((0.16, 0, 0.05, 0), (0.12, 0.15, 0, 0)),
                ((0.16, 0, 0.05, 0), (0.12, 0, 0, 0)),
                ((0.16, 0, 0.05, 0), (0.12, 0, 0, 0)),
            ]

    def findAndEnableDevices(self):
        # Legs
        joint_names = [
            "HipYawPitch",
            "HipRoll",
            "HipPitch",
            "KneePitch",
            "AnklePitch",
            "AnkleRoll",
        ]
        self.legJoints = {}
        prefixes = ["L", "R"]
        for prefix in prefixes:
            for idx in joint_names:
                joint_name = prefix + idx
                joint = self.getDevice(joint_name)
                self.legJoints[joint_name] = {
                    "joint": joint,
                    "joint_position": joint.getTargetPosition(),
                    "joint_max": joint.getMaxPosition(),
                    "joint_min": joint.getMinPosition(),
                }

        # Receiver
        self.receiver = self.getDevice("receiver")
        self.receiver.enable(self.timeStep)


if __name__ == "__main__":
    robot = Nao()
    while robot.step(robot.timeStep) != -1:
        robot.run()
