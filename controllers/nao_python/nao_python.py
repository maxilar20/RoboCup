from controller import Robot, Keyboard, Motion
import math
import numpy as np
from scipy import interpolate


class Nao(Robot):
    PHALANX_MAX = 8

    def __init__(self):
        Robot.__init__(self)
        self.currentlyPlaying = False

        # initialize stuff
        self.findAndEnableDevices()
        self.loadMotionFiles()

        # Animate handwave
        self.handWave.setLoop(False)
        self.handWave.play()
        self.currentlyPlaying = self.handWave

        # Walking parameters
        self.walk_speed = 1
        self.stride_time = 0.12
        self.smoothing = 0.8

        # init variables
        self.idx = 0
        self.t = 0
        self.start_t = self.t
        self.end_t = self.start_t + 1
        self.current_stride = [0.0, 0.0, 0.0, 0.0]
        self.new_stride = [0.0, 0.0, 0.0, 0.0]
        self.l, self.r = np.array([0.18, 0, 0, 0]), np.array([0.18, 0, 0, 0])

        self.updateStride()

    def run(self):
        while robot.step(self.timeStep) != -1:

            self.receiveMessage()

            if self.t > self.end_t:
                self.start_t = self.t
                self.end_t = self.start_t + self.stride_time
                self.idx += 1

            if self.idx > len(self.motion) - 1:
                self.idx = 0

            if self.idx in [1, 5]:
                if self.current_stride != self.new_stride:
                    self.current_stride = self.new_stride
                    self.updateStride()

                self.new_stride = [0.0, 0.0, 0.0, 0.0]
                stride_distance = np.linalg.norm(self.current_stride[:1])
                self.stride_time = max((stride_distance / self.walk_speed), 0.1)

            self.walk()

            self.t += self.timeStep / 1000

    def moveLegs(self, left, right):
        prefixes = ["L", "R"]
        for prefix, pos in zip(prefixes, [left, right]):
            L = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
            a = math.acos(((0.1**2) - (0.1**2) + (L**2)) / (2 * 0.1 * L))

            c = math.acos(((0.1**2) + (0.1**2) - (L**2)) / (2 * 0.1 * 0.1))
            alpha = math.atan2(pos[1], pos[0])
            H = a + alpha
            b = math.pi - c
            hip = -math.asin(pos[2] / L)

            self.actuateLegs(prefix, H, b, hip, pos)

    def actuateLegs(self, prefix, H, b, hip, pos):
        self.legJoints[prefix + "HipPitch"]["joint"].setPosition(-H)
        self.legJoints[prefix + "KneePitch"]["joint"].setPosition(b)
        self.legJoints[prefix + "AnklePitch"]["joint"].setPosition(H - b)
        self.legJoints[prefix + "HipRoll"]["joint"].setPosition(hip)
        self.legJoints[prefix + "AnkleRoll"]["joint"].setPosition(-hip)
        self.legJoints[prefix + "HipYawPitch"]["joint"].setPosition(pos[3])

    def walk(self):
        if self.start_t < self.t < self.end_t:
            t = [self.start_t, self.end_t]
            mot_l = np.array([self.motion[self.idx - 1][0], self.motion[self.idx][0]]).T
            mot_r = np.array([self.motion[self.idx - 1][1], self.motion[self.idx][1]]).T

            self.old_l = self.l
            self.old_r = self.r
            self.interp_l = interpolate.interp1d(t, np.array(mot_l), "linear")
            self.interp_r = interpolate.interp1d(t, np.array(mot_r), "linear")

            self.l = self.old_l * self.smoothing + self.interp_l(self.t) * (
                1 - self.smoothing
            )
            self.r = self.old_r * self.smoothing + self.interp_r(self.t) * (
                1 - self.smoothing
            )

            self.moveLegs(self.l, self.r)

    def receiveMessage(self):
        if self.receiver.getQueueLength() > 0:
            a = self.receiver.getFloats()
            self.receiver.nextPacket()
            self.old_stride = self.new_stride
            self.new_stride = [0.08 * a[0], 0.12 * a[1], 0.75 * a[2], 0.0]

    def updateStride(self):
        strd = self.current_stride
        cnstd_l = constrain(strd[0], -1, 0)
        cnstd_r = constrain(strd[0], 0, 1)
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

    def loadMotionFiles(self):
        self.handWave = Motion("./motions/HandWave.motion")
        self.forwards = Motion("./motions/Forwards.motion")
        self.backwards = Motion("./motions/Backwards.motion")
        self.sideStepLeft = Motion("./motions/SideStepLeft.motion")
        self.sideStepRight = Motion("./motions/SideStepRight.motion")
        self.turnLeft = Motion("./motions/TurnLeft40.motion")
        self.turnRight = Motion("./motions/TurnRight40.motion")
        self.shoot = Motion("./motions/Shoot.motion")

    def startMotion(self, motion):
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()

        motion.play()
        self.currentlyPlaying = motion

    def printGps(self):
        p = self.gps.getValues()
        print("----------gps----------")
        print("position: [ x y z ] = [%f %f %f]" % (p[0], p[1], p[2]))

    def setHandsAngle(self, angle):
        for i in range(0, self.PHALANX_MAX):
            clampedAngle = angle
            if clampedAngle > self.maxPhalanxMotorPosition[i]:
                clampedAngle = self.maxPhalanxMotorPosition[i]
            elif clampedAngle < self.minPhalanxMotorPosition[i]:
                clampedAngle = self.minPhalanxMotorPosition[i]

            if len(self.rphalanx) > i and self.rphalanx[i] is not None:
                self.rphalanx[i].setPosition(clampedAngle)
            if len(self.lphalanx) > i and self.lphalanx[i] is not None:
                self.lphalanx[i].setPosition(clampedAngle)

    def findAndEnableDevices(self):

        # get the time step of the current world.
        self.timeStep = int(self.getBasicTimeStep())

        # camera
        self.cameraTop = self.getDevice("CameraTop")
        self.cameraBottom = self.getDevice("CameraBottom")
        self.cameraTop.enable(4 * self.timeStep)
        self.cameraBottom.enable(4 * self.timeStep)

        # accelerometer
        self.accelerometer = self.getDevice("accelerometer")
        self.accelerometer.enable(4 * self.timeStep)

        # gyro
        self.gyro = self.getDevice("gyro")
        self.gyro.enable(4 * self.timeStep)

        # gps
        self.gps = self.getDevice("gps")
        self.gps.enable(4 * self.timeStep)

        # inertial unit
        self.inertialUnit = self.getDevice("inertial unit")
        self.inertialUnit.enable(self.timeStep)

        # ultrasound sensors
        self.us = []
        usNames = ["Sonar/Left", "Sonar/Right"]
        for i in range(0, len(usNames)):
            self.us.append(self.getDevice(usNames[i]))
            self.us[i].enable(self.timeStep)

        # foot sensors
        self.fsr = []
        fsrNames = ["LFsr", "RFsr"]
        for i in range(0, len(fsrNames)):
            self.fsr.append(self.getDevice(fsrNames[i]))
            self.fsr[i].enable(self.timeStep)

        # foot bumpers
        self.lfootlbumper = self.getDevice("LFoot/Bumper/Left")
        self.lfootrbumper = self.getDevice("LFoot/Bumper/Right")
        self.rfootlbumper = self.getDevice("RFoot/Bumper/Left")
        self.rfootrbumper = self.getDevice("RFoot/Bumper/Right")
        self.lfootlbumper.enable(self.timeStep)
        self.lfootrbumper.enable(self.timeStep)
        self.rfootlbumper.enable(self.timeStep)
        self.rfootrbumper.enable(self.timeStep)

        # there are 7 controlable LED groups in Webots
        self.leds = []
        self.leds.append(self.getDevice("ChestBoard/Led"))
        self.leds.append(self.getDevice("RFoot/Led"))
        self.leds.append(self.getDevice("LFoot/Led"))
        self.leds.append(self.getDevice("Face/Led/Right"))
        self.leds.append(self.getDevice("Face/Led/Left"))
        self.leds.append(self.getDevice("Ears/Led/Right"))
        self.leds.append(self.getDevice("Ears/Led/Left"))

        # get phalanx motor tags
        # the real Nao has only 2 motors for RHand/LHand
        # but in Webots we must implement RHand/LHand with 2x8 motors
        self.lphalanx = []
        self.rphalanx = []
        self.maxPhalanxMotorPosition = []
        self.minPhalanxMotorPosition = []
        for i in range(0, self.PHALANX_MAX):
            self.lphalanx.append(self.getDevice("LPhalanx%d" % (i + 1)))
            self.rphalanx.append(self.getDevice("RPhalanx%d" % (i + 1)))

            # assume right and left hands have the same motor position bounds
            self.maxPhalanxMotorPosition.append(self.rphalanx[i].getMaxPosition())
            self.minPhalanxMotorPosition.append(self.rphalanx[i].getMinPosition())

        # shoulder pitch motors
        self.RShoulderPitch = self.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.getDevice("LShoulderPitch")

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
        for idx in joint_names:
            L_name = "L" + idx
            R_name = "R" + idx
            joint = self.getDevice(L_name)
            self.legJoints[L_name] = {
                "joint": joint,
                "joint_position": joint.getTargetPosition(),
                "joint_max": joint.getMaxPosition(),
                "joint_min": joint.getMinPosition(),
            }
            joint = self.getDevice(R_name)
            self.legJoints[R_name] = {
                "joint": joint,
                "joint_position": joint.getTargetPosition(),
                "joint_max": joint.getMaxPosition(),
                "joint_min": joint.getMinPosition(),
            }

        # Keyboard
        self.keyboard = self.getKeyboard()
        self.keyboard.enable(10 * self.timeStep)

        # Receiver
        self.receiver = self.getDevice("receiver")
        self.receiver.enable(self.timeStep)


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


if __name__ == "__main__":
    robot = Nao()
    robot.run()
