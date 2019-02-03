import socket
import time

from car.car import Car
from enums import CommandKeys, MovementType
from settings import CONTROLLER_PORT, IP
from util import send_command_dict, receive_command_dict

car = Car(pwm_frequency=150)


def start_controlling_car(conn):

    while True:
        recv_command_list = receive_command_dict(conn)

        if not recv_command_list:
            print('Connection broke')
            break

        for each_command in recv_command_list:

            movement_type = each_command[CommandKeys.MOVEMENT_TYPE]

            if movement_type in {MovementType.FORWARD, MovementType.BACKWARD}:
                speed = each_command[CommandKeys.SPEED]
                move_duration = each_command[CommandKeys.MOVE_DURATION]
                car.move(speed=speed, direction=movement_type, duration=move_duration)

            elif movement_type in {MovementType.LEFT, MovementType.RIGHT, MovementType.DEFAULT_WHEEL_POSITION}:
                degree = each_command[CommandKeys.CAR_ROTATION_DEGREE]
                rotate_duration = each_command[CommandKeys.ROTATE_DURATION]
                car.turn_lr(degree=degree, duration=rotate_duration)

            elif movement_type in {MovementType.CAMERA_UP, MovementType.CAMERA_DOWN,
                                   MovementType.DEFAULT_CAMERA_POSITION}:

                degree = each_command[CommandKeys.CAMERA_ROTATION_DEGREE]
                rotate_duration = each_command[CommandKeys.ROTATE_DURATION]
                car.camera_position(degree, duration=rotate_duration)

        send_command_dict(conn, recv_command_list)


def connect_to_server(my_socket: socket.socket):
    try:
        print('Trying to connect to controller')
        my_socket.connect((IP, CONTROLLER_PORT))
        print('Connection established')
        return True
    except socket.error as e:
        print(e)
        time.sleep(3)
        return False


def receive_commands():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            is_connected = connect_to_server(conn)
            if is_connected:
                start_controlling_car(conn)
