import datetime
import time

import RPi.GPIO as GPIO
from enums import MovementType
from settings import CarSettings


class Car:

    def __init__(self, pwm_frequency=5000, rc_state=None):

        self.__testName = str(datetime.datetime.now()).replace(' ', '_')
        self.rc_state = rc_state if rc_state else {}
        self.__FW_MOVE_PIN = 40
        self.__BW_MOVE_PIN = 38
        self.__LR_MOVE_PIN = 36
        self.__CAM_MOVE_PIN = 32

        # Prevent setting distructive frequency
        if 100 <= pwm_frequency <= 5000:
            self.pwm_frequency = pwm_frequency
        else:
            self.pwm_frequency = 5000

        # Set gpio pin mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.__FW_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__FW_MOVE_PIN, GPIO.LOW)
        GPIO.setup(self.__BW_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__BW_MOVE_PIN, GPIO.LOW)
        GPIO.setup(self.__LR_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__LR_MOVE_PIN, GPIO.LOW)
        GPIO.setup(self.__CAM_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__CAM_MOVE_PIN, GPIO.LOW)

        self.__FR = GPIO.PWM(self.__FW_MOVE_PIN, self.pwm_frequency)
        self.__BK = GPIO.PWM(self.__BW_MOVE_PIN, self.pwm_frequency)

        # Setup servos
        self.__LR = GPIO.PWM(self.__LR_MOVE_PIN, 50)
        self.__CAM = GPIO.PWM(self.__CAM_MOVE_PIN, 50)

        self.__LR.start(0)
        self.__CAM.start(0)

        self.turn_lr(CarSettings.STARTING_ROTATION_POSITION, 0.5)
        self.camera_position(CarSettings.STARTING_CAMERA_POSITION, 0.5)

        self.__FR.start(0)
        self.__BK.start(0)

    def move(self, speed, direction, duration):

        if direction == MovementType.FORWARD:
            # switch off BW
            self.__BK.ChangeDutyCycle(0)
            # switch on FW
            self.__FR.ChangeDutyCycle(speed)
            time.sleep(duration)
            # stop motorb
            self.__FR.ChangeDutyCycle(0)
        elif direction == MovementType.BACKWARD:
            # switch off FW
            self.__FR.ChangeDutyCycle(0)
            # switch on BW
            self.__BK.ChangeDutyCycle(speed)
            time.sleep(duration)
            # stop motorb
            self.__BK.ChangeDutyCycle(0)

        return self.rc_state

    def turn_lr(self, degree, duration):

        if CarSettings.MIN_LEFT_TURN <= degree <= CarSettings.MAX_RIGHT_TURN:
            self.__LR.ChangeDutyCycle(degree)
            time.sleep(duration)
            self.__LR.ChangeDutyCycle(0)
            self.rc_state['turn_degree'] = degree
            return degree
        else:
            return -1

    def camera_position(self, degree, duration):

        if CarSettings.MIN_CAMERA_POSITION <= degree <= CarSettings.MAX_CAMERA_POSITION:
            self.__CAM.ChangeDutyCycle(degree)
            time.sleep(duration)
            self.__CAM.ChangeDutyCycle(0)
            self.rc_state['camera_position'] = degree
            return self.rc_state
        else:
            return -1

    def __del__(self):
        GPIO.cleanup()
