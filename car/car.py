from gpiozero import Motor

import time


class Car:
    def __init__(self, speed: float = 1):
        self.speed = speed

        self.left_motors = Motor(forward=20, backward=21)
        self.right_motors = Motor(forward=12, backward=16)

    def stop(self):
        self.left_motors.stop()
        self.right_motors.stop()

    def forward(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors.forward(speed=speed)
        self.right_motors.forward(speed=speed)

        time.sleep(duration)
        self.stop()

    def backward(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors.backward(speed=speed)
        self.right_motors.backward(speed=speed)

        time.sleep(duration)
        self.stop()

    def left(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors.backward(speed=speed)
        self.right_motors.forward(speed=speed)

        time.sleep(duration)
        self.stop()

    def right(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors.forward(speed=speed)
        self.right_motors.backward(speed=speed)

        time.sleep(duration)
        self.stop()
