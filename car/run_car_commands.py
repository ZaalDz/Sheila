from queue import Queue

from car.car import Car
from enums import CommandKeys, MovementType

commands_queue = Queue(maxsize=1)

car = Car(pwm_frequency=150)


def run_command():
    while True:
        if commands_queue.qsize():

            receive_command = commands_queue.get_nowait()

            print('=====>', receive_command)

            movement_type = receive_command[CommandKeys.MOVEMENT_TYPE]
            move_duration = receive_command[CommandKeys.MOVE_DURATION]

            if movement_type in {MovementType.FORWARD, MovementType.BACKWARD}:
                speed = receive_command[CommandKeys.SPEED]
                car.move(speed, movement_type, move_duration)

            elif movement_type in {MovementType.LEFT, MovementType.RIGHT, MovementType.DEFAULT_CAMERA_POSITION}:
                degree = receive_command[CommandKeys.CAR_ROTATION_DEGREE]
                car.turn_lr(degree, move_duration)

            elif movement_type in {MovementType.FORWARD_RIGHT, MovementType.FORWARD_LEFT}:
                degree = receive_command[CommandKeys.CAR_ROTATION_DEGREE]
                speed = receive_command[CommandKeys.SPEED]
                car.forward_left_right(speed, degree, move_duration)

            elif movement_type in {MovementType.BACKWARD_RIGHT, MovementType.BACKWARD_LEFT}:
                degree = receive_command[CommandKeys.CAR_ROTATION_DEGREE]
                speed = receive_command[CommandKeys.SPEED]
                car.backward_left_right(speed, degree, move_duration)
