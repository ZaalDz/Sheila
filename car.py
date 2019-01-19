import time
import datetime
import RPi.GPIO as GPIO


class Directions:
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


class Car:

    def __init__(self, pwm_frequency=5000, rc_state=None):

        self.__testName = str(datetime.datetime.now()).replace(' ', '_')
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

        self.__FR.start(0)
        self.__BK.start(0)

        self.rc_state = rc_state if rc_state else {}

    def move(self, direction, duration, speed):
        """
        direction <string> "forward" / "backward"
        duration <float> in seconds
        speed <int> in % 
        """

        if direction == Directions.FORWARD:
            # switch off BW
            self.__BK.ChangeDutyCycle(0)
            # switch on FW
            self.__FR.ChangeDutyCycle(speed)
            time.sleep(duration)
            # stop motorb
            self.__FR.ChangeDutyCycle(0)
        elif direction == Directions.BACKWARD:
            # switch off FW
            self.__FR.ChangeDutyCycle(0)
            # switch on BW
            self.__BK.ChangeDutyCycle(speed)
            time.sleep(duration)
            # stop motorb
            self.__BK.ChangeDutyCycle(0)

        return self.rc_state

    def turn_lr(self, degree):
        """
        degree <int> between 5 and 10
        Returns degree if ok.
        Returns -1, if error
        """
        if 5 <= degree <= 9:
            self.__LR.ChangeDutyCycle(degree)
            time.sleep(0.5)
            self.__LR.ChangeDutyCycle(0)
            self.rc_state['turn_degree'] = degree
            return degree
        else:
            return -1

    def camera_position(self, position):
        if 9 <= position <= 12:
            self.__CAM.ChangeDutyCycle(position)
            time.sleep(0.5)
            self.__CAM.ChangeDutyCycle(0)
            self.rc_state['camera_position'] = position
            return self.rc_state
        else:
            return -1

    def __del__(self):
        GPIO.cleanup()
