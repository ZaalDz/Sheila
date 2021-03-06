from car.car import Car
from enums import CommandKeys, MovementType, Driver

car = Car()


def run_command(receive_command):
    print('=====>', receive_command)

    movement_type = receive_command[CommandKeys.COMMAND_TYPE]
    driver = receive_command[CommandKeys.DRIVER]
    if driver == Driver.AUTONOMOUS and car.not_in_safe_distance():
        car.stop()

    if movement_type == MovementType.FORWARD:
        move_speed = receive_command[CommandKeys.MOVE_SPEED]
        car.forward(speed=move_speed)

    elif movement_type == MovementType.BACKWARD:
        move_speed = receive_command[CommandKeys.MOVE_SPEED]
        car.backward(speed=move_speed)
    elif movement_type == MovementType.LEFT:
        rotate_speed = receive_command[CommandKeys.ROTATE_SPEED]
        car.left(speed=rotate_speed)
    elif movement_type == MovementType.RIGHT:
        rotate_speed = receive_command[CommandKeys.ROTATE_SPEED]
        car.right(speed=rotate_speed)
    elif movement_type == MovementType.STOP:
        car.stop()
