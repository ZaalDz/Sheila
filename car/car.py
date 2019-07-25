from gpiozero import Motor
from gpiozero import DistanceSensor
from settings import SAFE_DISTANCE_THRESHOLD


class Car:
    def __init__(self, speed: float = 1):
        self.speed = speed
        self.diff = 0.04

        self.forward_right_motor = Motor(forward=12, backward=16)
        self.backward_right_motor = Motor(forward=21, backward=20)

        self.forward_left_motor = Motor(forward=23, backward=18)
        self.backward_left_motor = Motor(forward=24, backward=25)

        self.distance = DistanceSensor(13, 6)

    def stop(self):
        self.forward_left_motor.stop()
        self.forward_right_motor.stop()
        self.backward_left_motor.stop()
        self.backward_right_motor.stop()

    def not_in_safe_distance(self, distance_threshold=SAFE_DISTANCE_THRESHOLD):
        return self.distance > distance_threshold

    def forward(self, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - self.diff)

        self.forward_left_motor.forward(speed=speed)
        self.forward_right_motor.forward(speed=right_speed)
        self.backward_left_motor.forward(speed=speed)
        self.backward_right_motor.forward(speed=right_speed)

    def backward(self, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - self.diff)

        self.forward_left_motor.backward(speed=speed)
        self.forward_right_motor.backward(speed=right_speed)
        self.backward_left_motor.backward(speed=speed)
        self.backward_right_motor.backward(speed=right_speed)

    def left(self, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - self.diff)

        self.forward_left_motor.backward(speed=speed)
        self.forward_right_motor.forward(speed=right_speed)
        self.backward_left_motor.backward(speed=speed)
        self.backward_right_motor.forward(speed=right_speed)

    def right(self, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - self.diff)

        self.forward_left_motor.forward(speed=speed)
        self.forward_right_motor.backward(speed=right_speed)
        self.backward_left_motor.forward(speed=speed)
        self.backward_right_motor.backward(speed=right_speed)
