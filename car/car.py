from gpiozero import Motor

import time


class Car:
    def __init__(self, speed: float = 1):
        self.speed = speed

        self.forward_right_motor = Motor(forward=12, backward=16)
        self.backward_right_motor = Motor(forward=21, backward=20)

        self.forward_left_motor = Motor(forward=23, backward=18)
        self.backward_left_motor = Motor(forward=24, backward=25)

        self.motors = [self.forward_left_motor, self.forward_right_motor, self.backward_left_motor,
                       self.backward_right_motor]

    def stop(self):
        for each_motor in self.motors:
            each_motor.stop()

    def forward(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.forward_left_motor.forward(speed=speed)
        self.forward_right_motor.forward(speed=speed)
        self.backward_left_motor.forward(speed=speed)
        self.backward_right_motor.forward(speed=speed)

        time.sleep(duration)
        self.stop()

    def backward(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.forward_left_motor.backward(speed=speed)
        self.forward_right_motor.backward(speed=speed)
        self.backward_left_motor.backward(speed=speed)
        self.backward_right_motor.backward(speed=speed)

        time.sleep(duration)
        self.stop()

    def left(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.forward_left_motor.backward(speed=speed)
        self.forward_right_motor.forward(speed=speed)
        self.backward_left_motor.backward(speed=speed)
        self.backward_right_motor.forward(speed=speed)

        time.sleep(duration)
        self.stop()

    def right(self, duration: float, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        self.forward_left_motor.forward(speed=speed)
        self.forward_right_motor.backward(speed=speed)
        self.backward_left_motor.forward(speed=speed)
        self.backward_right_motor.backward(speed=speed)

        time.sleep(duration)
        self.stop()
