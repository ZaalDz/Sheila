from car.car import Car
from enums import CommandKeys, MovementType

car = Car()


def run_command(receive_command):
    print('=====>', receive_command)

    movement_type = receive_command[CommandKeys.MOVEMENT_TYPE]

    if movement_type == MovementType.FORWARD:
        move_speed = receive_command[CommandKeys.MOVE_SPEED]
        move_duration = receive_command[CommandKeys.MOVE_DURATION]
        car.forward(duration=move_duration, speed=move_speed)

    elif movement_type == MovementType.BACKWARD:
        move_speed = receive_command[CommandKeys.MOVE_SPEED]
        move_duration = receive_command[CommandKeys.MOVE_DURATION]
        car.backward(duration=move_duration, speed=move_speed)
    elif movement_type == MovementType.LEFT:
        rotate_speed = receive_command[CommandKeys.ROTATE_SPEED]
        rotate_duration = receive_command[CommandKeys.ROTATE_DURATION]
        car.left(duration=rotate_duration, speed=rotate_speed)
    elif movement_type == MovementType.RIGHT:
        rotate_speed = receive_command[CommandKeys.ROTATE_SPEED]
        rotate_duration = receive_command[CommandKeys.ROTATE_DURATION]
        car.right(duration=rotate_duration, speed=rotate_speed)
