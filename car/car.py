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

        self.forward = GPIO.PWM(self.__FW_MOVE_PIN, self.pwm_frequency)
        self.backward = GPIO.PWM(self.__BW_MOVE_PIN, self.pwm_frequency)

        # Setup servos
        self.left_right = GPIO.PWM(self.__LR_MOVE_PIN, 50)
        self.camera = GPIO.PWM(self.__CAM_MOVE_PIN, 50)

        self.left_right.start(0)
        self.camera.start(0)

        self.set_camera_starting_position()
        self.set_wheel_starting_position()

        self.forward.start(0)
        self.backward.start(0)

    def set_camera_starting_position(self):
        self.camera_position(CarSettings.STARTING_CAMERA_POSITION, 0.5)

    def set_wheel_starting_position(self):
        self.turn_lr(CarSettings.STARTING_ROTATION_POSITION, 0.5)

    def move(self, speed, direction, duration):

        if direction == MovementType.FORWARD:
            # switch off BW
            self.backward.ChangeDutyCycle(0)
            # switch on FW
            self.forward.ChangeDutyCycle(speed)
            time.sleep(duration)
            # stop motorb
            self.forward.ChangeDutyCycle(0)
        elif direction == MovementType.BACKWARD:
            # switch off FW
            self.forward.ChangeDutyCycle(0)
            # switch on BW
            self.backward.ChangeDutyCycle(speed)
            time.sleep(duration)
            # stop motorb
            self.backward.ChangeDutyCycle(0)

        return self.rc_state

    def turn_lr(self, degree, duration):

        if CarSettings.MIN_LEFT_TURN <= degree <= CarSettings.MAX_RIGHT_TURN:
            self.left_right.ChangeDutyCycle(degree)
            time.sleep(duration)
            self.left_right.ChangeDutyCycle(0)
            self.rc_state['turn_degree'] = degree

        return self.rc_state

    def forward_left_right(self, speed: float, degree: float, duration: float):

        self.backward.ChangeDutyCycle(0)
        self.forward.ChangeDutyCycle(speed)

        if CarSettings.MIN_LEFT_TURN <= degree <= CarSettings.MAX_RIGHT_TURN:
            self.left_right.ChangeDutyCycle(degree)

        time.sleep(duration)

        self.forward.ChangeDutyCycle(0)
        self.left_right.ChangeDutyCycle(0)

    def backward_left_right(self, speed: float, degree: float, duration: float):

        self.forward.ChangeDutyCycle(0)
        self.backward.ChangeDutyCycle(speed)

        if CarSettings.MIN_LEFT_TURN <= degree <= CarSettings.MAX_RIGHT_TURN:
            self.left_right.ChangeDutyCycle(degree)

        time.sleep(duration)

        self.backward.ChangeDutyCycle(0)
        self.left_right.ChangeDutyCycle(0)

    def camera_position(self, degree, duration):

        if CarSettings.MIN_CAMERA_POSITION <= degree <= CarSettings.MAX_CAMERA_POSITION:
            self.camera.ChangeDutyCycle(degree)
            time.sleep(duration)
            self.camera.ChangeDutyCycle(0)
            self.rc_state['camera_position'] = degree

        return self.rc_state

    def __del__(self):
        GPIO.cleanup()
