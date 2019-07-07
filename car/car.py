from gpiozero import Motor


class Car:
    def __init__(self, speed: float = 1):
        self.speed = speed

        self.forward_right_motor = Motor(forward=12, backward=16)
        self.backward_right_motor = Motor(forward=21, backward=20)

        self.forward_left_motor = Motor(forward=23, backward=18)
        self.backward_left_motor = Motor(forward=24, backward=25)

    def stop(self):
        self.forward_left_motor.stop()
        self.forward_right_motor.stop()
        self.backward_left_motor.stop()
        self.backward_right_motor.stop()

    def forward(self, speed: float = None):

        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - 0.04)

        self.forward_left_motor.forward(speed=speed)
        self.forward_right_motor.forward(speed=right_speed)
        self.backward_left_motor.forward(speed=speed)
        self.backward_right_motor.forward(speed=right_speed)

    def backward(self, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - 0.04)

        self.forward_left_motor.backward(speed=speed)
        self.forward_right_motor.backward(speed=right_speed)
        self.backward_left_motor.backward(speed=speed)
        self.backward_right_motor.backward(speed=right_speed)

    def left(self, speed: float = None):

        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - 0.04)

        self.forward_left_motor.backward(speed=speed)
        self.forward_right_motor.forward(speed=right_speed)
        self.backward_left_motor.backward(speed=speed)
        self.backward_right_motor.forward(speed=right_speed)

    def right(self, speed: float = None):
        speed = max(min(speed if speed else self.speed, 1), 0)
        right_speed = max(0.0, speed - 0.04)

        self.forward_left_motor.forward(speed=speed)
        self.forward_right_motor.backward(speed=right_speed)
        self.backward_left_motor.forward(speed=speed)
        self.backward_right_motor.backward(speed=right_speed)
