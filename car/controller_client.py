import socket
import time

from car.car import Car
from settings import CONTROLLER_PORT, IP
from util import send_command_dict, receive_command_dict
from enums import CommandKeys, MovementType

car = Car(pwm_frequency=150)


def start_controlling_car(conn):
    while True:
        recv_command = receive_command_dict(conn)

        if not recv_command:
            print('Connection broke')
            break

        movement_type = recv_command[CommandKeys.MOVEMENT_TYPE]
        duration = recv_command[CommandKeys.DURATION]

        if movement_type in {MovementType.FORWARD, MovementType.BACKWARD}:
            speed = recv_command[CommandKeys.SPEED]
            car.move(speed=speed, direction=movement_type, duration=duration)

        elif movement_type in {MovementType.LEFT, MovementType.RIGHT}:
            degree = recv_command[CommandKeys.CAR_ROTATION_DEGREE]
            car.turn_lr(degree=degree, duration=duration)

        elif movement_type in {MovementType.CAMERA_UP, MovementType.CAMERA_DOWN}:
            degree = recv_command[CommandKeys.CAMERA_ROTATION_DEGREE]
            car.camera_position(degree, duration=duration)

        send_command_dict(conn, recv_command)


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
