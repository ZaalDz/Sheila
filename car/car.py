from gpiozero import Motor

import time


class Car:
    def __init__(self, speed: float = 1):
        self.speed = speed

        self.left_motors_1 = Motor(forward=24, backward=25)
        self.left_motors_2 = Motor(forward=18, backward=23)

        self.right_motors_1 = Motor(forward=12, backward=16)
        self.right_motors_2 = Motor(forward=20, backward=21)

    def stop(self):
        self.left_motors_1.stop()
        self.left_motors_2.stop()
        self.right_motors_1.stop()
        self.right_motors_2.stop()

    def forward(self, duration: float, speed: float = None):
        self.stop()
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors_1.forward(speed=speed)
        self.left_motors_2.forward(speed=speed)
        self.right_motors_1.forward(speed=speed)
        self.right_motors_2.forward(speed=speed)

        time.sleep(duration)
        self.stop()

    def backward(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.stop()
        self.left_motors_1.backward(speed=speed)
        self.left_motors_2.backward(speed=speed)
        self.right_motors_1.backward(speed=speed)
        self.right_motors_2.backward(speed=speed)

        time.sleep(duration)
        self.stop()

    def left(self, duration: float, speed: float = None):
        self.stop()
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors_1.backward(speed=speed)
        self.left_motors_2.backward(speed=speed)
        self.right_motors_1.forward(speed=speed)
        self.right_motors_2.forward(speed=speed)

        time.sleep(duration)
        self.stop()

    def right(self, duration: float, speed: float = None):
        self.stop()
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.left_motors_1.forward(speed=speed)
        self.left_motors_2.forward(speed=speed)
        self.right_motors_1.backward(speed=speed)
        self.right_motors_2.backward(speed=speed)

        time.sleep(duration)
        self.stop()
