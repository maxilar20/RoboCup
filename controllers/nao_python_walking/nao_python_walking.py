from controller import Robot, Keyboard, Motion
import math
import numpy as np


class Nao(Robot):
    PHALANX_MAX = 8

    # load motion files
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
        # interrupt current motion
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()

        # start new motion
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
        for i in self.legJoints:
            print(i, self.legJoints[i])

        # keyboard
        self.keyboard = self.getKeyboard()
        self.keyboard.enable(10 * self.timeStep)

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

            self.legJoints[prefix + "HipPitch"]["joint"].setPosition(-H)
            self.legJoints[prefix + "KneePitch"]["joint"].setPosition(b)
            self.legJoints[prefix + "AnklePitch"]["joint"].setPosition(H - b)
            self.legJoints[prefix + "HipRoll"]["joint"].setPosition(hip)
            self.legJoints[prefix + "AnkleRoll"]["joint"].setPosition(-hip)

    def walk(self):
        stride = self.stride

        motion = [
            ((0.16, stride[1], constrain(stride[0], -0.05, 0)), (0.18, 0, -0.05)),
            ((0.18, stride[1], constrain(stride[0], -0.05, 0)), (0.18, 0, -0.05)),
            ((0.18, 0, 0.05), (0.18, -stride[1], -constrain(stride[0], -0.05, 0))),
            ((0.18, 0, 0.05), (0.16, -stride[1], -constrain(stride[0], -0.05, 0))),
            ((0.18, 0, 0.05), (0.16, 0, 0)),
            ((0.18, 0, 0.05), (0.16, stride[1], constrain(stride[0], 0, 0.05))),
            ((0.18, 0, 0.05), (0.18, stride[1], constrain(stride[0], 0, 0.05))),
            ((0.18, -stride[1], -constrain(stride[0], 0, 0.05)), (0.18, 0, -0.05)),
            ((0.16, -stride[1], -constrain(stride[0], 0, 0.05)), (0.18, 0, -0.05)),
            ((0.16, 0, 0), (0.18, 0, -0.05)),
        ]

        if self.t > self.end_t:
            self.start_t = self.t
            self.end_t = self.start_t + 0.075
            self.idx += 1

        if self.idx > len(motion) - 1:
            self.idx = 0

        if self.idx in [0, 4]:
            self.stride = self.new_stride
            self.new_stride = [0, 0, 0]

        if self.start_t < self.t < self.end_t:

            self.moveLegs(
                map_range(
                    self.t,
                    self.start_t,
                    self.end_t,
                    np.array(motion[self.idx - 1][0]),
                    np.array(motion[self.idx][0]),
                ),
                map_range(
                    self.t,
                    self.start_t,
                    self.end_t,
                    np.array(motion[self.idx - 1][1]),
                    np.array(motion[self.idx][1]),
                ),
            )

    def __init__(self):
        Robot.__init__(self)
        self.currentlyPlaying = False

        # initialize stuff
        self.findAndEnableDevices()
        self.loadMotionFiles()

    def run(self):
        self.handWave.setLoop(False)
        self.handWave.play()
        self.currentlyPlaying = self.handWave

        self.idx = 0
        self.t = 0
        self.start_t = self.t
        self.end_t = self.start_t + 1
        self.stride = [0, 0, 0]
        self.new_stride = [0, 0, 0]

        # until a key is pressed
        key = -1
        while robot.step(self.timeStep) != -1:

            key = self.keyboard.getKey()
            if key == Keyboard.LEFT:
                self.new_stride = [-0.035, 0, 0]
                # self.startMotion(self.sideStepLeft)
            if key == Keyboard.RIGHT:
                self.new_stride = [0.035, 0, 0]
                # self.startMotion(self.sideStepRight)
            if key == Keyboard.UP:
                self.new_stride = [0, 0.05, 0]
                # self.startMotion(self.forwards)
            if key == Keyboard.DOWN:
                self.new_stride = [0, -0.05, 0]
                # self.startMotion(self.backwards)

            if key == Keyboard.LEFT | Keyboard.SHIFT:
                self.startMotion(self.turnLeft)
            elif key == Keyboard.RIGHT | Keyboard.SHIFT:
                self.startMotion(self.turnRight)
            elif key == ord(" "):
                self.startMotion(self.shoot)

            # print("\x1b[2J")
            self.walk()

            self.t += self.timeStep / 1000


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


robot = Nao()
robot.run()
